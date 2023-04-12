This is supposed to be a cool Amtrack routing program. 
(Currently in development)
|         |         |         |         |         |         |         |         |

Currently working extract_amtrak.py.  Want to have it change to be server-side 
database extraction and loading, for example: 
#working on separating extraction from database
def get_train_route(traincode):
    pass
def get_train_next_station(traincode):
    pass
def get_station_details(stationcode):
    pass
def get_train_details(traincode):
    pass
def get_active_stations():
    pass
def get_active_trains():
    pass
def get_station_schedule(stationcode):
    pass
def get_train_station_schedule(traincode, stationcode):
    pass

The database should have everything a client needs to look-up trains, stations,
routes, and other details about Amtrak.  The server should maintain train 
status, active station, and hardcoded routes.

Right now, it takes direction from main, but that should be a test program.

It creates a list of all possible three-letter station codes (AAA to ZZZ) then 
opens the Amtrack tracking website to find valid stations.  It stores the
station in a list (for a single code) or a dictionary of list where the key is 
the staition code.

It outputs these results to a csv file.