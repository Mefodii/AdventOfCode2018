# --- Day 5: Alchemical Reduction ---
# You've managed to sneak in to the prototype suit manufacturing lab. The Elves are making decent progress, but are
# still struggling with the suit's size reduction capabilities.
#
# While the very latest in 1518 alchemical technology might have solved their problem eventually, you can do better.
# You scan the chemical composition of the suit's material and discover that it is formed by extremely long polymers
# (one of which is available as your puzzle input).
#
# The polymer is formed by smaller units which, when triggered, react with each other such that two adjacent units
# of the same type and opposite polarity are destroyed. Units' types are represented by letters; units' polarity is
# represented by capitalization. For instance, r and R are units with the same type but opposite polarity,
# whereas r and s are entirely different types and do not react.
#
# For example:
#
# - In aA, a and A react, leaving nothing behind.
# - In abBA, bB destroys itself, leaving aA. As above, this then destroys itself, leaving nothing.
# - In abAB, no two adjacent units are of the same type, and so nothing happens.
# - In aabAAB, even though aa and AA are of the same type, their polarities match, and so nothing happens.
#
# Now, consider a larger example, dabAcCaCBAcCcaDA:
#
# dabAcCaCBAcCcaDA  The first 'cC' is removed.
# dabAaCBAcCcaDA    This creates 'Aa', which is removed.
# dabCBAcCcaDA      Either 'cC' or 'Cc' are removed (the result is the same).
# dabCBAcaDA        No further actions can be taken.
#
# After all possible reactions, the resulting polymer contains 10 units.

#######################################################################################################################
# IMPORTS
#######################################################################################################################
import os

from utils import paths
from utils.helpers import Runner

#######################################################################################################################
# CONSTANTS
#######################################################################################################################
PARENT_FOLDER_NAME = "Day_5"
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
def shrink(record):
    old_value = ""
    new_value = record

    while not len(new_value) == len(old_value):
        old_value = new_value

        for i in "abcdefghijklmnopqrstuvwxyz":
            new_value = new_value.replace(i + i.upper(), "")
            new_value = new_value.replace(i.upper() + i, "")

    return new_value


#######################################################################################################################
# Main function
#######################################################################################################################
def __main__():
    # BE SURE TO RENAME PARENT_FOLDER_NAME VARIABLE
    runner = Runner(INPUT_PATH, OUTPUT_PATH, debug=True)

    # Your code goes here
    shrunk_result = shrink(runner.input_data[0])

    runner.finish([len(shrunk_result)])


#######################################################################################################################
# Process
#######################################################################################################################
if __name__ == "__main__":
    __main__()
