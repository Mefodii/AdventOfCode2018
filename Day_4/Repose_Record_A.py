# --- Day 4: Repose Record ---
# You've sneaked into another supply closet - this time, it's across from the prototype suit manufacturing lab.
# You need to sneak inside and fix the issues with the suit, but there's a guard stationed outside the lab, so this
# is as close as you can safely get.
#
# As you search the closet for anything that might help, you discover that you're not the first person to want to sneak
# in. Covering the walls, someone has spent an hour starting every midnight for the past few months secretly observing
# this guard post! They've been writing down the ID of the one guard on duty that night - the Elves seem to have
# decided that one guard was enough for the overnight shift - as well as when they fall asleep or wake up while at
# their post (your puzzle input).
#
# For example, consider the following records, which have already been organized into chronological order:
#
# [1518-11-01 00:00] Guard #10 begins shift
# [1518-11-01 00:05] falls asleep
# [1518-11-01 00:25] wakes up
# [1518-11-01 00:30] falls asleep
# [1518-11-01 00:55] wakes up
# [1518-11-01 23:58] Guard #99 begins shift
# [1518-11-02 00:40] falls asleep
# [1518-11-02 00:50] wakes up
# [1518-11-03 00:05] Guard #10 begins shift
# [1518-11-03 00:24] falls asleep
# [1518-11-03 00:29] wakes up
# [1518-11-04 00:02] Guard #99 begins shift
# [1518-11-04 00:36] falls asleep
# [1518-11-04 00:46] wakes up
# [1518-11-05 00:03] Guard #99 begins shift
# [1518-11-05 00:45] falls asleep
# [1518-11-05 00:55] wakes up
#
# Timestamps are written using year-month-day hour:minute format. The guard falling asleep or waking up is always the
# one whose shift most recently started. Because all asleep/awake times are during the midnight hour (00:00 - 00:59),
# only the minute portion (00 - 59) is relevant for those events.
#
# Visually, these records show that the guards are asleep at these times:
#
# Date   ID   Minute
#             000000000011111111112222222222333333333344444444445555555555
#             012345678901234567890123456789012345678901234567890123456789
# 11-01  #10  .....####################.....#########################.....
# 11-02  #99  ........................................##########..........
# 11-03  #10  ........................#####...............................
# 11-04  #99  ....................................##########..............
# 11-05  #99  .............................................##########.....
#
# The columns are Date, which shows the month-day portion of the relevant day; ID, which shows the guard on duty that
# day; and Minute, which shows the minutes during which the guard was asleep within the midnight hour.
# (The Minute column's header shows the minute's ten's digit in the first row and the one's digit in the second row.)
# Awake is shown as ., and asleep is shown as #.
#
# Note that guards count as asleep on the minute they fall asleep, and they count as awake on the minute they wake up.
# For example, because Guard #10 wakes up at 00:25 on 1518-11-01, minute 25 is marked as awake.
#
# If you can figure out the guard most likely to be asleep at a specific time, you might be able to trick that guard
# into working tonight so you can have the best chance of sneaking in. You have two strategies for choosing the best
# guard/minute combination.
#
# Strategy 1: Find the guard that has the most minutes asleep. What minute does that guard spend asleep the most?
#
# In the example above, Guard #10 spent the most minutes asleep, a total of 50 minutes (20+25+5), while Guard #99 only
# slept for a total of 30 minutes (10+10+10). Guard #10 was asleep most during minute 24 (on two days, whereas any
# other minute the guard was asleep was only seen on one day).
#
# While this example listed the entries in chronological order, your entries are in the order you found them. You'll
# need to organize them before they can be analyzed.
#
# What is the ID of the guard you chose multiplied by the minute you chose?
# (In the above example, the answer would be 10 * 24 = 240.)

#######################################################################################################################
# IMPORTS
#######################################################################################################################
import datetime
import re

from utils.paths import SAMPLE_PATH, INPUT_PATH, OUTPUT_PATH
from utils.helpers import Runner

