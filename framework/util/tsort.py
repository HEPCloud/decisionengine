"""
See:

https://en.wikipedia.org/wiki/Topological_sorting

Kahn's topological sorting algorithm

L Empty list that will contain the sorted elements
S Set of all nodes with no incoming edge
while S is non-empty do
    remove a node n from S
    add n to tail of L
    for each node m with an edge e from n to m do
        remove edge e from the graph
        if m has no other incoming edges then
            insert m into S
if graph has edges then
    return error (graph has at least one cycle)
else
    return L (a topologically sorted order)
"""

import types


def tsort(graph):
    """
    Function implementing Kahn's topological sorting algorithm
    returns two lists : sorted list and cyclic lost
    (if graph is acyclic second list is always None)

    :type graph: :obj:`dict` that contains pairs of vertices
                 and adjacent edges.
    :rtype: :obj:`list`

    """

    if isinstance(graph, types.ListType):
        graph = dict(graph)
    """
    count incoming edges for each vertex
    """
    incoming_edges = {}
    for vertex, edges in graph.items():
        incoming_edges.setdefault(vertex, 0)
        for edge in edges:
            incoming_edges[edge] = incoming_edges.get(edge, 0)+1

    """
    create dict of vertices that have no incoming edges
    """
    empty = {v for v, count in incoming_edges.items() if count == 0}

    sorted_graph = []

    while empty:
        """
        pick a vertex w/ no incoming edges
        """
        v = empty.pop()
        sorted_graph.append(v)

        """
        decrement edge counts for
        edges that have connection from this vertex
        vertex.
        """

        for edge in graph.get(v, []):
            incoming_edges[edge] -= 1
            if incoming_edges[edge] == 0:
                empty.add(edge)

    cyclic_graph = [v for v, count in incoming_edges.items() if count != 0]

    """
     if there are no cyclic dependencies the above list is None
    """

    return sorted_graph, cyclic_graph
