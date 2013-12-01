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
        #print(self.visited.values())
        for key in self.graph.keys():
            self.visited[key] = False
        #print(self.visited.values())
    
    def __s_v__(self, vertex_name):
        if not (vertex_name in self.graph.keys()):
            self.graph[vertex_name] = []
            self.graph[vertex_name].append([vertex_name, 0])
            self.visited[vertex_name] = False
    
    def add_vertex(self, vertex_name, dest_name, dest_distance):
        vertex_name = vertex_name  # .upper()
        dest_name = dest_name  # .upper()
        self.__s_v__(vertex_name)
        self.__s_v__(dest_name)
        self.graph[vertex_name].append([dest_name, dest_distance])
        return self
    
    def __get_adjacent__(self, vertex_name):
        vertex_name = vertex_name  # .upper()
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
    
    def find_path(self, start, end):
        start = start  # .upper()
        # end = list(set([x.upper() for x in end]))  # list comprehension, convert tuple to list. Booyeah.
        end = end  # [x.upper() for x in end]
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
                print(shortest.head())
                print(shortest.path())
                print(end)
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

def setupdb():
    import os
    try:
        os.remove(r"C:\Users\Paul\Documents\Aptana Studio 3 Workspace\DurchDenMutterland\src\default.db")
        print("DB Deleted.")
    except:
        print("DB Not Deleted.")
    import csv
    import sqlite3
    import re
    conn = sqlite3.connect("default.db")
    c = conn.cursor()
    csvparsed = csv.reader(open('GermanRoutes.csv'))
    for row in csvparsed:
        if (row[0] == "CSV"):
            head = "current text"
            for i in range(1, len(row)):
                head += ",'" + row[i].lower() + "' text"
            # print(head)
            c.execute("CREATE TABLE graph (" + head + ")")
        else:
            line = "'" + row[0].lower() + "'"
            # print(row)
            for i in range(1, len(row)):
                # print (str(i) + " " + row[i])
                if (row[i] == "NULL"):
                    line += ",NULL"
                    continue
                kilometers = re.search(r"^\s*(\d+\.?\d*)\s*km", row[i]).group(1)
                '''if (float(kilometers) > 450):
                    line += ",NULL"
                    continue'''
                minutes = int(re.search(r"\s*(\d+)\s*mins?", row[i]).group(1))
                hours = re.search(r"(\d+)\s*hours", row[i])
                if (hours):
                    minutes += int(hours.group(1)) * 60 
                line += ",'" + str(kilometers) + ":" + str(minutes) + "'"
            # print(line)
            c.execute("INSERT INTO graph VALUES (" + line + ")")
        # print(row)
    conn.commit()
    conn.close()
    
def testdb():
    import sqlite3
    conn = sqlite3.connect("default.db")
    c = conn.cursor()
    print("---")
    for row in c.execute("SELECT * FROM graph"):
        print(row)
    print("---")
    '''for row in c.execute("SELECT koln FROM graph WHERE current='bremen'"):
        print(row[0])'''
    conn.close()
    
def purgedb(limit):
    cities = full_cities()
    import sqlite3
    conn = sqlite3.connect("default.db")
    c = conn.cursor()
    for row in cities:
        row_array = []
        for col in cities:
            dest = valFromDb(row, col)
            if (dest):
                row_array.append([col, dest])
        row_array.sort(key=lambda x: float(x[1].split(':')[0]))
        for large in row_array[limit:]:
            c.execute("UPDATE graph SET " + large[0] + "=NULL WHERE current='" + row + "'")
    conn.commit()
    conn.close()
    
def valFromDb(current_city, destination_city):
    import sqlite3
    conn = sqlite3.connect("default.db")
    c = conn.cursor()
    query_result = c.execute("SELECT " + destination_city + " FROM graph WHERE current='" + current_city + "'").fetchone()[0]
    # print(query_result)
    conn.close()
    return query_result

def full_cities():
    import csv
    first_line = [x.lower() for x in next(csv.reader(open('GermanRoutes.csv')))[1:]]
    return first_line
def dest_cities():
    import csv
    first_line = [x.lower() for x in next(csv.reader(open('Destinations.csv')))[1:]]
    return first_line

def showtime():
    # Initialize our graph
    germany = DijkstraGraph()
    # load the list of cities available
    cities_list = full_cities()
    destinations_list = dest_cities()
    # intitialize those distances (which are measured in KM in our graph)
    import re
    for a in cities_list:
        for b in cities_list:
            # print("{} to {}".format(a, b))
            info = valFromDb(a, b)
            if (info):
                germany.add_vertex(a, b, float(info.split(':')[0]))
    print(germany.find_path('kassel', ['basel_switzerland']))
    print(germany.find_path('basel_switzerland', ['kassel']))
    path = germany.find_path('berlin', destinations_list)
    print(path)
    pass
    
if (__name__ == "__main__"):
    # test()
    setupdb()
    testdb()
    purgedb(12)
    #testdb()
    showtime()
    # showtime()
