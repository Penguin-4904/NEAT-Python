
class Node:
    def __init__(self, func):
        self.layer = layer
        self.value = 0
        self.func = func

    def run(self):
        self.value = self.func(self.value)
        return self.value
