class State():
    def __init__(self, data):
        self.data=data
        pass

    def enter(self, root):
        self.root = root

    def exit(self):
        pass

    def transition(self, new_state):
        self.exit()
        new_state.enter(self.root)