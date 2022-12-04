#Builds dictionary list

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

#build the graph from edges connecting verticies
G = {}  # dict of tuple keys for route list
for s in station_routes:
    for r in station_routes[s]:
        #search tree with competing edge
        for search in station_routes:
            if r in station_routes[search] and s != search:
                if G[(s,search)] is null:
                    G[(s,search)] = [r]
                else:
                    G[(s,search)].append(r)
                # print(f"found matching {r} between {s} and {search}")
print(*G, sep=', ')

#create a tree from the graph by removing cycles
# undirected graph
# start with a dictionary of listed connections G
# get list of all possible routes H, where a route h is a list of nodes
query = start
connections = G[query] #value is list
# create tree where only one node exists

for (i,j) in keys(G):
    try:
        G.pop(j,i)
    except KeyError:
        continue
