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
        # print(self.visited.values())
        for key in self.graph.keys():
            self.visited[key] = False
        # print(self.visited.values())
    
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
                '''print(shortest.head())
                print(shortest.path())
                print(end)'''
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

def setupdb():  # loadup our database with information from out CSV files.
    import os
    try:
        os.remove(r"C:\Users\Paul\Documents\Aptana Studio 3 Workspace\DurchDenMutterland\src\default.db")
        # print("DB Deleted.")
    except:
        print("DB Not Deleted.")  # this means that our db is not accessible or does not exist.
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
            c.execute("CREATE TABLE graph (" + head + ")")
        else:
            line = "'" + row[0].lower() + "'"
            for i in range(1, len(row)):
                if (row[i] == "NULL"):
                    line += ",NULL"
                    continue
                kilometers = re.search(r"^\s*(\d+\.?\d*)\s*km", row[i]).group(1)
                minutes = int(re.search(r"\s*(\d+)\s*mins?", row[i]).group(1))
                hours = re.search(r"(\d+)\s*hours", row[i])
                if (hours):
                    minutes += int(hours.group(1)) * 60 
                line += ",'" + str(kilometers) + ":" + str(minutes) + "'"
            c.execute("INSERT INTO graph VALUES (" + line + ")")
    
    csvparsed = csv.reader(open('PricelineInEuros.csv'))
    c.execute("CREATE TABLE priceline ( hotel text, price text )")  # Here is the priceline hotels in euros.
    for row in csvparsed:
        c.execute("INSERT INTO priceline VALUES ('" + row[0].lower() + "', '" + row[1] + "')")
    
    c.execute("CREATE TABLE misc ( item text, price text )")
    c.execute("INSERT INTO misc VALUES ('rolex', '6137.45')")
    c.execute("INSERT INTO misc VALUES ('marzipan', '9.92')")
    c.execute("INSERT INTO misc VALUES ('car', '187.09')")  # cost: http://goo.gl/6RBdGn
    c.execute("INSERT INTO misc VALUES ('kmpl', '19.78')")  # kmpl: http://goo.gl/9NTmqT
    c.execute("INSERT INTO misc VALUES ('diesel', '1.48')")  # diesel per liter
    c.execute("INSERT INTO misc VALUES ('castle', '40')")  # castle distance in KM
    
    full_cities = ""
    csv_full_cities = [x.lower() for x in next(csv.reader(open('GermanRoutes.csv')))[1:]]
    for i in range(0, len(csv_full_cities)):
        full_cities += '"' + csv_full_cities[i] + '"'
        if ((i + 1) < len(csv_full_cities)):
            full_cities += ", "
    full_cities = "[" + full_cities + "]"
    c.execute("INSERT INTO misc VALUES ('full_cities', '" + full_cities + "')")
    
    dest_cities = ""
    csv_dest_cities = [x.lower() for x in next(csv.reader(open('Destinations.csv')))]
    for i in range(0, len(csv_dest_cities)):
        dest_cities += '"' + csv_dest_cities[i] + '"'
        if ((i + 1) < len(csv_dest_cities)):
            dest_cities += ", "
    dest_cities = "[" + dest_cities + "]"
    c.execute("INSERT INTO misc VALUES ('dest_cities', '" + dest_cities + "')")
    
    conn.commit()
    conn.close()
    
def testdb():
    import sqlite3
    conn = sqlite3.connect("default.db")
    c = conn.cursor()
    print("---")
    for row in c.execute("SELECT * FROM graph"):
        print(row)
    for row in c.execute("SELECT * FROM priceline"):
        print(row)
    print("---")
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
    
def valFromDb(current_city, destination_city, table=None):
    if (table == None):
        table = "graph"
    import sqlite3
    conn = sqlite3.connect("default.db")
    c = conn.cursor()
    query_result = c.execute("SELECT " + destination_city + " FROM " + table + " WHERE current='" + current_city + "'").fetchone()[0]
    conn.close()
    return query_result

