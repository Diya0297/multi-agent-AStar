class Node:
    '''
    state: list of 9 integers (current board) --> list
    parent: Link to previous node --> Node 
    actions: Up, Down, Left, Right --> String
    g: Cost from start to current node --> int
    h: heuristic esimate to the goal --> int
    f: g + h --> int
    '''
    def __init__(self, state, parent=None, actions=None, g=0, h=0):
        self.state = state
        self.parent = parent 
        self.actions = actions
        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f
    