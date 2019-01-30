
class Node:
    def __init__(self, func, after=[]):
        self.value = 0
        self.func = func
        self.after = after # which nodes this nodes can not run simultaneously with or before

    def run(self):
        self.value = self.func(self.value)
        return self.value