# --- Day 8: Memory Maneuver ---
# The sleigh is much easier to pull than you'd expect for something its weight.
# Unfortunately, neither you nor the Elves know which way the North Pole is from here.
#
# You check your wrist device for anything that might help. It seems to have some kind of navigation system!
# Activating the navigation system produces more bad news: "Failed to start navigation system.
# Could not read software license file."
#
# The navigation system's license file consists of a list of numbers (your puzzle input).
# The numbers define a data structure which, when processed, produces some kind of tree that can be
# used to calculate the license number.
#
# The tree is made up of nodes; a single, outermost node forms the tree's root, and it contains all
# other nodes in the tree (or contains nodes that contain nodes, and so on).
#
# Specifically, a node consists of:
#
# A header, which is always exactly two numbers:
# - The quantity of child nodes.
# - The quantity of metadata entries.
# - Zero or more child nodes (as specified in the header).
# - One or more metadata entries (as specified in the header).
#
# Each child node is itself a node that has its own header, child nodes, and metadata. For example:
#
# 2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
# A----------------------------------
#     B----------- C-----------
#                      D-----
#
# In this example, each node of the tree is also marked with an underline starting with a letter for easier
# identification. In it, there are four nodes:
#
# - A, which has 2 child nodes (B, C) and 3 metadata entries (1, 1, 2).
# - B, which has 0 child nodes and 3 metadata entries (10, 11, 12).
# - C, which has 1 child node (D) and 1 metadata entry (2).
# - D, which has 0 child nodes and 1 metadata entry (99).
#
# The first check done on the license file is to simply add up all of the metadata entries.
# In this example, that sum is 1+1+2+10+11+12+2+99=138.
#
# What is the sum of all metadata entries?
#
# Your puzzle answer was 38567.
#
# The first half of this puzzle is complete! It provides one gold star: *

#######################################################################################################################
# IMPORTS
#######################################################################################################################
import os

from utils.paths import SAMPLE_PATH, INPUT_PATH, OUTPUT_PATH
from utils.helpers import Runner

#######################################################################################################################
# CONSTANTS
#######################################################################################################################


#######################################################################################################################
# Root function
#######################################################################################################################
class Node:
    BASE_LENGTH = 2

    def __init__(self, parent_node, children_number, metadata_length):
        self.children_number = children_number
        self.metadata_length = metadata_length

        self.children = []
        self.parent = parent_node
        self.metadata = []

        self.width = self.BASE_LENGTH + self.metadata_length

    def add_child(self, node):
        self.children.append(node)
        self.update_width()

    def set_parent(self, node):
        self.parent = node

    def metadata_sum(self):
        return sum(self.metadata)

    def full_metadata_sum(self):
        return self.metadata_sum() + sum([child.full_metadata_sum() for child in self.children])

    def update_width(self):
        self.width = sum([child.width for child in self.children]) + self.metadata_length + self.BASE_LENGTH

    def __repr__(self):
        s = str(self.children_number) + " " + str(self.metadata_length) + " "

        for child in self.children:
            s += repr(child) + " "

        s += " ".join([str(metadata_value) for metadata_value in self.metadata])

        return s


def build_node(parent_node, values):
    node_children_number = values[0]
    node_metadata_length = values[1]
    node = Node(parent_node, node_children_number, node_metadata_length)

    for i in range(node_children_number):
        child_values = values[node.width - node.metadata_length:]
        node.add_child(build_node(node, child_values))

    node.metadata = values[node.width - node.metadata_length:node.width]

    return node


def build_tree(data):
    values = [int(string_value) for string_value in data.split(" ")]

    root_children_number = values[0]
    root_metadata_length = values[1]
    tree_root = Node(None, root_children_number, root_metadata_length)

    for i in range(root_children_number):
        child_values = values[tree_root.width - tree_root.metadata_length:]
        tree_root.add_child(build_node(tree_root, child_values))

    tree_root.metadata = values[tree_root.width - tree_root.metadata_length:tree_root.width]
    return tree_root


#######################################################################################################################
# Main function
#######################################################################################################################
def __main__():
    runner = Runner(INPUT_PATH, OUTPUT_PATH, debug=True)

    # Your code goes here
    tree = build_tree(runner.input_data[0])

    runner.finish([tree.full_metadata_sum()])


#######################################################################################################################
# Process
#######################################################################################################################
if __name__ == "__main__":
    __main__()
