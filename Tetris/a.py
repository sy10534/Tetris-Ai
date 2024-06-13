n,x,y,z = map(int, input().split())

if((z>=y and z<=x) or (z <= y and z >= x)):
    print("Yes")
else:
    print("No")