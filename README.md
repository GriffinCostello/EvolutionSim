# Evolution Simulation

This is an agent-based simulation of organisms in a 2D world. Organisms have individual traits, move around the world, search for food, and interact with other organisms.

## Current Features
- Multiple organisms with customizable traits (speed, energy, vision, mating behavior).
- Organisms move randomly or toward the nearest food within their detection radius.
- Energy management: moving and actions consume energy; eating food restores energy.
- Organisms age over time and may slow down based on age.
- Food is randomly distributed in the world.
- Mating calls: organisms can detect nearby potential mates within a radius.
- Shared 2D world environment for all organisms using SimPy for concurrent simulation.
- Added reproduction functionality where organisms can create offspring with inherited traits.
- Food is regrown by animals eating and spreading seeds
- Carnivores can now be spawned in the simulation and carnivores can hunt herbivores for food.
- Herbivores attempt to escape Carnivores

## Future Plans
- Evolutionary dynamics and population growth.
- More complex behaviors: group hunting, competition, or territory defense.
- Environmental effects: seasonal food availability, hazards, or migration.
- Visualization of the simulation using graphical libraries.
- Add third plane of space for height

## How to Run
1. Install Python 3.8+.
2. Install dependencies:
   ```bash
   pip install numpy simpy matplotlib
3. Run the simulation:
   ```bash
   python run.py
   ```
4. Wait (for a few minutes) for the simulation to complete and view the results through Matplotlib visualizations

## How to Test
1. Install pytest:
   ```bash
   pip install pytest
   ```
2. Run the test suite:
   ```bash
   pytest -v
   ```
