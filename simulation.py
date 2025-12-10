import numpy as np
import random

worldSize = 1000

class Organism:
    def __init__(self, name, species, age, x , y, detectionRadius, energy, energyCapacity):
        self.name = name
        self.species = species
        self.age = age
        self.x = x
        self.y = y
        self.detectionRadius = detectionRadius
        self.energy = energy
        self.energyCapacity = energyCapacity

    def tick(self):
        self.age += 1
        self.energy = max(self.energy - 1, 0)  # Decrease energy each tick

    def scanForFood(self, world):
        x_min = max(self.x - self.detectionRadius, 0)
        x_max = min(self.x + self.detectionRadius + 1, worldSize)
        y_min = max(self.y - self.detectionRadius, 0)
        y_max = min(self.y + self.detectionRadius + 1, worldSize)

        # Slice region around the organism
        area = world[x_min:x_max, y_min:y_max]
        # Find actual coordinates of food
        foodPositions = np.argwhere(area == 1) 
        if len(foodPositions) == 0:
            return None  # No food found

        # Convert to world coordinates
        foodGlobal = [(x_min + fx, y_min + fy) for fx, fy in foodPositions]

        # Compute closest food by distance
        closest = min(foodGlobal, key=lambda pos: (pos[0]-self.x)**2 + (pos[1]-self.y)**2)
        return closest 

    def moveTowarsds(self, target):
        target_x, target_y = target
        if self.x < target_x:
            self.x += 1
        elif self.x > target_x:
            self.x -= 1

        if self.y < target_y:
            self.y += 1
        elif self.y > target_y:
            self.y -= 1
        self.energy = max(self.energy - 1, 0)

    def eatFood(self, world, foodPos):
        food_x, food_y = foodPos
        if world[food_x, food_y] == 1:
            world[food_x, food_y] = 0  # Remove food from the world
            print(f"{self.name} ate food at ({food_x}, {food_y})")
        else:
            print("No food to eat at this position.")

        self.energy = min(self.energy + 10, self.energyCapacity)  # Gain energy

def main():
    
    averageAge = 0
    for i in range(10):  # Simulate for 1 organism
        Leo = Organism("Leo", "Lion", 5, np.random.randint(0, worldSize), np.random.randint(0, worldSize), 20, 50, 100)
        map = initMap()

        i=0
        while(i<100):
            closestFood = Leo.scanForFood(map)
            Leo.tick()
            if Leo.energy <= 0:
                print(f"{Leo.name} has run out of energy and died at age {Leo.age}.")
                averageAge += Leo.age
                break
            if closestFood:
                print(f"Nearest food at ({closestFood[0]}, {closestFood[1]})")
                print(f"Leo at ({Leo.x}, {Leo.y}) moving towards food...")
                Leo.moveTowarsds(closestFood)
                print(f"Leo moved to ({Leo.x}, {Leo.y})")
                if (Leo.x, Leo.y) == closestFood:
                    Leo.eatFood(map, closestFood)
                    
            else:
                dx, dy = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
                Leo.x = (Leo.x + dx) % worldSize
                Leo.y = (Leo.y + dy) % worldSize
                print("No food detected. Moving...")
                print(f"Leo moved to ({Leo.x}, {Leo.y})")
            i += 1
    
    print(f"Average age of organisms: {averageAge / 10}")


def initMap():
    map = np.zeros((worldSize, worldSize), dtype=int)
    num_points = (worldSize * worldSize) // 800  # approx 1 every 800 spaces

    # pick random coordinates
    xs = np.random.randint(0, worldSize, num_points)
    ys = np.random.randint(0, worldSize, num_points)

    map[xs, ys] = 1

    return map

if __name__ == "__main__":
    main()
            