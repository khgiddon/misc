
# https://fivethirtyeight.com/features/can-you-zoom-around-the-race-track/
# Just having fun some here plotting valid sequences!

import random
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# Global constants
x_max, y_max, x_min, y_min = [7,7,-7,-7]

"""
Checks for valid coordinates
"""
def check_coordinate_is_valid(proposed_coordinate,prev_coords):
    return True if all([check_coordinate_in_bounds(proposed_coordinate),
                        check_coordinate_not_in_circle(proposed_coordinate),
                        check_coordinate_does_not_cross_bar(proposed_coordinate,prev_coords),
                        check_coordinate_not_visited(proposed_coordinate,prev_coords)]) else False

def check_coordinate_in_bounds(proposed_coordinate):
        x,y = proposed_coordinate[0], proposed_coordinate[1]
        return True if x >= x_min and x <= x_max and y >= y_min and y <= y_max else False

def check_coordinate_not_visited(proposed_coordinate,prev_coords):
    if proposed_coordinate not in prev_coords:
        return True
    elif proposed_coordinate == [0,-5] and prev_coords[-1][0] < 0: # Can revisit the starting point
        return True
    else:
        return False

def check_coordinate_not_in_circle(proposed_coordinate):
    x,y = proposed_coordinate[0], proposed_coordinate[1]
    r = 3
    return x**2 + y**2 > r**2

def check_coordinate_does_not_cross_bar(proposed_coordinate,prev_coords):
    #can cross from the left but not the right 
    x,y = proposed_coordinate[0], proposed_coordinate[1]
    return False if prev_coords[-1][0] >= 0 and prev_coords[-1][1] <= -3 and x < 0 else True

def new_coords(x,y,prev_x,prev_y,prev_coords):
    center_x, center_y = [x + x - prev_x, y + y - prev_y]
    proposed_coordinates = []
    for x_delta in range(-1,2):
        for y_delta in range(-1,2):
            proposed_coordinates.append([center_x + x_delta, center_y + y_delta])
    valid_coords = [coord for coord in proposed_coordinates if check_coordinate_is_valid(coord,prev_coords)]
    if len(valid_coords) == 0:
        pass
    else:
        if [0,-5] in valid_coords:
            new_coords = [0,-5]
        else: 
            new_coords = random.choice(valid_coords)
        prev_x, prev_y = [x,y]
        return [new_coords[0], new_coords[1], prev_x, prev_y]

def generate_seq():
    x = 0
    y = -5
    prev_x = 0
    prev_y = -5
    prev_coords = [[0,-5]]

    while True:
        if (result := new_coords(x,y,prev_x,prev_y,prev_coords)) is not None:
            x,y,prev_x,prev_y = result
            prev_coords.append([x,y])
            if [x,y] == [0,-5]:
                break
        else:
            break

    return prev_coords

# Temporary stopping function
while True:
    s = generate_seq()
    if s[-1] == [0,-5] and len(s) < 20:
        break

print(len(s))

xs, ys = zip(*s)

# Set up charts
fig, ax = plt.subplots()
ax.xaxis.set_major_locator(MultipleLocator(1))
ax.yaxis.set_major_locator(MultipleLocator(1))
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.grid(which='both',color='#CCCCCC', linestyle='--')
fig.set_size_inches(18.5, 10.5)

# Or if you want different settings for the grids:

# Embellishments
circle1 = plt.Circle((0, 0), 3, color='black')
circle2 = plt.Circle((0, -5), 0.3, color='red')
ax.plot([0,0],[0,-7],color='black')

ax.add_patch(circle1)
ax.add_patch(circle2)

# Plot sequence
ax.plot(xs,ys,marker='o',markersize='8')
ax.set_xlim((x_min-1, x_max+1))
ax.set_ylim((y_min-1, y_max+1))


