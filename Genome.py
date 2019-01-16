from Node import *
from Gene import *


class Genome:
    def __init__(self, inputs, outputs):

        self.inputs = inputs
        self.outputs = outputs

        # Creating in and out nodes
        self.nodes = [Node(0) for _ in range(inputs)] + [Node(1) for _ in range(outputs)] # Never changes order
        # Bias Node
        self.nodes.append(Node(0))

        self.genes = [] #Never changes order
        self.layers = [self._get_input() + self._get_bias(), self._get_output()]

    def assemble(self):
        """Reorders node_exe_order genes_exe_order and layer assignment"""
        exe_order = []
        for layer in self.layers:
            exe_order += sorted(layer, key=lambda o: 0 if type(o) is Node else 1)
        return exe_order

    def _insert_layer(self, layer_nr, layer):
        """layer is the layer below which to insert a layer"""
        self.layers.inser(layer_nr + 1, layer)

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

