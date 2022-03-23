from typing import Tuple, TypeVar, Generic, Dict, Set


def clamp(var, min, max):
    """
        Helper function to clamp a variable between a `min` and a `max`.
    """
    
    if var < min:
        var = min
    elif var > max:
        var = max


T = TypeVar("T")
Edge = Tuple[T, float]


class MarkovChain(Generic[T]):
    """
        A data structure that resembles a directed graph with the edges containing probabilities.
    """

    _adjacency_list: Dict[T, Set[Edge]]
    __slots__ = "_adjacency_list"
    
    def __init__(self) -> None:
        self._adjacency_list = {  }
        super().__init__()
    
    def add_vertex(self, key: T):
        """
            Adds a new vertex into the `MarkovChain` which can be connected to other verticies with edges.
        """
        
        self._adjacency_list[key] = set()
    
    def remove_vertex(self, key: T):
        """
            Removes a vertex from the `MarkovChain`, removing any reference to it in the edges as well.
        """
        
        del self._adjacency_list[key]
    
    def add_edge(self, vertex_a: T, vertex_b: T, probability: float):
        """
            Adds a new edge from `vertex_a` to `vertex_b` with the provided `probability`,
            the `probability` is clamped from `0.0` to `1.0` minus the sum of all probabilities within `vertex_a`.
        """
        
        total_probability = sum(e[1] for e in self._adjacency_list[vertex_a])
        self._adjacency_list[vertex_a].add((vertex_b, clamp(probability, 0.0, 1.0 - total_probability)))
    
    def remove_edge(self, vertex_a: T, vertex_b: T):
        """
            Completely removes an edge between two verticies.
        """
        
        self._adjacency_list[vertex_a].remove(vertex_b)

    def modify_probability(self, vertex_a: T, vertex_b: T, probability: float):
        """
            Modifies the `probability` of an edge between two verticies,
            the `probability` is clamped from `0.0` to `1.0` minus the sum of all probabilities within `vertex_a`.
        """
        
        assert vertex_b in self._adjacency_list[vertex_a], \
            "There is no edge between the two given verticies in modify_probability()."
        
        total_probability = sum(e[1] for e in self._adjacency_list[vertex_a])
        self._adjacency_list[vertex_a][vertex_b][1] = clamp(probability, 0.0, 1.0 - total_probability)