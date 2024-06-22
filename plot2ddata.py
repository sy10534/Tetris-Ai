import numpy as np
import matplotlib.pyplot as plt

# Load data from file
data = np.loadtxt('blackholeoutput.txt')

# Extract x, y, and color values
x = data[:, 0]
y = data[:, 1]
red = data[:, 2]
green = data[:, 3]
blue = data[:, 4]

# Combine the RGB values into a single 2D array
colors = np.column_stack((red, green, blue))

# Create the plot
plt.figure(figsize=(8, 6))
plt.scatter(x, y, c=colors)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Plot of data.txt')
plt.grid()

# Set the same scale for x and y axes
plt.axis('equal')

plt.show()