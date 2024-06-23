# blackhole_simulation.pyx

import math
from decimal import Decimal
import numpy as np
from libc.math cimport atan, pi, cos, sin, log
from PIL import Image
cimport numpy as np
import numpy as np
cdef double accretionDiskOuterRadius = 5.184 * (10 ** 9)
cdef double gravitationalConstant = 6.67430 * (10 ** (-11))
cdef double massOfBlackHoleInSolarMass = 700000/2
cdef double speedoflight = 3 * (10 ** 8)
cdef double schwarzschildRadius = 2 * gravitationalConstant * massOfBlackHoleInSolarMass * (1.989 * 10**30) / speedoflight / speedoflight / 2
cdef double accretionDiskInnerRadius = 5.184 * (10 ** 9)/5

cdef double deltatime = 0.2
cdef double scale = 0.01

cdef double sx = -accretionDiskOuterRadius*6
cdef double sy = 1
cdef double sz = accretionDiskOuterRadius
cdef double distanceFromBlackHole = (sx*sx+sz*sz)**0.5
cdef int resolution = 1600

cdef list maxbrightness = [255 / 255, 100 / 255, 0]
cdef list minbrightness = [0, 0, 0]
cdef list screen = [[[0 for x in range(1)] for x in range(resolution)] for x in range(resolution)]
cdef list screencolour = [[[0 for x in range(3)] for x in range(resolution)] for x in range(resolution)]

#cdef double fieldOfView = 180 / pi * 2 * atan(accretionDiskOuterRadius / distanceFromBlackHole)+30
cdef double fieldOfView = 60
print("Field of view:", fieldOfView)

cdef double deg(double angle):
    return 180 / pi * angle

cdef double rad(double angle):
    return pi / 180 * angle

cdef double degrectify(double angle):
    while angle < 0:
        angle += 360
    while angle > 360:
        angle -= 360
    return angle

cdef double clamp(double num, double minn, double maxx):
    return min(max(minn, num), maxx)

cdef tuple checkcollision(double x, double y, double z, double dx, double dy, double dz):
    cdef double xprime = x + dx
    cdef double yprime = y + dy
    cdef double zprime = z + dz
    cdef bint crash = False
    cdef bint visible = False
    cdef double horizontaldist = (xprime ** 2 + yprime ** 2) ** 0.5
    cdef double dist = (xprime ** 2 + yprime ** 2 + zprime ** 2) ** 0.5

    #if ((z > 0 and zprime < 0) or (z < 0 and zprime > 0) or (z == 0)):
    #    if horizontaldist <= accretionDiskOuterRadius and horizontaldist >= accretionDiskInnerRadius:
    #        crash = True
    #        visible = True
    if dist <= schwarzschildRadius:
        visible = False
        crash = True

    return crash, visible

cdef tuple getOriginPolar(double x, double y, double z):
    cdef double horidist = (x * x + y * y) ** 0.5
    cdef double dec = deg(atan(z / horidist))
    cdef double ra = 0
    if x > 0 and y > 0:
        ra = deg(atan(y / x))
    elif x < 0 and y > 0:
        ra = 90 + deg(atan(-x / y))
    elif x < 0 and y < 0:
        ra = 180 + deg(atan(-y / -x))
    elif x > 0 and y < 0:
        ra = 270 + deg(atan(x / -y))
    return ra, dec

cdef tuple getBackOriginPolar(double x, double y, double z):
    return getOriginPolar(-x, -y, -z)


cdef list get_image_data():
    # Open the image using Pillow
    image = Image.open(r"C:\Users\user\Desktop\local code\Tetris-Ai\galaxy.jpg")
    
    # Convert the image to RGB if it is not already in that mode
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Get the size of the image
    width, height = image.size
    
    # Load the image data
    cdef np.ndarray[np.uint8_t, ndim=3] data = np.asarray(image)
    
    # Create an empty list to hold the pixel data
    cdef list pixel_data = []
    
    # Iterate through each pixel and store the color data
    cdef int x, y
    for y in range(height):
        for x in range(width):
            r = data[y, x, 0]
            g = data[y, x, 1]
            b = data[y, x, 2]
            # Store the data as a flat list of tuples
            pixel_data.append((r, g, b))
    
    return pixel_data
cdef tuple get_pixel_color_at_polar(double ra, double dec):
    cdef double x, y
    cdef int px, py
    x = degrectify(ra+180) / 360 * image_width
    y = (dec+90) / 180 * image_height


    px = <int>x
    py = <int>y

    px = max(0, min(px, image_width - 1))
    py = max(0, min(py, image_height - 1))

    # Access the pixel color using nested indexing
    r, g, b = pixel_colors[py * image_width + px]
    return r, g, b
