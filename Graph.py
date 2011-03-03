### Matt Caldwell
### 2004

class Graph:
    """ Class representing a generic directed graph data structure. """
    
    def __init__(self):
        # Define a dictionary with vertices as the keys and adjacent vertices
        # as the values.
        
        self._adjacentVertices = {}

    def __repr__(self):
        # Allows you to specify "print <some_graph>" and prints the graph
        # as a string of vertices.
        
        return str(self._adjacentVertices)

    def __str__(self):
        # Allows you to specify "str(<some_graph>)" and returns a string
        # of vertices.
        
        return str(self._adjacentVertices)

    def add(self, vertex, adjacent=None):
        # adds transition from vertex to adjacent

        # we should only omit the adjacent parameter if the vertex has not yet
        # been added.  It is no use adding the same vertex again, without specifying
        # any adjacent vertices.  Check for this:
        
        if not adjacent:
            if self._adjacentVertices.get(vertex, None) != None:
                exc = "Ambiguous vertex.  Adjacent to 'None', yet has already been added\n"
                raise exc

        # if 'vertex' has already been added, simply add the adjacent vertex
        # to the adjacency list for 'vertex'.
        
        if self._adjacentVertices.get(vertex, False):
            self._adjacentVertices[vertex] = self._adjacentVertices[vertex] + [adjacent]

        # if 'vertex' has not yet been added, and an adjacent vertex was specified,
        # then create a new key (vertex) in the dictionary, and initiailize it with
        # a list containing the adjacent vertex only.  If an adjacent vertex was not
        # specified, then initialize the new key with an empty list.
        
        else:
            if adjacent:
                self._adjacentVertices[vertex] = [adjacent]
            else:
                self._adjacentVertices[vertex] = []


# For testing purposes only

if __name__ == "__main__":
    # Test graph implementation
    graph = Graph()
    graph.add('a','b')
    graph.add('a','c')
    graph.add('c')
    graph.add('d','e')

    # Demonstrate support for weighted graphs as well
    weightedGraph = Graph()
    weightedGraph.add('a',('b',0.2))
    weightedGraph.add('a',('c',0.4))
    print graph
    print weightedGraph
