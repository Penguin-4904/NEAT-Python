import random
from Node import *
from Gene import *
from Functions import identity


class Genome:
    def __init__(self, inputs, outputs, functions, innovation):

        self.inputs = inputs
        self.outputs = outputs
        self.functions = functions
        self.new_innovation = innovation

        # Creating in and out nodes
        self.nodes = [Node(identity, []) for _ in range(inputs)]
        self.nodes += [Node(identity, self.nodes[:self.inputs]) for _ in range(outputs)]  # Never changes order
        # Bias Node
        self.nodes.append(Node(0))
        self.genes = []  # Never changes order
        self.layers = [self._get_input() + self._get_bias(), self._get_output()]
        self.score = 0

    def _assemble(self):
        """Returns the execution order for the neural net so it can go through feed forward"""
        exe_order = []
        for layer in self.layers:
            exe_order += layer
            for gene in self.genes:
                if self.nodes[gene.in_node] in layer:
                    exe_order.append(gene)
        return exe_order

    def run(self, inputs):
        for node, value in zip(self._get_input(), inputs):
            node.value = value
        exe_order = self._assemble()
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
            for node in self.nodes:
                if gene.out_node in node.after:
                    node.after.append(gene.in_node)
            while self._find_layer(self.nodes[gene.in_node]) >= self._find_layer(self.nodes[gene.out_node]):
                self._move_node(self.nodes[gene.in_node])

            for g in self.genes:
                if g.in_node == gene.in_node and g.out_node == gene.out_node:
                    g.disable()
            # self.layers[self._find_layer(self.nodes[gene.in_node])].append(gene)
            self.genes.append(gene)

    def mutate(self, gene_chance, node_chance):
        if random.random() < gene_chance:
            self._mutate_gene()
        if random.random() < node_chance:
            self._mutate_node()

    def _mutate_gene(self):
        in_node = random.choice(list(sum(self.layers[:-1], [])))
        ls = [x if i not in in_node.after else None for i, x in enumerate(self.nodes)]
        ls = filter(None, ls)
        out_node = self.nodes.index(random.choice(ls))
        in_node = self.nodes.index(in_node)
        weight = random.random()
        innovation = self.new_innovation(in_node, out_node)
        gene = Gene(in_node, out_node, weight, innovation)
        self._add_gene(gene)

    def _mutate_node(self):
        gene = random.choice(self.genes)
        func = random.choice(self.functions)
        node = Node(func, self.nodes[gene.in_node].after)
        i = len(self.nodes)
        self.nodes[gene.out_node].after.append(i)
        self.nodes.append(node)
        self.layers[-2].append(node)
        gene1 = Gene(gene.in_node, i, gene.weight, self.new_innovation(gene.in_node, i))
        gene2 = Gene(i, gene.out_node, 1, self.new_innovation(i, gene.out_node))
        self._add_gene(gene2)
        self._add_gene(gene1)
        gene.disable()

    def _find_layer(self, obj):
        for i, layer in enumerate(self.layers):  # TODO make more efficient
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
                if self._find_layer(self.nodes[i]) + 1 >= layer:
                    self._move_node(self.nodes[i])
        pass

    def reset(self):
        for node in self.nodes:
            node.value = 0

    def _insert_layer(self, layer_nr, layer):
        """layer is the layer below which to insert a layer"""
        self.layers.insert(layer_nr + 1, layer)

    def _get_bias(self):
        return self.nodes[self.inputs + self.outputs]

    def _get_input(self):
        return self.nodes[:self.inputs]

    def _get_output(self):
        return self.nodes[self.inputs:self.inputs + self.outputs]

    def get_score(self):
        return self.score
