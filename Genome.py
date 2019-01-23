from Node import *
from Gene import *
from Functions import identity

class Genome:
    def __init__(self, inputs, outputs):

        self.inputs = inputs
        self.outputs = outputs

        # Creating in and out nodes
        self.nodes = [Node(identity, []) for _ in range(inputs)]
        self.nodes += [Node(identity, self.nodes[:self.inputs]) for _ in range(outputs)]  # Never changes order
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

    def run(self, inputs):
        for node, value in zip(self._get_input(), inputs):
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

    def _add_gene(self, gene):
        """Needs to check if the gene does not create a circle and rearrange layers if needed"""
        if gene.out_node in self.nodes[gene.in_node].after:
            print("connection gene not valid")
            return False
        else:
            self.nodes[gene.out_node].after.append(gene.in_node)
            for node in self.nodes: # TODO Make more efficient
                if gene.out_node in node.after:
                    node.after.append(gene.in_node)
            while self._find_layer(self.nodes[gene.in_node]) >= self._find_layer(self.nodes[gene.out_node]):
                self._move_node(self.nodes[gene.in_node])

            for g in self.genes:
                if g.in_node == gene.in_node and g.out_node == gene.out_node:
                    g.disable()
            self.genes.append(gene)
        pass

    def _find_layer(self, obj):
        for i, layer in enumerate(self.layers): # TODO make more efficient
            if obj in layer:
                return i
        return None

    def _move_node(self, node):
        """moves a node downward by number of layers"""
        layer = self._find_layer(node)
        if layer == 0:
            print("can not move input nodes")
            return None
        elif layer == 1:
            self._insert_layer(1, [node])
            self.layers[2].remove(node)
        else:
            self.layers[layer - 1].append(node)
            self.layers[layer].remove(node)
            for i in node.after:
                self._move_node(self.nodes[i])
        pass

    def reset(self):
        for node in self.nodes:
            node.value = 0

    def _insert_layer(self, layer_nr, layer):
        """layer is the layer below which to insert a layer"""
        self.layers.insert(layer_nr + 1, layer)

    def _add_gene_overide(self, gene): # TODO remove/modify to match _add_gene
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
