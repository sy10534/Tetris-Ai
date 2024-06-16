s = str(input())
t = str(input())
dp = 0
for i in range(len(s)):
    while(s[i]!=t[dp]):
        dp+=1
    print(dp+1, end=" ")
    dp+=1