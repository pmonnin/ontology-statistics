__author__ = "Pierre Monnin"

"""
    Little ontology to test statistics' algorithms
"""

class_to_index = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6
}

index_to_class = [
    'a',
    'b',
    'c',
    'd',
    'e',
    'f',
    'g',
]

class_parents = [
    [3, 4, 6],
    [0],
    [1],
    [2],
    [3],
    [4],
    []
]

class_children = [
    [1],
    [2],
    [3],
    [0, 4],
    [0, 5],
    [],
    [0]
]
