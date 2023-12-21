import gui
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import random

app = gui.App()
app.root.mainloop()

# Set up the initial grid
grid_size = 100
grid = np.zeros((grid_size, grid_size))

# Set up the initial number of predators and prey
num_predators = app.predator_value  # 20
num_prey = app.prey_value  # 25

# Set up the reproduction rates
predator_reproduction_rate = app.predator_repro  # 0.04
prey_reproduction_rate = app.prey_repro  # 0.038

# Set death rates
predator_death_rate = app.predator_death  # 0.03
prey_death_rate = app.prey_death  # 0.03

# Set the size of each grid cell
cell_size = 10


# Class definition for predators
class Predator:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.num_consumed = 0  # Initialize the number of prey consumed to 0

    def move(self, grid, predators, prey):
        # Find the nearby prey
        nearby_prey = get_nearby_individuals(self.x, self.y, prey)

        if len(nearby_prey) > 0:
            closest_prey_index = np.argmin(
                distance(self.x, self.y, nearby_prey[:, 0], nearby_prey[:, 1])
            )
            closest_prey = nearby_prey[closest_prey_index]

            dx = np.sign(closest_prey[0] - self.x)
            dy = np.sign(closest_prey[1] - self.y)

            # Increment the number of prey consumed
            self.num_consumed += 1
        else:
            dx = 0
            dy = 0

        target_x = (self.x + dx) % grid_size
        target_y = (self.y + dy) % grid_size

        if grid[target_x, target_y] != 0:
            choices = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            random.shuffle(choices)
            for choice in choices:
                dx, dy = choice
                new_x = (self.x + dx) % grid_size
                new_y = (self.y + dy) % grid_size
                if grid[new_x, new_y] == 0:
                    target_x = new_x
                    target_y = new_y
                    break

        grid[self.x, self.y] = 0
        grid[target_x, target_y] = 2
        self.x = target_x
        self.y = target_y


# Class definition for prey
class Prey:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, grid, predators):
        nearby_predators = get_nearby_individuals(self.x, self.y, predators)

        if len(nearby_predators) > 0:
            closest_predator_index = np.argmin(
                distance(self.x, self.y, nearby_predators[:, 0], nearby_predators[:, 1])
            )
            closest_predator = nearby_predators[closest_predator_index]

            dx = np.sign(self.x - closest_predator[0])
            dy = np.sign(self.y - closest_predator[1])
        else:
            dx = 0
            dy = 0

        random_dx = np.random.randint(-1, 2)
        random_dy = np.random.randint(-1, 2)
        new_x = self.x + dx + random_dx
        new_y = self.y + dy + random_dy

        if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
            if grid[new_x, new_y] == 1:
                self.x, self.y = self.x, self.y
            else:
                grid[self.x, self.y] = 0
                grid[new_x, new_y] = 1
                self.x, self.y = new_x, new_y

        if (self.x, self.y) in [(predator.x, predator.y) for predator in predators]:
            return True  # Prey is eaten

        return False


# Set up the initial predators and prey
predators = [Predator(x, y) for x, y in zip(np.random.choice(range(grid_size), size=num_predators),
                                            np.random.choice(range(grid_size), size=num_predators))]
prey = [Prey(x, y) for x, y in zip(np.random.choice(range(grid_size), size=num_prey),
                                   np.random.choice(range(grid_size), size=num_prey))]

# Set up the plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
plt.subplots_adjust(hspace=0.5)

# Initialize the grid plot
grid_plot = ax1.imshow(grid, cmap="binary", vmin=0, vmax=2)

# Initialize the line plots for predator and prey populations
time_steps = []
predator_counts = []
prey_counts = []
predator_line, = ax2.plot(time_steps, predator_counts, label='Predators')
prey_line, = ax2.plot(time_steps, prey_counts, label='Prey')
ax2.legend()


# Function to calculate Euclidean distance between two points using Pythagoras
def distance(x1, y1, x2, y2):
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


# Works out the nearest individual within a set range
def get_nearby_individuals(x, y, individuals):
    cell_x = int(x // cell_size)
    cell_y = int(y // cell_size)

    nearby_individuals = []
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            neighbor_x = cell_x + dx
            neighbor_y = cell_y + dy

            if (
                    0 <= neighbor_x < grid_size // cell_size
                    and 0 <= neighbor_y < grid_size // cell_size
            ):
                cell_individuals = [
                    (ind.x, ind.y) for ind in individuals
                    if ind.x // cell_size == neighbor_x
                       and ind.y // cell_size == neighbor_y
                ]
                nearby_individuals.extend(cell_individuals)

    return np.array(nearby_individuals)


# Loop over each time step
for t in range(1000):
    # Plot the current grid
    grid_plot.set_data(grid)

    reproduced_predators = []
    reproduced_prey = []
    eaten_prey = []  # Initialize the eaten prey list

    # Update the positions of the predators
    for predator in predators:
        predator.move(grid, predators, prey)

        # Predator reproduction based on prey consumption
        if predator.num_consumed > 0 and np.random.random() < predator_reproduction_rate:
            reproduced_predators.append(Predator(predator.x, predator.y))

        # Predator death
        if np.random.random() < predator_death_rate or predator.num_consumed == 0:
            grid[predator.x, predator.y] = 0
            predators.remove(predator)

    # Update the positions of the prey
    for i, p in enumerate(prey):
        if p.move(grid, predators):
            eaten_prey.append(i)

        # Prey reproduction
        if np.random.random() < prey_reproduction_rate:
            reproduced_prey.append(Prey(p.x, p.y))

        # Prey death
        if np.random.random() < prey_death_rate:
            eaten_prey.append(i)

    # Remove the eaten prey from the prey list and update the grid
    eaten_prey = sorted(set(eaten_prey))  # Remove duplicate indices and sort in ascending order
    for i in eaten_prey:
        if i < len(prey):  # Check if the index is valid
            p = prey[i]
            grid[p.x, p.y] = 0
            del prey[i]

    num_predators = len(predators)  # Update the predator count
    num_prey = len(prey)  # Update the prey count

    # Add the reproduced predators and prey
    predators.extend(reproduced_predators)
    prey.extend(reproduced_prey)

    # Update the predator and prey counts
    predator_counts.append(num_predators)
    prey_counts.append(num_prey)
    time_steps.append(t)

    # Update the plots
    predator_line.set_data(time_steps, predator_counts)
    prey_line.set_data(time_steps, prey_counts)

    # Adjust the plot limits if necessary
    ax2.set_xlim(0, t)
    ax2.set_ylim(0, max(max(predator_counts), max(prey_counts)) * 1.1)

    plt.pause(0.1)

plt.show()
