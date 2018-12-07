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


def mark_infinite_points(matrix, coords_dict):
    infinite_points_id = set([])

    max_y = len(matrix[0]) - 1
    for x in range(len(matrix)):
        cell = matrix[x][0]
        if not cell == ".":
            infinite_points_id.add(cell)
        cell = matrix[x][max_y]
        if not cell == ".":
            infinite_points_id.add(cell)

    max_x = len(matrix) - 1
    for y in range(1, len(matrix[0]) - 1):
        cell = matrix[0][y]
        if not cell == ".":
            infinite_points_id.add(cell)
        cell = matrix[max_x][y]
        if not cell == ".":
            infinite_points_id.add(cell)

    for point_id in infinite_points_id:
        point = coords_dict[point_id]
        point.is_finite = False


def print_matrix(matrix):
    for y in range(len(matrix[0])):
        s = ""
        for x in range(len(matrix)):
            s += str(matrix[x][y])

        print(s)


def map_coords(coords, max_x, max_y):
    matrix = [["." for j in range(max_y)] for i in range(max_x)]

    for point in coords:
        matrix[point.x][point.y] = "X"

    return matrix


def get_closest_point(coords, x, y):
    closest_point_id = ""
    closest_point_distance = 9999
    distance_equal = False

    current_point = Point(-1, x, y)
    for point in coords:
        distance = point.dist(current_point)

        if distance < closest_point_distance:
            closest_point_distance = distance
            closest_point_id = point.id
            distance_equal = False
        elif distance == closest_point_distance:
            distance_equal = True

    if distance_equal:
        return "."
    else:
        return closest_point_id


def determine_largest_area(coords):
    max_x, max_y = get_boundaries(coords)

    matrix = map_coords(coords, max_x, max_y)

    coords_dict = {}
    for point in coords:
        coords_dict[str(point.id)] = point

    for y in range(len(matrix[0])):
        for x in range(len(matrix)):
            closest_point = get_closest_point(coords, x, y)
            if not closest_point == ".":
                point = coords_dict[str(closest_point)]
                point.increase_area()
                matrix[x][y] = closest_point
            else:
                matrix[x][y] = "."

    print_matrix(matrix)

    mark_infinite_points(matrix, coords_dict)

    largest_area = 0
    for point in coords:
        if point.is_finite:
            if point.area > largest_area:
                largest_area = point.area

    return largest_area


#######################################################################################################################
# Main function
#######################################################################################################################
def __main__():
    runner = Runner(INPUT_PATH, OUTPUT_PATH, debug=True)

    # Your code goes here
    coords = create_coords(runner.input_data)
    largest_area = determine_largest_area(coords)

    runner.finish([largest_area])


#######################################################################################################################
# Process
#######################################################################################################################
if __name__ == "__main__":
    __main__()
