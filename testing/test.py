import numpy as np
from matplotlib import pyplot as plt

population = ["obj1", "obj2", "obj3", "banana!", "bob"]  # Replace obj1, obj2, obj3 with your actual objects
fitness_array = [1, 0.7, 0.9, 7, 0.2]

# Sort the objects array based on the scores (in descending order)

population = sorted(population, key=lambda obj: fitness_array[population.index(obj)], reverse=True)

# Now, sorted_objects_array contains the objects sorted based on the scores
print(population)
total_array = [1, 1, 1, 1, 1, 1, 4, 5, 5, 6]
time_steps = np.arange(1, len(total_array)+1)
plt.plot(time_steps, np.array(total_array))
plt.show()
print("LOL")