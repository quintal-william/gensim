from .node import Node


'''
A number between 0 and 1 which represents the probability of two nodes being connected
'''
Connectivity = float

'''
Helper type that allows the user to pass in either a list of nodes, or tha number of LeafNodes that should be added to a topology
'''
Nodes = int | list[Node]
