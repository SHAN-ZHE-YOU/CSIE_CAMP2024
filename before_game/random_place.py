import random

for i in range(8):
    print(f'mv {i+1}.png {random.randint(10, 50)}/{random.randint(10, 99)}/{random.randint(10, 99)}')