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


def execute_steps(steps):
    execution_log = ""

    available_steps = []
    for step in steps:
        if len(step.prev_steps) == 0:
            available_steps.append(step)

    current_step = get_next_step(available_steps)
    available_steps.remove(current_step)
    while current_step:
        execution_log += current_step.name
        current_step.execute()

        for step in current_step.next_steps:
            if step.is_available:
                available_steps.append(step)

        if len(available_steps) == 0:
            current_step = None
        else:
            candidate = get_next_step(available_steps)

            available_steps.remove(candidate)
            current_step = candidate

    return execution_log


#######################################################################################################################
# Main function
#######################################################################################################################
def __main__():
    runner = Runner(INPUT_PATH, OUTPUT_PATH, debug=True)

    # Your code goes here
    raw_steps = process_input(runner.input_data)
    steps = create_steps(raw_steps)

    execution_log = execute_steps(steps)

    runner.finish([execution_log])


#######################################################################################################################
# Process
#######################################################################################################################
if __name__ == "__main__":
    __main__()
