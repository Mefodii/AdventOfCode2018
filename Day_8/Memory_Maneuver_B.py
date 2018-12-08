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
#
# --- Part Two ---
# The second check is slightly more complicated: you need to find the value of the root node (A in the example above).
#
# The value of a node depends on whether it has child nodes.
#
# If a node has no child nodes, its value is the sum of its metadata entries.
# So, the value of node B is 10+11+12=33, and the value of node D is 99.
#
# However, if a node does have child nodes, the metadata entries become indexes which refer to those child nodes.
# A metadata entry of 1 refers to the first child node, 2 to the second, 3 to the third, and so on.
# The value of this node is the sum of the values of the child nodes referenced by the metadata entries.
# If a referenced child node does not exist, that reference is skipped. A child node can be referenced multiple
# time and counts each time it is referenced. A metadata entry of 0 does not refer to any child node.
#
# For example, again using the above nodes:
#
# - Node C has one metadata entry, 2. Because node C has only one child node, 2 references a child node which does not
#   exist, and so the value of node C is 0.
# - Node A has three metadata entries: 1, 1, and 2. The 1 references node A's first child node, B, and the 2
#   references node A's second child node, C. Because node B has a value of 33 and node C has a value of 0, the value
#   of node A is 33+33+0=66.
#
# So, in this example, the value of the root node is 66.
#
# What is the value of the root node?

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
        self.value = 0

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

    def update_value(self):
        if self.children_number == 0:
            self.value = self.metadata_sum()
        else:
            for metadata_value in self.metadata:
                if metadata_value <= self.children_number:
                    self.value += self.children[metadata_value - 1].value

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
    node.update_value()

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
    tree_root.update_value()

    return tree_root


#######################################################################################################################
# Main function
#######################################################################################################################
def __main__():
    runner = Runner(INPUT_PATH, OUTPUT_PATH, debug=True)

    # Your code goes here
    tree = build_tree(runner.input_data[0])

    runner.finish([tree.value])


#######################################################################################################################
# Process
#######################################################################################################################
if __name__ == "__main__":
    __main__()