cdef int image_width = 6000
cdef int image_height = 3000
cdef list pixel_colors = get_image_data()
cdef double angleincrement = fieldOfView / resolution
cdef double anglera = 0
cdef double angledec = deg(atan(sz/sx))
#cdef double angledec = -70
cdef int iteration = 0
cdef int bruh = 0
cdef double localtime = 0
cdef bint raycast = False
cdef bint emitlight = False
cdef double x = 0
cdef double y = 0
cdef double z = 0
cdef double dist = 0
cdef double horidist = 0
cdef double horiv = 0
cdef double vx = 0
cdef double vy = 0
cdef double vz = 0
cdef double acceleration = 0
cdef tuple originra_origindec = getBackOriginPolar(1, 1, 1)
cdef double originra = 0
cdef double origindec = 0
cdef double horia = 0
cdef double ax = 0
cdef double ay = 0
cdef double az = 0
cdef tuple pointra_pointdec = getOriginPolar(1, 1, 1)
cdef tuple getcrash_getvisible = checkcollision(1, 1, 1, 1 * 1, 1 * 1, 1 * 1)
cdef bint getcrash = False
cdef bint getvisible = False
cdef tuple nice = get_pixel_color_at_polar((getOriginPolar(1, 1, 1))[0],1)
for pixely in range(resolution):
    anglera = 0
    for pixelx in range(resolution):
        launchra = anglera - fieldOfView / 2
        launchdec = angledec - fieldOfView / 2
        pointra = degrectify(launchra)
        pointdec = launchdec
        localtime = 0
        raycast = False
        emitlight = False
        x = sx
        z = sz
        dist = (x ** 2 + y ** 2 + z ** 2) ** 0.5
        horidist = (x * x + y * y) ** 0.5
        horiv = speedoflight * cos(rad(pointdec))
        vx = horiv * cos(rad(pointra))
        vy = horiv * sin(rad(pointra))
        vz = speedoflight * sin(rad(pointdec))
        y = sy
        
        while raycast == False and localtime < accretionDiskOuterRadius * 2 / speedoflight * 10:
            dist = (x ** 2 + y ** 2 + z ** 2) ** 0.5
            horidist = (x * x + y * y) ** 0.5
            acceleration = gravitationalConstant * massOfBlackHoleInSolarMass * (1.989 * (10 ** 30)) / (dist ** 2)
            originra_origindec = getBackOriginPolar(x, y, z)
            originra = originra_origindec[0]
            origindec = originra_origindec[1]
            horia = acceleration * cos(rad(origindec))
            ax = horia * cos(rad(originra)) * deltatime
            ay = horia * sin(rad(originra)) * deltatime
            az = acceleration * sin(rad(origindec)) * deltatime

            vx += ax
            vy += ay
            vz += az

            pointra_pointdec = getOriginPolar(vx, vy, vz)
            pointra = pointra_pointdec[0]
            pointdec = pointra_pointdec[1]
            horiv = speedoflight * cos(rad(pointdec))
            vx = horiv * cos(rad(pointra))
            vy = horiv * sin(rad(pointra))
            vz = speedoflight * sin(rad(pointdec))

            getcrash_getvisible = checkcollision(x, y, z, vx * deltatime, vy * deltatime, vz * deltatime)
            getcrash = getcrash_getvisible[0]
            getvisible = getcrash_getvisible[1]
            raycast = getcrash
            emitlight = getvisible

            x += vx * deltatime
            y += vy * deltatime
            z += vz * deltatime

            localtime += deltatime
        
        iteration += 1
        bruh += 1
            #screencolour[pixely][pixelx][0] = clamp((maxbrightness[0] - minbrightness[0]) * ((accretionDiskOuterRadius - horidist) / (accretionDiskOuterRadius - schwarzschildRadius)), 0, 1)
            #screencolour[pixely][pixelx][1] = clamp((maxbrightness[1] - minbrightness[1]) * ((accretionDiskOuterRadius - horidist) / (accretionDiskOuterRadius - schwarzschildRadius)), 0, 1)
            #screencolour[pixely][pixelx][2] = clamp((maxbrightness[2] - minbrightness[2]) * ((accretionDiskOuterRadius - horidist) / (accretionDiskOuterRadius - schwarzschildRadius)), 0, 1)
        if not emitlight and raycast:
            bruh = 0
            screen[pixely][pixelx] = 1
            screencolour[pixely][pixelx][0] = 0
            screencolour[pixely][pixelx][1] = 0
            screencolour[pixely][pixelx][2] = 0
        else:
            bruh = 0
            screen[pixely][pixelx] = 1
            nice = get_pixel_color_at_polar(getOriginPolar(vx, vy, vz)[0],getOriginPolar(vx, vy, vz)[1])
            screencolour[pixely][pixelx][0] = nice[0]
            screencolour[pixely][pixelx][1] = nice[1]
            screencolour[pixely][pixelx][2] = nice[2]

        anglera += angleincrement
    angledec += angleincrement
    print(pixely/resolution*100, "% finished")

# Output the screen matrix and color data for verification
#for pixely in range(resolution):
#    for pixelx in range(resolution):
#        print(pixelx, pixely, screen[pixely][pixelx], screencolour[pixely][pixelx],"~")
with open("blackholeoutput.txt", 'w') as file:
    for pixely in range(resolution):
        for pixelx in range(resolution):
            if(screen[pixely][pixelx] == 1):
                file.write(f"{pixelx} {pixely} {screencolour[pixely][pixelx][0]} {screencolour[pixely][pixelx][1]} {screencolour[pixely][pixelx][2]}\n")