import numpy as np
import matplotlib.pyplot as plt

# Load data from file
data = np.loadtxt('blackholeoutput.txt')

# Extract x and y values
x = data[:, 0]
y = data[:, 1]

# Create the plot
plt.figure(figsize=(8, 6))
plt.scatter(x, y)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Plot of data.txt')
plt.grid()

# Set the same scale for x and y axes
plt.axis('equal')

plt.show()