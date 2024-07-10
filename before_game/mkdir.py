print("mkdir game")

print("cd game") # 0

print("mkdir 00")

print("cd 00") # 1

print("mkdir 00")

print("cd 00") # 2

for i in range(100):
    if(i < 10):
        print("mkdir 0"+str(i))
    else:
        print("mkdir "+str(i))

print("cd ..") # 1
        
for i in range (100):
    if(i < 10):
        print("cp -r 00 0"+str(i))
    else:
        print("cp -r 00 "+str(i))
        
print("cd ..") # 0

for i in range (100):
    if(i < 10):
        print("cp -r 00 0"+str(i))
    else:
        print("cp -r 00 "+str(i))