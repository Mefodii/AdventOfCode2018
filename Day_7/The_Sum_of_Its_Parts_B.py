# --- Day 7: The Sum of Its Parts ---
# You find yourself standing on a snow-covered coastline; apparently, you landed a little off course.
# The region is too hilly to see the North Pole from here, but you do spot some Elves that seem to be trying to unpack
# something that washed ashore. It's quite cold out, so you decide to risk creating a paradox by asking
# them for directions.
#
# "Oh, are you the search party?" Somehow, you can understand whatever Elves from the year 1018 speak; you assume
# it's Ancient Nordic Elvish. Could the device on your wrist also be a translator? "Those clothes don't look very
# warm; take this." They hand you a heavy coat.
#
# "We do need to find our way back to the North Pole, but we have higher priorities at the moment.
# You see, believe it or not, this box contains something that will solve all of Santa's transportation
# problems - at least, that's what it looks like from the pictures in the instructions." It doesn't seem like they can
# read whatever language it's in, but you can: "Sleigh kit. Some assembly required."
#
# "'Sleigh'? What a wonderful name! You must help us assemble this 'sleigh' at once!"
# They start excitedly pulling more parts out of the box.
#
# The instructions specify a series of steps and requirements about which steps must be finished before others can
# begin (your puzzle input). Each step is designated by a single letter. For example, suppose you have
# the following instructions:
#
# - Step C must be finished before step A can begin.
# - Step C must be finished before step F can begin.
# - Step A must be finished before step B can begin.
# - Step A must be finished before step D can begin.
# - Step B must be finished before step E can begin.
# - Step D must be finished before step E can begin.
# - Step F must be finished before step E can begin.
#
# Visually, these requirements look like this:
#
#
#   -->A--->B--
#  /    \      \
# C      -->D----->E
#  \           /
#   ---->F-----
#
# Your first goal is to determine the order in which the steps should be completed.
# If more than one step is ready, choose the step which is first alphabetically.
# In this example, the steps would be completed as follows:
#
# - Only C is available, and so it is done first.
# - Next, both A and F are available. A is first alphabetically, so it is done next.
# - Then, even though F was available earlier, steps B and D are now also available, and B is the first alphabetically
#   of the three.
# - After that, only D and F are available. E is not available because only some of its prerequisites are complete.
#   Therefore, D is completed next.
# - F is the only choice, so it is done next.
# - Finally, E is completed.
#
# So, in this example, the correct order is CABDFE.
#
# In what order should the steps in your instructions be completed?
#
# --- Part Two ---
# As you're about to begin construction, four of the Elves offer to help. "The sun will set soon; it'll go faster if we
# work together." Now, you need to account for multiple people working on steps simultaneously.
# If multiple steps are available, workers should still begin them in alphabetical order.
#
# Each step takes 60 seconds plus an amount corresponding to its letter: A=1, B=2, C=3, and so on.
# So, step A takes 60+1=61 seconds, while step Z takes 60+26=86 seconds. No time is required between steps.
#
# To simplify things for the example, however, suppose you only have help from one Elf (a total of two workers)
# and that each step takes 60 fewer seconds (so that step A takes 1 second and step Z takes 26 seconds).
# Then, using the same instructions as above, this is how each second would be spent:
#
# Second   Worker 1   Worker 2   Done
#    0        C          .
#    1        C          .
#    2        C          .
#    3        A          F       C
#    4        B          F       CA
#    5        B          F       CA
#    6        D          F       CAB
#    7        D          F       CAB
#    8        D          F       CAB
#    9        D          .       CABF
#   10        E          .       CABFD
#   11        E          .       CABFD
#   12        E          .       CABFD
#   13        E          .       CABFD
#   14        E          .       CABFD
#   15        .          .       CABFDE
#
# Each row represents one second of time. The Second column identifies how many seconds have passed as of the beginning
# of that second. Each worker column shows the step that worker is currently doing (or . if they are idle).
# The Done column shows completed steps.
#
# Note that the order of the steps has changed; this is because steps now take time to finish and multiple workers
# can begin multiple steps simultaneously.
#
# In this example, it would take 15 seconds for two workers to complete these steps.
#
# With 5 workers and the 60+ second step durations described above, how long will it take to complete all of the steps?

#######################################################################################################################
# IMPORTS
#######################################################################################################################
import re

from utils.paths import SAMPLE_PATH, INPUT_PATH, OUTPUT_PATH
from utils.helpers import Runner

#######################################################################################################################
# CONSTANTS
#######################################################################################################################


