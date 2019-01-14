from Node import *
from Gene import *


class Genome:
    def __init__(self, inputs, outputs):

        self.inputs = inputs
        self.outputs = outputs

        # Creating in and out nodes
        self.nodes = [Node() for _ in range(inputs)] + [Node() for _ in range(outputs)] # Never changes order
        self.node_exe_order = list(range(inputs + outputs)) # Changes order to build network correctly
        # Bias Node
        self.nodes.append(Node())
        self.node_exe_order.insert(0, inputs + outputs)

        self.genes = []
