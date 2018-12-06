
#######################################################################################################################
# IMPORTS
#######################################################################################################################
import os

from utils import paths
from utils.helpers import Runner

#######################################################################################################################
# CONSTANTS
#######################################################################################################################
PARENT_FOLDER_NAME = "Day_6"
FILES_NAME = "io"
INPUT_FILE = "input.txt"
SAMPLE_FILE = "sample.txt"
OUTPUT_FILE = os.path.basename(__file__)[:-3] + "_output.txt"

SAMPLE_PATH = "/".join([paths.PROJECT_PATH, PARENT_FOLDER_NAME, FILES_NAME, SAMPLE_FILE])
INPUT_PATH = "/".join([paths.PROJECT_PATH, PARENT_FOLDER_NAME, FILES_NAME, INPUT_FILE])
OUTPUT_PATH = "/".join([paths.PROJECT_PATH, PARENT_FOLDER_NAME, FILES_NAME, OUTPUT_FILE])


#######################################################################################################################
# Root function
#######################################################################################################################
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_finite = True

    def dist(self, point):
        x_dist = abs(self.x - point.x)
        y_dist = abs(self.y - point.y)

        return x_dist + y_dist

    def check_finite(self, point):
        pass

    def __str__(self):
        return str(self.x) + " " + str(self.y)


def create_coords(data):
    coords = []

    for record in data:
        x, y = record.split(", ")
        coords.append(Point(int(x), int(y)))

    return coords


def determinte_finite_coords(coords):
    max_x, max_y =  0, 0
    for point in coords:
        if point.x > max_x:
            max_x = point.x
        if point.x > max_y:
            max_y = point.y

    print(max_x, max_y)



#######################################################################################################################
# Main function
#######################################################################################################################
def __main__():
    # BE SURE TO RENAME PARENT_FOLDER_NAME VARIABLE
    runner = Runner(SAMPLE_PATH, OUTPUT_PATH, debug=True)

    # Your code goes here
    coords = create_coords(runner.input_data)
    determinte_finite_coords(coords)

    runner.finish([])


#######################################################################################################################
# Process
#######################################################################################################################
if __name__ == "__main__":
    __main__()
