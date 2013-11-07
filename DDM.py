class DijkstraGraph:
    
    class __PathClass__:
        
        __counter__ = 0
        
        def __init__(self, lst):
            self.__lst__ = lst
            self.weight = 0
            self.__fifo__ = DijkstraGraph.__PathClass__.__counter__
            DijkstraGraph.__PathClass__.__counter__ += 1
            for i in range(0, len(self.__lst__)):
                self.weight += self.__lst__[i][1]
        
        def path(self):
            return list(self.__lst__)
        
        def head(self):
            return self.__lst__[-1][0]
        
        def __lt__(self, other):
            a = (self.weight, len(self.__lst__), self.__fifo__)
            b = (other.weight, len(other.__lst__), other.__fifo__)
            '''a = (self.weight, self.__fifo__)
            b = (other.weight, other.__fifo__)'''
            return a < b
    
    def __init__(self):
        self.graph = {}
        self.visited = {}
    
    def __reset_visited__(self):
        for key in self.graph.keys():
            self.visited[key] = False
    
    def __s_v__(self, vertex_name):
        if not (vertex_name in self.graph.keys()):
            self.graph[vertex_name] = []
            self.graph[vertex_name].append([vertex_name, 0])
            self.visited[vertex_name] = False
    
    def add_vertex(self, vertex_name, dest_name, dest_distance):
        vertex_name = vertex_name.upper()
        dest_name = dest_name.upper()
        self.__s_v__(vertex_name)
        self.__s_v__(dest_name)
        self.graph[vertex_name].append([dest_name, dest_distance])
        return self
    
    def __get_adjacent__(self, vertex_name):
        vertex_name = vertex_name.upper()
        self.__s_v__(vertex_name)
        '''return list(self.graph[vertex_name])'''
        self.visited[vertex_name] = True
        adj_lst = []
        adj = self.graph[vertex_name]
        for i in range(0, len(adj)):
            if (not self.visited[adj[i][0]]):
                adj_lst.append(adj[i])
        return adj_lst
    
    def __assign__(self, pq, current, adj):
        for a in adj:
            pq.put(self.__PathClass__(current + [a]))
    
    def find_path(self, start, *end):
        start = start.upper()
        end = list(set([x.upper() for x in end]))  # list comprehension, convert tuple to list. Booyeah.
        while (start in end):
            end.remove(start)
        if (not start in self.graph.keys()) or (not set(end) <= set(self.graph.keys())) or (start == end):
            return []
        self.__reset_visited__()
        from queue import PriorityQueue
        pq = PriorityQueue()
        self.__assign__(pq, [[start, 0]], self.__get_adjacent__(start))
        while not pq.empty():
            shortest = pq.get()
            if (shortest.head() in end):
                end.remove(shortest.head())
                self.__reset_visited__()
                pq = PriorityQueue()
                self.__assign__(pq, shortest.path(), [])
                if not end:
                    return shortest.path()
            self.__assign__(pq, shortest.path(), self.__get_adjacent__(shortest.head()))
        '''print("second")'''
        return []

def test():
    mdm = DijkstraGraph()  # multi-direction map
    mdm.add_vertex("a", "b", 3) \
        .add_vertex("a", "c", 6) \
        .add_vertex("c", "a", 6) \
        .add_vertex("c", "d", 3) \
        .add_vertex("d", "b", 5) \
        .add_vertex("b", "e", 1) \
        .add_vertex("e", "f", 1) \
        .add_vertex("f", "c", 2)
    print("Path from A to D, F: {}".format(mdm.find_path("A", "D", "F")))
    print("Path from A to D, F: {}".format(mdm.find_path("A", "F", "D")))
    print("Path from A to D, F: {}".format(mdm.find_path("A", "F", "F")))
    print("Path from A to D, F: {}".format(mdm.find_path("A", "D", "D")))
    print("Path from A to D, F: {}".format(mdm.find_path("A", "D", "F", "This_Is_Not_Here")))
    print("Path from A to D, F: {}".format(mdm.find_path("A", "")))
    print("Path from A to D, F: {}".format(mdm.find_path("This_Is_Not_Here", "D", "F")))
    print("Path from A to D, F: {}".format(mdm.find_path("", "D", "F")))
    print("Path from A to D, F: {}".format(mdm.find_path("", "")))
    print("Path from A to D, F: {}".format(mdm.find_path("A", "F")))
    print("Path from A to D, F: {}".format(mdm.find_path("A", "F", "A", "A", "A")))

if(__name__ == "__main__"):
    test()