#######################################################################################################################
# Root function
#######################################################################################################################
class Brigade:
    def __init__(self, workers, base_execution_time):
        self.workers = workers
        self.base_execution_time = base_execution_time
        self.execution_time = 0
        self.is_executing = False
        self.available_steps = []

    def submit(self, steps):
        self.is_executing = True
        self.available_steps = steps
        while self.is_executing:
            can_assign = True
            while can_assign:
                current_step = self.get_next_step()

                if current_step:
                    worker = self.next_available_worker()

                    if worker:
                        worker.assign(current_step)
                        self.available_steps.remove(current_step)
                    else:
                        can_assign = False
                else:
                    can_assign = False

            self.refresh()

            if self.is_executing:
                self.execute_shortest_step()

        return self.execution_time

    def refresh(self):
        if len(self.available_steps) > 0:
            return
        else:
            for worker in self.workers:
                if worker.is_executing:
                    return

        self.is_executing = False

    def execute_shortest_step(self):
        workers_execution_time = []

        for worker in self.workers:
            if worker.is_executing:
                workers_execution_time.append(worker.time_to_execute)

        execution_time = min(workers_execution_time)
        self.execute(execution_time)

    def execute(self, time):
        for worker in self.workers:
            self.available_steps += worker.execute(time)

        self.execution_time += time

    def next_available_worker(self):
        for worker in self.workers:
            if not worker.is_executing:
                return worker

        return None

    def get_next_step(self):
        if len(self.available_steps) > 0:
            candidate = self.available_steps[0]

            for i in range(1, len(self.available_steps)):
                if self.available_steps[i].name < candidate.name:
                    candidate = self.available_steps[i]

            return candidate

        return None


class Worker:
    def __init__(self, base_execution_time):
        self.step = None
        self.time_to_execute = -1
        self.base_execution_time = base_execution_time
        self.is_executing = False

    def assign(self, step):
        self.step = step
        self.time_to_execute = self.base_execution_time + ord(step.name) - 64
        self.is_executing = True

    def execute(self, time):
        next_available_steps = []
        if self.is_executing:
            self.time_to_execute -= time

            if self.time_to_execute <= 0:
                self.is_executing = False
                self.step.execute()

                for step in self.step.next_steps:
                    if step.is_available:
                        next_available_steps.append(step)

        return next_available_steps


class Step:
    def __init__(self, name):
        self.name = name
        self.is_executed = False
        self.is_available = False
        self.next_steps = []
        self.prev_steps = []

    def add_next(self, step):
        self.next_steps.append(step)

    def add_prev(self, step):
        self.prev_steps.append(step)

    def refresh(self):
        is_available = True

        for step in self.prev_steps:
            if not step.is_executed:
                is_available = False

        self.is_available = is_available

    def execute(self):
        self.is_executed = True

        for step in self.next_steps:
            step.refresh()

    def __str__(self):
        return self.name + " " + str(len(self.next_steps)) + " " + str(len(self.prev_steps))

    def __repr__(self):
        s = "{Name: " + self.name + ", "

        next_s = "["
        for step in self.next_steps:
            next_s += step.name + ", "
        s += next_s + "] "

        prev_s = "["
        for step in self.prev_steps:
            prev_s += step.name + ", "
        s += prev_s + "] "

        s += "}"
        return s


def create_steps(raw_steps):
    steps = {}

    steps_name = set([])
    for raw_step in raw_steps:
        old_steps_name_len = len(steps_name)
        steps_name.add(raw_step[0])
        if not old_steps_name_len == len(steps_name):
            steps[raw_step[0]] = Step(raw_step[0])

        old_steps_name_len = len(steps_name)
        steps_name.add(raw_step[1])
        if not old_steps_name_len == len(steps_name):
            steps[raw_step[1]] = Step(raw_step[1])

        steps[raw_step[0]].add_next(steps[raw_step[1]])
        steps[raw_step[1]].add_prev(steps[raw_step[0]])

    return [steps[step] for step in steps]


def process_input(data):
    steps = []
    for record in data:
        re_groups = re.search("Step (\w).*step (\w)", record)
        steps.append([re_groups.group(1), re_groups.group(2)])

    return steps


def get_next_step(available_steps):
    candidate = available_steps[0]

    for i in range(1, len(available_steps)):
        if available_steps[i].name < candidate.name:
            candidate = available_steps[i]

    return candidate


def execute_steps(steps, base_execution_time, workers_number):
    brigade = Brigade([Worker(base_execution_time) for i in range(workers_number)], base_execution_time)

    available_steps = []
    for step in steps:
        if len(step.prev_steps) == 0:
            available_steps.append(step)

    execution_time = brigade.submit(available_steps)

    return execution_time


#######################################################################################################################
# Main function
#######################################################################################################################
def __main__():
    runner = Runner(INPUT_PATH, OUTPUT_PATH, debug=True)

    # Your code goes here
    raw_steps = process_input(runner.input_data)
    steps = create_steps(raw_steps)

    base_time = 60
    worker_num = 5
    execution_log = execute_steps(steps, base_time, worker_num)

    runner.finish([execution_log])


#######################################################################################################################
# Process
#######################################################################################################################
if __name__ == "__main__":
    __main__()