def hotelFromDb(city):
    import sqlite3
    conn = sqlite3.connect("default.db")
    c = conn.cursor()
    query_result = float(c.execute("SELECT price FROM priceline WHERE hotel='" + city + "'").fetchone()[0])
    conn.close()
    return query_result

def miscFromDb(misc):
    import sqlite3
    conn = sqlite3.connect("default.db")
    c = conn.cursor()
    query_result = float(c.execute("SELECT price FROM misc WHERE item='" + misc + "'").fetchone()[0])
    conn.close()
    return query_result

def full_cities():
    import sqlite3
    conn = sqlite3.connect("default.db")
    c = conn.cursor()
    query_result = eval(c.execute("SELECT price FROM misc WHERE item='full_cities'").fetchone()[0])
    conn.close()
    return query_result

def dest_cities():
    import sqlite3
    conn = sqlite3.connect("default.db")
    c = conn.cursor()
    query_result = eval(c.execute("SELECT price FROM misc WHERE item='dest_cities'").fetchone()[0])
    conn.close()
    return query_result

def showtime():
    # Initialize our graph
    germany = DijkstraGraph()
    # load the list of cities available
    cities_list = full_cities()
    destinations_list = dest_cities()
    # intitialize those distances (which are measured in KM in our graph)
    for a in cities_list:
        for b in cities_list:
            info = valFromDb(a, b)
            if (info):
                germany.add_vertex(a, b, float(info.split(':')[0]))
    path = germany.find_path('berlin', destinations_list)
    return_path = germany.find_path(path[-1][0], [path[0][0]])
    full_path = list(path + return_path[1:])
    print("Total number of cities: {}".format(len(full_path)))
    print("Cities and corisponding distances: {}".format(full_path))
    print()
    traverse_path(path, return_path[1:])

def process_city(a, b, total_time, total_dist, total_cost):
    delta = valFromDb(a, b).split(":")
    print("You travel from {} to {}".format(a.upper(), b.upper()))
    total_time += float(delta[1])
    total_dist += float(delta[0])
    print("Travel adds {} km.".format(delta[0]))
    print("It takes {} minutes.".format(delta[1]))
    if (b == "lubeck"):
        total_cost += float(miscFromDb('marzipan'))  # marzipan 13.50 in euros.
        total_time += 15  # takes about 15 minutes to take a stop and git r done.
        print("Your family takes about fifteen minutes to get 9.92 EUR's worth of marzipan.")
    elif (b == "hamburg"):
        # http://jalopnik.com/352372/the-old-elbe-river-tunnel
        # http://en.wikipedia.org/wiki/Elbe_Tunnel_(1911)
        total_dist += 0.42611  # In km, the distance under the river is 1398 ft.
        total_time += 45  # about 45 minutes or so
    elif (b == "hannover"):
        ipads = 1
        total_cost += 180 * ipads
        print("Your family stops and buys {} ipad which costs {} EUR.".format(ipads, ipads * 180))
    elif (b == "koln"):
        castle = 2 * float(miscFromDb('castle'))
        total_dist += castle
        total_time += 180
        total_cost += 1.2 * castle
        print("Your family goes to visit the castle 40 KM (there and back) Hauptbahnhof.")
        print("It takes about 3 hours to have some exploritory fun.")
        print("The taxi costs {}".format(1.2 * castle))
    elif (b == "baden_baden"):
        # http://goo.gl/p9VoT6 545 EUR for one night in a double room.
        spa_cost = hotelFromDb('spa')
        htl_cost = hotelFromDb('baden_baden')
        if ((total_time % 1440) > 720):
            print()
            print("Your family gets to the spa, but it's after mid-day.")
            print("You don't want to waste time that could be spent at the spa.")
            print("You all spend the night at a regular hotel")
            dd = (1440 - (total_time % 1440)) + 540
            print("It costs {} EUR for 1 room. It took {} hours.".format(htl_cost * 1, dd / 60))
            total_time += dd
            total_cost += htl_cost * 1
            print()
        dd = (1440 - (total_time % 1440)) + 540
        print("Your oma spends the day at the spa.")
        print("It costs {} for your oma to enjoy the day.".format(spa_cost))
        print("The family only needs one room at the hotel, this costs {}.".format(htl_cost * 1))
        print("It takes {} hours.".format(dd / 60))
        total_cost += spa_cost
        total_cost += htl_cost * 1
        total_time += dd
    elif (b == "basel_switzerland"):
        # http://goo.gl/iyoPSx rolex for 8,350.00 USD which is 6137.45 EUR.
        total_cost += miscFromDb('rolex') * 2  # I find this VERY wasteful.
        print("Your dad and opa buy two rolexes. It costs {}".format(miscFromDb('rolex') * 2))
    else:
        pass
    print()
    return total_time, total_dist, total_cost

