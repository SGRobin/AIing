import numpy as np

x = np.linspace(0 ,1 ,100)
directions = [(d / 5) - 0.1 for d in x]
print(directions)