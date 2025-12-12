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


## Future Plans
- Reproduction with genetic variation.
- Evolutionary dynamics and population growth.
- More complex behaviors: group hunting, competition, or territory defense.
- Environmental effects: seasonal food availability, hazards, or migration.
- Visualization of the simulation using graphical libraries.

## How to Run
1. Install Python 3.8+.
2. Install dependencies:
   ```bash
   pip install numpy simpy
