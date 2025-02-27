import random
import time

MOVEMENT = [-1, 1]

def main():
    input_sizes = [20, 200, 2000, 20000, 2000000]
    times_3d = []
    pct_one = []
    pct_two = []
    pct_three = []
    
    for n in input_sizes:
        pct_one.append(one_dimension(n))
        pct_two.append(two_dimensions(n))
        
        start_time = time.time()
        pct_three.append(three_dimensions(n))
        times_3d.append(time.time() - start_time)
    
    
    print(f'Percentages of time particle returned to origin:\n'
          f'Number of steps: {20:>5,} {200:>7,} {2000:>9,} {20000:>8,} {200000:>8,}'
          f'\n1D:               {pct_one[0]:>5} {pct_one[1]:>7} {pct_one[2]:>7} {pct_one[3]:>7} {pct_one[4]:>7}'
          f'\n2D:               {pct_two[0]:>5} {pct_two[1]:>7} {pct_two[2]:>7} {pct_two[3]:>7} {pct_two[4]:>7}'
          f'\n3D:               {pct_three[0]:>5} {pct_three[1]:>7} {pct_three[2]:>7} {pct_three[3]:>7} {pct_three[4]:>7}\n'
          f'Run time (seconds):\n'
          f'Number of steps: {20:>5,} {200:>7,} {2000:>9,} {20000:>8,} {200000:>8,}'
          f'\n3D:              {times_3d[0]:>5.0} {times_3d[1]:>7.3} {times_3d[2]:>9.3} {times_3d[3]:>8.3} {times_3d[4]:>8.3}')

def one_dimension(steps):
    probability_data = []
    for i in range(100):
        total = 0
        for j in range(steps):
            step = random.choice(MOVEMENT)
            total += step
            if total == 0:
                probability_data.append(1)
                break
    percentage = f'{sum(probability_data)}%'
    return percentage

def two_dimensions(steps):
    probability_data = []
    for i in range(100):
        x, y = 0, 0
        for j in range(steps):
            if random.choice([x,y]) == x:
                x += random.choice(MOVEMENT)
            else:
                y += random.choice(MOVEMENT)
            if x == 0 and y == 0:
                probability_data.append(1)
                break
    percentage = f'{sum(probability_data)}%'
    return percentage

def three_dimensions(steps):
    probability_data = []
    for i in range(100):
        x, y, z = 0, 0, 0
        for j in range(steps):
            random_var = random.choice([x,y,z])
            if random_var == x:
                x += random.choice(MOVEMENT)
            elif random_var == y:
                y += random.choice(MOVEMENT)
            else:
                z += random.choice(MOVEMENT)
            if x == 0 and y == 0 and z == 0:
                probability_data.append(1)
                break
    percentage = f'{sum(probability_data)}%'
    return percentage

main()