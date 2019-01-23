from Node import *
from Gene import *


class Genome:
    def __init__(self, inputs, outputs):

        self.inputs = inputs
        self.outputs = outputs

        # Creating in and out nodes
        self.nodes = [Node(0) for _ in range(inputs)] + [Node(1) for _ in range(outputs)]  # Never changes order
        # Bias Node
        self.nodes.append(Node(0))

        self.genes = []  # Never changes order
        self.layers = [self._get_input() + self._get_bias(), self._get_output()]

    def assemble(self):
        """Returns the execution order for the neural net so it can go through feed forward"""
        exe_order = []
        for layer in self.layers:
            exe_order += sorted(layer, key=lambda o: 0 if type(o) is Node else 1)
        return exe_order

    def run(self, input):
        for node, value in zip(self._get_input(), input):
            node.value = value
        exe_order = self.assemble()
        for obj in exe_order:
            if type(obj) is Gene:
                obj.value = self.nodes[obj.in_node].value
            obj.run()
            if type(obj) is Gene:
                self.nodes[obj.out_node].value += obj.value
        out = []
        for node in self._get_output():
            out.append(node.value)
        self.reset()
        return out

    def reset(self):
        for node in self.nodes:
            node.value = 0

    def _insert_layer(self, layer_nr, layer):
        """layer is the layer below which to insert a layer"""
        self.layers.insert(layer_nr + 1, layer)

    def _add_gene_overide(self, gene):
        """Overrides everything even if the gene is already present"""
        in_node = gene.in_node
        out_node = gene.out_node
        for g in self.genes:
            if g.in_node == in_node and g.out_node == out_node:
                self.genes.remove(g)
                self.genes.append(gene)

    def _get_bias(self):
        return self.nodes[self.inputs + self.outputs]

    def _get_input(self):
        return self.nodes[:self.inputs]

    def _get_output(self):
        return self.nodes[self.inputs:self.inputs + self.outputs]
