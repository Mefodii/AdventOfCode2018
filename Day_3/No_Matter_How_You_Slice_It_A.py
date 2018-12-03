# --- Day 3: No Matter How You Slice It ---
# The Elves managed to locate the chimney-squeeze prototype fabric for Santa's suit (thanks to someone who helpfully
# wrote its box IDs on the wall of the warehouse in the middle of the night). Unfortunately, anomalies are still
# affecting them - nobody can even agree on how to cut the fabric.
#
# The whole piece of fabric they're working on is a very large square - at least 1000 inches on each side.
#
# Each Elf has made a claim about which area of fabric would be ideal for Santa's suit. All claims have an ID and
# consist of a single rectangle with edges parallel to the edges of the fabric. Each claim's rectangle is defined as
# follows:
#
# - The number of inches between the left edge of the fabric and the left edge of the rectangle.
# - The number of inches between the top edge of the fabric and the top edge of the rectangle.
# - The width of the rectangle in inches.
# - The height of the rectangle in inches.
#
# A claim like #123 @ 3,2: 5x4 means that claim ID 123 specifies a rectangle 3 inches from the left edge, 2 inches from
# the top edge, 5 inches wide, and 4 inches tall. Visually, it claims the square inches of fabric represented by #
# (and ignores the square inches of fabric represented by .) in the diagram below:
#
# ...........
# ...........
# ...#####...
# ...#####...
# ...#####...
# ...#####...
# ...........
# ...........
# ...........
#
# The problem is that many of the claims overlap, causing two or more claims to cover part of the same areas.
# For example, consider the following claims:
#
# #1 @ 1,3: 4x4
# #2 @ 3,1: 4x4
# #3 @ 5,5: 2x2
#
# Visually, these claim the following areas:
#
# ........
# ...2222.
# ...2222.
# .11XX22.
# .11XX22.
# .111133.
# .111133.
# ........
# The four square inches marked with X are claimed by both 1 and 2. (Claim 3, while adjacent to the others, does not
# overlap either of them.)
#
# If the Elves all proceed with their own plans, none of them will have enough fabric. How many square inches of fabric
# are within two or more claims?

#######################################################################################################################
# IMPORTS
#######################################################################################################################
import os

from utils import paths
from utils.helpers import Runner

#######################################################################################################################
# CONSTANTS
#######################################################################################################################
PARENT_FOLDER_NAME = "Day_3"
FILES_NAME = "io"
INPUT_FILE = "input.txt"
OUTPUT_FILE = os.path.basename(__file__)[:-3] + "_output.txt"

INPUT_PATH = "/".join([paths.PROJECT_PATH, PARENT_FOLDER_NAME, FILES_NAME, INPUT_FILE])
OUTPUT_PATH = "/".join([paths.PROJECT_PATH, PARENT_FOLDER_NAME, FILES_NAME, OUTPUT_FILE])


#######################################################################################################################
# Root function
#######################################################################################################################
class Claim:
    def __init__(self, id_nr, cut_left, cut_top, width, height):
        self.id = id_nr
        self.cut_left = cut_left
        self.cut_top = cut_top
        self.width = width
        self.height = height

        self.start_x = cut_left
        self.end_x = cut_left + width - 1

        self.start_y = cut_top
        self.end_y = cut_top + height - 1

    def is_overlap(self, claim):
        if self.start_x <= claim.start_x <= self.end_x:
            if self.start_y <= claim.start_y <= self.end_y:
                return True
            if self.start_y <= claim.end_y <= self.end_y:
                return True
        if self.start_x <= claim.end_x <= self.end_x:
            if self.start_y <= claim.start_y <= self.end_y:
                return True
            if self.start_y <= claim.end_y <= self.end_y:
                return True

        return False

    def __str__(self):
        return str([self.id, self.cut_left, self.cut_top, self.width, self.height])


def process_input(data):
    result = []

    for record in data:
        processed_record = {}

        raw_data = record.split(" @ ")

        processed_record["id"] = int(raw_data[0][1:])

        raw_data = raw_data[1].split(": ")
        raw_cuts = raw_data[0].split(",")
        raw_size = raw_data[1].split("x")

        processed_record["cut_left"] = int(raw_cuts[0])
        processed_record["cut_top"] = int(raw_cuts[1])

        processed_record["width"] = int(raw_size[0])
        processed_record["height"] = int(raw_size[1])

        result.append(processed_record)

    return result


def create_claims(data):
    claims = []

    for record in data:
        claim = Claim(record["id"], record["cut_left"], record["cut_top"], record["width"], record["height"])
        claims.append(claim)

    return claims


def calculate_overlaps(claims):
    overlaps = 0

    for i in range(len(claims) - 1):
        for j in range(i+1, len(claims)):
            if claims[i].is_overlap(claims[j]):
                overlaps += 1

    return overlaps


#######################################################################################################################
# Main function
#######################################################################################################################
def __main__():
    # BE SURE TO RENAME PARENT_FOLDER_NAME VARIABLE
    runner = Runner(INPUT_PATH, OUTPUT_PATH, debug=True)

    # Your code goes here
    claims = create_claims(process_input(runner.input_data))

    overlaps = calculate_overlaps(claims)

    runner.finish([overlaps])


#######################################################################################################################
# Process
#######################################################################################################################
if __name__ == "__main__":
    __main__()
