#######################################################################################################################
# Prepare libs
#######################################################################################################################
import time
from utils import File


class Runner:
    def __init__(self, input_file, output_file, debug=False):
        self.time_start = time.time()
        self.time_finish = None
        self.time_execution = None

        self.input_file = input_file
        self.output_file = output_file
        self.input_data = File.read(input_file)
        self.output_data = []

        self.debug = debug

    def finish(self, output_data):
        self.output_data = output_data
        File.write(self.output_file, self.output_data)

        self.time_finish = time.time()
        self.time_execution = self.time_finish - self.time_start

        if self.debug:
            print("------======   RESULT   ======------")
            for line in self.output_data:
                print(line)
            print("------======   STATS    ======------")
            print("Program ran for: ", self.time_execution, "seconds.")