def process_back(a, b, total_time, total_dist, total_cost):
    delta = valFromDb(a, b).split(":")
    print("You travel from {} to {}".format(a.upper(), b.upper()))
    total_time += float(delta[1])
    total_dist += float(delta[0])
    print("Travel adds {} km.".format(delta[0]))
    print("It takes {} minutes.".format(delta[1]))
    print()
    return total_time, total_dist, total_cost

def process_hotel(total_time, total_cost, b):
    if ((total_time % 1440) > 1230):  # if the current time is after 8:30PM we should go to a hotel and stay the night.
        dd = (1440 - (total_time % 1440)) + 540
        htl_cost = hotelFromDb(b) * 1
        total_time += dd
        total_cost += htl_cost
        print("It's after 8:30 PM.")
        print("Your family stays the night at a hotel until 9AM. It takes {} hours.".format(dd / 60))
        print("It costs {} for 1 room (your parents and grandparents each take a bed. You take the floor).".format(htl_cost))
        print()
    return total_time, total_cost

def traverse_path(path, return_path):
    total_time = 540  # this is 9AM in minutes.
    total_dist = 0  # 0 kilometers
    total_cost = 0  # in euros
    print("We land in " + path[0][0] + " at 9AM on Monday.")
    print("You rent a car. The policy and car with taxes costs: {}".format(miscFromDb('car')))
    total_cost += float(miscFromDb('car'))
    # a day has 1440 minutes in a day
    import datetime
    for i in range(1, len(path)):
        print(str(datetime.timedelta(minutes=total_time)))
        a = path[i - 1][0]
        b = path[i][0]
        total_time, total_cost = process_hotel(total_time, total_cost, b)
        total_time, total_dist, total_cost = process_city(a, b, total_time, total_dist, total_cost)
        total_time, total_cost = process_hotel(total_time, total_cost, b)
    for i in range(1, len(return_path)):
        print(str(datetime.timedelta(minutes=total_time)))
        a = return_path[i - 1][0]
        b = return_path[i][0]
        total_time, total_cost = process_hotel(total_time, total_cost, b)
        total_time, total_dist, total_cost = process_back(a, b, total_time, total_dist, total_cost)
        total_time, total_cost = process_hotel(total_time, total_cost, b)
    castle = 2 * float(miscFromDb("kmpl"))
    kmpl = miscFromDb("kmpl")
    diesel = miscFromDb("diesel")
    fuel_cost = (total_dist - castle) / kmpl * diesel
    print("The cost of the fuel for the car for the whole trip is: {}".format(fuel_cost))
    total_cost += fuel_cost
    print("Total time: {}, total distance: {} KM, total cost: {} EUR.".format(datetime.timedelta(minutes=total_time), total_dist, total_cost))
    
if (__name__ == "__main__"):
    setupdb()
    purgedb(8)  # empties out all but the n closest vertexes for ALL vertexes in the database
    showtime()
