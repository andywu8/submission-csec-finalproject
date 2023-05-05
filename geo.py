

from geopy.geocoders import Nominatim
from geopy import distance
import geopy.geocoders
import certifi
import ssl

def find_distance(city1, city2):
    ctx = ssl._create_unverified_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ctx

    geocoder = Nominatim(user_agent="Andy", scheme='http')
    coordinates1 = geocoder.geocode(city1)
    coordinates2 = geocoder.geocode(city2)
    lat1, long1 = (coordinates1.latitude), (coordinates1.longitude)
    lat2, long2 = (coordinates2.latitude), (coordinates2.longitude)
    city1 = (lat1, long1)
    city2 = (lat2, long2)
    # print("distance", distance.distance(city1, city2))
    return distance.distance(city1, city2)
    

     
    # return 

def find_flight_time(city1, city2):
    distance = find_distance(city1, city2)

    return float(str(distance).replace(" km", ""))/860

if __name__ == '__main__':
    city1 = "San Francisco"
    city2 = "London"
    find_distance(city1, city2)
