import os
import sys

PROJECT_PATH = "\\".join(os.getcwd().split("\\")[0:-1])
PARENT_FOLDER_NAME = os.path.basename(os.getcwd())
FILES_NAME = "io"
INPUT_FILE = "input.txt"
SAMPLE_FILE = "sample.txt"
OUTPUT_FILE = os.path.basename(sys.argv[0])[:-3] + "_output.txt"

SAMPLE_PATH = "/".join([PROJECT_PATH, PARENT_FOLDER_NAME, FILES_NAME, SAMPLE_FILE])
INPUT_PATH = "/".join([PROJECT_PATH, PARENT_FOLDER_NAME, FILES_NAME, INPUT_FILE])
OUTPUT_PATH = "/".join([PROJECT_PATH, PARENT_FOLDER_NAME, FILES_NAME, OUTPUT_FILE])
