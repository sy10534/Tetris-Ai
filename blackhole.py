import math
from decimal import Decimal
accretionDiskOuterRadius = 5.184*(10**9)
accretionDiskInnerRadius = 0
gravitationalConstant = 6.67430*(10**(-11))
massOfBlackHoleInSolarMass = 700000
speedoflight = 3*(10**8)
schwarzschildRadius = 2*gravitationalConstant*massOfBlackHoleInSolarMass*(1.989*10**30)/speedoflight/speedoflight/3

deltatime = 1
scale = 0.01

distanceFromBlackHole = accretionDiskOuterRadius*10
sx = -distanceFromBlackHole
sy = 1
sz = accretionDiskOuterRadius/5
resolution = 100

fieldOfView = 180/math.pi*2*math.atan(accretionDiskOuterRadius/distanceFromBlackHole)
print("Field of view:",fieldOfView)
screen = [[[0 for x in range(1)] for x in range(resolution)] for x in range(resolution)]
def deg(angle):
    return 180/math.pi*angle
def rad(angle):
    return math.pi/180*angle
def degrectify(angle):
    while(angle < 0):
        angle += 360
    while(angle > 360):
        angle -= 360
    return angle
def checkcollision(x,y,z,dx,dy,dz):
    xprime = x+dx
    yprime = y+dy
    zprime = z+dz
    crash = False
    visible = False

    dist = (xprime**2+yprime**2+zprime**2)**0.5
    # print(dist)

    if((z > 0 and zprime < 0) or (z < 0 and zprime > 0) or (z==0)):
        horizontaldist = (xprime**2+yprime**2)**0.5
        if(horizontaldist <= accretionDiskOuterRadius):
            # print("RING RING RING")
            crash = True
            visible = True
    if(dist <= schwarzschildRadius):
        visible = False
        crash = True

    return crash,visible
def getOriginPolar(x,y,z):
    horidist = (x*x+y*y)**0.5
    dec = deg(math.atan(z/horidist))
    ra = 0
    if(x>0 and y>0):
        ra = deg(math.atan(y/x))
    elif(x<0 and y>0):
        ra = 90+deg(math.atan(-x/y))
    elif(x<0 and y<0):
        ra = 180+deg(math.atan(-y/-x))
    elif(x>0 and y<0):
        ra = 270+deg(math.atan(x/-y))
    return ra,dec
def getBackOriginPolar(x,y,z):
    return getOriginPolar(-x,-y,-z)
def sn(bruh):
    return f"{Decimal(bruh):.2E}"
angleincrement = fieldOfView/resolution
anglera = 0
angledec = 0
iteration = 0
bruh = 0
for pixely in range(resolution):
    anglera = 0
    for pixelx in range(resolution):
        launchra = anglera-fieldOfView/2
        launchdec = angledec-fieldOfView/2
        pointra = degrectify(launchra)
        pointdec = launchdec
        localtime = 0
        raycast = False
        emitlight = False
        x = sx
        y = sy
        z = sz
        horiv = speedoflight*math.cos(rad(pointdec))
        vx = horiv*math.cos(rad(pointra))
        vy = horiv*math.sin(rad(pointra))
        vz = speedoflight*math.sin(rad(pointdec))
        # print(sn(vx),sn(vy),sn(vz), pointra, pointdec)
        while(raycast == False and localtime < accretionDiskOuterRadius*2/speedoflight*10):
            
            dist = (x**2+y**2+z**2)**0.5
            acceleration = gravitationalConstant*massOfBlackHoleInSolarMass*(1.989*(10**30))/(dist**2)
            #unit direction
            originra,origindec = getBackOriginPolar(x,y,z)
            #acceleration
            horia = acceleration*math.cos(rad(origindec))
            ax = horia*math.cos(rad(originra))*deltatime
            ay = horia*math.sin(rad(originra))*deltatime
            az = acceleration*math.sin(rad(origindec))*deltatime
            #new velocity
            vx += ax
            vy += ay
            vz += az
            #unitvector
            pointra,pointdec = getOriginPolar(vx,vy,vz)
            horiv = speedoflight*math.cos(rad(pointdec))
            vx = horiv*math.cos(rad(pointra))
            vy = horiv*math.sin(rad(pointra))
            vz = speedoflight*math.sin(rad(pointdec))
            getcrash,getvisible = checkcollision(x,y,z,vx*deltatime,vy*deltatime,vz*deltatime)
            raycast = getcrash
            emitlight = getvisible
            x += vx*deltatime
            y += vy*deltatime
            z += vz*deltatime
            # if(pixely%10 == 0 and pixelx == 0 and localtime%50 == 0):
            #     print(pointra,pointdec)
            #     print("")
                # print(sn(dist), sn(schwarzschildRadius),sn(x),sn(y),sn(z),sn(vx),sn(vy),sn(vz),sn(ax),sn(ay),sn(az))
                # print("")
                # print("")

            localtime += deltatime
        iteration += 1
        bruh += 1
        if(emitlight == True):
            bruh = 0
            screen[pixely][pixelx] = 1
        anglera+=angleincrement
        print(iteration/resolution/resolution*100,'%', "finished")
    if(bruh > 100 and pixely/resolution*100 > 30):
        break
    # if(pixely%10 == 0):
    angledec+=angleincrement
    


with open("blackholeoutput.txt", 'w') as file:
    for i in range(resolution):
        for y in range(resolution):
            if(screen[i][y] == 1):
                file.write(str(y)+" "+str(i)+"\n")