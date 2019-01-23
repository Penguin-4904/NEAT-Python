class Gene:
    def __init__(self, in_node, out_node, weight, innovation, enabled=True):
        # The Gene for a connection between nodes
        self.out_node = out_node # The Id of the in and out node
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
        if self.enabled:
            self.value = self.value * self.weight
            return self.value
        else:
            self.value = 0
            return self.value