#######################################################################################################################
# CONSTANTS
#######################################################################################################################
ACTION_SLEEP = "S"
ACTION_WAKE_UP = "W"
SHIFT_LENGTH = 60


#######################################################################################################################
# Root function
#######################################################################################################################
class Shift:
    def __init__(self, date, guard_id):
        self.date = date
        self.guard_id = guard_id
        self.actions = []
        self.shift_log = [False for i in range(SHIFT_LENGTH)]
        self.sleep_time = 0

    def add_action(self, action):
        self.actions.append(action)

    def create_shift_log(self):
        for i in range(len(self.actions) - 1):
            if self.actions[i][0] == ACTION_SLEEP:
                for j in range(self.actions[i][1], self.actions[i + 1][1]):
                    self.shift_log[j] = True
                    self.sleep_time += 1

        if len(self.actions) > 0 and self.actions[-1][0] == ACTION_SLEEP:
            for j in range(self.actions[-1][1], SHIFT_LENGTH):
                self.shift_log[j] = True
                self.sleep_time += 1

    def __str__(self):
        log = ""
        for minute in self.shift_log:
            if minute:
                log += "#"
            else:
                log += "."
        return " ".join([self.date, self.guard_id, log])


def create_shifts(data):
    shifts = []
    shift = None

    for record in data:
        re_date = re.search(r'(\d{4}-\d\d-\d\d) (\d\d):(\d\d)', record)
        re_shift_start = re.search(r'.*#\D*(\d*).*(shift)', record)
        re_asleep = re.search(r'(asleep)', record)
        re_waking = re.search(r'(wakes)', record)

        if re_shift_start:
            if shift:
                shift.create_shift_log()
                shifts.append(shift)

            date = datetime.datetime.strptime(re_date.group(1), "%Y-%m-%d").date()
            if re_date.group(2) == "23":
                date += datetime.timedelta(days=1)

            shift = Shift(date, int(re_shift_start.group(1)))
        elif re_asleep:
            shift.add_action([ACTION_SLEEP, int(re_date.group(3))])
        elif re_waking:
            shift.add_action([ACTION_WAKE_UP, int(re_date.group(3))])

    shift.create_shift_log()
    shifts.append(shift)

    return shifts


def obtain_most_tired_guard(shifts):
    guards = {}

    for shift in shifts:
        guards[shift.guard_id] = guards.get(shift.guard_id, 0) + shift.sleep_time

    guard_id = "0"
    sleep_time = 0
    for key, value in guards.items():
        if value > sleep_time:
            guard_id = key
            sleep_time = value

    return guard_id


def get_shifts_for_guard(shifts, guard_id):
    shifts_for_guard = []

    for shift in shifts:
        if shift.guard_id == guard_id:
            shifts_for_guard.append(shift)

    return shifts_for_guard


def get_most_asleep_minute(shifts):
    most_asleep_minute = 0
    most_asleep_minute_sleep_count = 0

    for i in range(SHIFT_LENGTH):
        sleep_count = 0
        for shift in shifts:
            if shift.shift_log[i]:
                sleep_count += 1

        if sleep_count > most_asleep_minute_sleep_count:
            most_asleep_minute = i
            most_asleep_minute_sleep_count = sleep_count

    return most_asleep_minute


#######################################################################################################################
# Main function
#######################################################################################################################
def __main__():
    # BE SURE TO RENAME PARENT_FOLDER_NAME VARIABLE
    runner = Runner(INPUT_PATH, OUTPUT_PATH, debug=True)

    # Your code goes here
    runner.input_data.sort()
    shifts = create_shifts(runner.input_data)

    most_tired_guard = obtain_most_tired_guard(shifts)
    shifts_for_guard = get_shifts_for_guard(shifts, most_tired_guard)
    most_asleep_minute = get_most_asleep_minute(shifts_for_guard)

    checksum = int(most_tired_guard) * most_asleep_minute
    runner.finish([checksum])


#######################################################################################################################
# Process
#######################################################################################################################
if __name__ == "__main__":
    __main__()
