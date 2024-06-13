import matplotlib.pyplot as plt
import numpy as np
def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

timepoints = []
xpoints = []
ypoints = []
zpoints = []
data = open(r"C:\Users\user\Desktop\local code\Tetris-Ai\Tetris\data.txt",'r')
data = data.readlines()
data.pop(len(data)-1)
for _ in range(0,10):
    data.pop(0)
for i,v in enumerate(data):
    currentdata = v.split("\n")[0]
    time,x,y,z,r,t,p = map(float,currentdata.split(","))
    timepoints.append(time)
    xpoints.append(x)
    ypoints.append(y)
    zpoints.append(z)

    print("TIME BATCH:",i)
    print(z)
ax = plt.gca()
ax.ticklabel_format(useOffset=False)
plt.plot(timepoints, smooth(xpoints,10), color='r', label = 'x')
plt.plot(timepoints, smooth(ypoints,10), color='g', label = 'x')
plt.plot(timepoints, smooth(zpoints,10), color='b', label = 'z')
plt.xlabel("Time(seconds)")
plt.ylabel("Acceleration Magnitude(ms-2)")
plt.title("HKG(Hong Kong) To PK(Peking) Landing at 2023-07-29 16:03:40")
plt.legend("XYZ")
plt.xlim(0,200)#seconds
plt.ylim(0,50)#magnitude
plt.show()