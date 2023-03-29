'''#Builds dictionary list

class udg:
    def __init__(self):
        self.help()
    def help(self):
        print("USAGE")

# for connection.py file:
# Uses  a database of stations, trains, and schedules to map the best route
# for an Amtrack travel.

#pseudocode
startstation = 'Chicago'
endstation = 'Miami'
routes = [
    'Empire Builder',
    'California Zephyr',
    'Coast Starflight',
    'Sunset Limited',
    'City of New Orleans',
    'Lake Shore Limited',
    'Crescent',
    'Cardinal',
    'Silver Star',
    'Regional'
]
#station list with available routes
station_routes = {
    'Chicago' : (
        'Empire Builder',
        'Califoria Zephyr',
        'City of New Orleans',
        'Lake Shore Limited',
        'Cardinal'
    ),
    'San Francisco' : (
        'Califoria Zephyr',
        #'Coast Starflight' #will add when edges better implemented
    ),
    'Seattle' : (
        'Empire Builder',
        'Coast Starflight'
    ),
    'Los Angles' : (
        'Coast Starflight',
        'Sunset Limited'
    ),
    'New Orleans' : (
        'Sunset Limited',
        'City of New Orleans',
        'Crescent'
    ),
    'New York' : (
        'Lake Shore Limited',
        'Crescent',
        'Silver Star',
        #'Cardinal',    #will add when edges better implemented
        'Regional'
    ),
    'Washington, D.C.' : (
        'Cardinal',
        'Regional',
        #'Silver Star'  #will add when edges better implemented
    ),
    'Miami' : (
        'Silver Star'
    )
}

''''''#build the graph from edges connecting verticies
G = {}  # dict of tuple keys for route list
for s in station_routes:
    for r in station_routes[s]:
        #search tree with competing edge
        for search in station_routes:
            if r in station_routes[search] and s != search:
                if G[(s,search)] is None:
                    G[(s,search)] = [r]
                else:
                    G[(s,search)].append(r)
                # print(f"found matching {r} between {s} and {search}")
print(*G, sep=', ')
''''''

station_routes = {
    1 : [ 'a', 'b' ],
    2 : ['a','c'],
    3 : ['b','c','d'],
    4 : ['d']
}


#build the graph from edges
G = {}  #dict of tuple keys for route list (routes arbitrary)
for station in station_routes:   #key
    search_stations = station_routes
    search_stations.pop(station)
    for route in station_routes[station]:   #item from value (a list)
        #stop here.  How can I search a dictionary of lists? I need a better way to build this graph (hardcode for now)
        #if route in search_stations:
            #G.append
        pass
    print(f"{station} has routes " + str(station_routes[station]) )

#chatgpt output:
'''# Import the necessary libraries
import networkx as nx
import matplotlib.pyplot as plt

# Define the dictionary of stations and their routes
stations = {
    'Station1': ['Route1', 'Route2', 'Route3'],
    'Station2': ['Route1', 'Route2'],
    'Station3': ['Route2', 'Route3'],
    'Station4': ['Route1', 'Route3'],
}
# Create an empty graph
#graph = {}

# Transform stations to routes
routes = {}
for station, route_list in stations.items():
    for route in route_list:
        try:
            routes[route].add(station)
        except KeyError:
            routes[route] = {station}
print(stations)
print(routes)

graph = {}
# Add a node for each station and its corresponding routes
for route, stations in routes.items():
    #for station in stations:
    #    if route in stations.items() and station
    graph[route] = set(station)
    print(route, stations)

# Print the graph to see if it's correct
#print(graph)

# Create an empty graph
G = nx.Graph()

# Add the stations as nodes to the graph
for route, stations in routes.items():
    G.add_node(route)
    G.add_edges_from(stations)

'''# Add the routes as vectors to the graph
for route, routes in stations.items():
    for route in routes:
        G.add_edge(station, route)'''

# Draw the graph
nx.draw(G, with_labels=True)
plt.show()
#'''
'''
# importing networkx
import networkx as nx
# importing matplotlib.pyplot
import matplotlib.pyplot as plt
 
g = nx.Graph()
 
g.add_edge(1, 2)
g.add_edge(2, 3)
g.add_edge(3, 4)
g.add_edge(1, 4)
g.add_edge(1, 5)
 
nx.draw(g, with_labels = True)
plt.show()  #'''