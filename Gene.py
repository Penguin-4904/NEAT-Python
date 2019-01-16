class Gene:
    def __init__(self, in_node, out_node, weight, innovation, enabled=True):
        # The Gene for a connection between nodes
        self.out_node = out_node
        self.in_node = in_node
        self.weight = weight
        self.enabled = enabled
        self.innovation = innovation
        self.value = 0

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True

    def run(self):
        self.value = self.value * self.weight
        return self.value
