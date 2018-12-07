# --- Day 6: Chronal Coordinates ---
# The device on your wrist beeps several times, and once again you feel like you're falling.
#
# "Situation critical," the device announces. "Destination indeterminate. Chronal interference detected. Please specify
# new target coordinates."
#
# The device then produces a list of coordinates (your puzzle input). Are they places it thinks are safe or dangerous?
# It recommends you check manual page 729. The Elves did not give you a manual.
#
# If they're dangerous, maybe you can minimize the danger by finding the coordinate that gives the largest distance
# from the other points.
#
# Using only the Manhattan distance, determine the area around each coordinate by counting the number of integer X,Y
# locations that are closest to that coordinate (and aren't tied in distance to any other coordinate).
#
# Your goal is to find the size of the largest area that isn't infinite. For example, consider the following list of
# coordinates:
#
# 1, 1
# 1, 6
# 8, 3
# 3, 4
# 5, 5
# 8, 9
#
# If we name these coordinates A through F, we can draw them on a grid, putting 0,0 at the top left:
#
# ..........
# .A........
# ..........
# ........C.
# ...D......
# .....E....
# .B........
# ..........
# ..........
# ........F.
# This view is partial - the actual grid extends infinitely in all directions. Using the Manhattan distance, each
# location's closest coordinate can be determined, shown here in lowercase:
#
# aaaaa.cccc
# aAaaa.cccc
# aaaddecccc
# aadddeccCc
# ..dDdeeccc
# bb.deEeecc
# bBb.eeee..
# bbb.eeefff
# bbb.eeffff
# bbb.ffffFf
# Locations shown as . are equally far from two or more coordinates, and so they don't count as being closest to any.
#
# In this example, the areas of coordinates A, B, C, and F are infinite - while not shown here, their areas extend
# forever outside the visible grid. However, the areas of coordinates D and E are finite: D is closest to 9 locations,
# and E is closest to 17 (both including the coordinate's location itself). Therefore, in this example, the size of the
# largest area is 17.
#
# What is the size of the largest area that isn't infinite?
#
# Your puzzle answer was 4011.
#
# The first half of this puzzle is complete! It provides one gold star: *
#
# --- Part Two ---
# On the other hand, if the coordinates are safe, maybe the best you can do is try to find a region near as many
# coordinates as possible.
#
# For example, suppose you want the sum of the Manhattan distance to all of the coordinates to be less than 32.
# For each location, add up the distances to all of the given coordinates; if the total of those distances is less
# than 32, that location is within the desired region. Using the same coordinates as above, the resulting region
# looks like this:
#
# ..........
# .A........
# ..........
# ...###..C.
# ..#D###...
# ..###E#...
# .B.###....
# ..........
# ..........
# ........F.
# In particular, consider the highlighted location 4,3 located at the top middle of the region. Its calculation
# is as follows, where abs() is the absolute value function:
#
# - Distance to coordinate A: abs(4-1) + abs(3-1) =  5
# - Distance to coordinate B: abs(4-1) + abs(3-6) =  6
# - Distance to coordinate C: abs(4-8) + abs(3-3) =  4
# - Distance to coordinate D: abs(4-3) + abs(3-4) =  2
# - Distance to coordinate E: abs(4-5) + abs(3-5) =  3
# - Distance to coordinate F: abs(4-8) + abs(3-9) = 10
# - Total distance: 5 + 6 + 4 + 2 + 3 + 10 = 30
#
# Because the total distance to all coordinates (30) is less than 32, the location is within the region.
#
# This region, which also includes coordinates D and E, has a total size of 16.
#
# Your actual region will need to be much larger than this example, though, instead including all locations with a
# total distance of less than 10000.
#
# What is the size of the region containing all locations which have a total distance to all given coordinates of
# less than 10000?

#######################################################################################################################
# IMPORTS
#######################################################################################################################
from utils.paths import SAMPLE_PATH, INPUT_PATH, OUTPUT_PATH
from utils.helpers import Runner

#######################################################################################################################
# CONSTANTS
#######################################################################################################################


#######################################################################################################################
# Root function
#######################################################################################################################
class Point:
    def __init__(self, point_id, x, y):
        self.id = point_id
        self.x = x
        self.y = y
        self.is_finite = True

        self.area = 0

    def dist(self, point):
        x_dist = abs(self.x - point.x)
        y_dist = abs(self.y - point.y)

        return x_dist + y_dist

    def increase_area(self):
        self.area += 1

    def __str__(self):
        return str(self.x) + " " + str(self.y)


def create_coords(data):
    coords = []

    point_id = 0
    id_list = "abcdefghijklmnopqrstuvwxyz"
    id_list += id_list.upper()
    for record in data:
        x, y = record.split(", ")
        coords.append(Point(id_list[point_id], int(x), int(y)))
        point_id += 1

    return coords


def get_boundaries(coords):
    max_x, max_y = 0, 0
    for point in coords:
        if point.x > max_x:
            max_x = point.x
        if point.x > max_y:
            max_y = point.y

    return [max_x + 1, max_y + 1]


def get_distance_sum(coords, x, y):
    distance_sum = 0

    current_point = Point(-1, x, y)
    for point in coords:
        distance = point.dist(current_point)

        distance_sum += distance

    return distance_sum


def determine_largest_area_withing_distance_sum(coords, distance_sum_limit):
    area = 0

    max_x, max_y = get_boundaries(coords)

    for y in range(max_y):
        for x in range(max_x):
            distance_sum = get_distance_sum(coords, x, y)

            if distance_sum < distance_sum_limit:
                area += 1

    return area


#######################################################################################################################
# Main function
#######################################################################################################################
def __main__():
    runner = Runner(INPUT_PATH, OUTPUT_PATH, debug=True)

    # Your code goes here
    coords = create_coords(runner.input_data)

    distance_sum = 10000
    largest_area = determine_largest_area_withing_distance_sum(coords, distance_sum)

    runner.finish([largest_area])


#######################################################################################################################
# Process
#######################################################################################################################
if __name__ == "__main__":
    __main__()