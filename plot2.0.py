import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import juggle_axes

# Load data from a text file
data = np.loadtxt('3d_data.txt', delimiter=' ')
data2 = np.loadtxt('3d_data2.txt', delimiter=' ')

# Extract x, y, z coordinates from the data
x = data[:, 0]
y = data[:, 1]
z = [0]*len(y)
x2 = data2[:, 0]
y2 = data2[:, 1]
z2 = [0]*len(y2)
# Create a 3D figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the 3D scatter
ax.scatter(x, y, z, s = 15)
ax.scatter(x2, y2, z2, s = 25)

# Add a sphere at the origin with a radius of 0.5
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x_sphere = 0.5 * np.cos(u) * np.sin(v)
y_sphere = 0.5 * np.sin(u) * np.sin(v)
z_sphere = 0.5 * np.cos(v)
ax.plot_surface(x_sphere, y_sphere, z_sphere, color='r', alpha=0.3)
#set aspect
ax.set_aspect('equal')

# Add labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.title('Hohmann transfer orbit (earth to moon)')

plt.show()