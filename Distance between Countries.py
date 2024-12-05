import configparser, sys, json
import functools
from operator import itemgetter
import iso3166, geopy, requests, csv
from geopy import distance
import diskcache as dc

config = configparser.ConfigParser()
config.read("settings.cfg")

geonames_username = config.get("geonames","username")
print("Talking to Geonames as "+geonames_username)
GEONAMES_API_URL = "http://api.geonames.org/searchJSON"

cache = dc.Cache('./geo_cache')

print ("Finding largest cities in country:")
alpha3_to_city = {}
for country in iso3166.countries:
    print( "  "+country.name)
    cache_key = country.alpha3+"-geocode"
    results_text = None
    if cache.get(cache_key):
        results_text = cache.get(cache_key)
    else:
        response = requests.get(GEONAMES_API_URL,
            params={ 'country':country.alpha2,
              'q':country.name.split(",")[0],
              'username':geonames_username})
        results_text = response.content
        cache.set(cache_key,results_text)
    results = json.loads(results_text)
    try:
        cities = sorted([place for place in results['geonames'] if "PPL" in place['fcode']], key=itemgetter('population'),reverse=True)
    except KeyError:
        print ("Error! Couldn't find an fcodes")
        continue
    if len(cities)>0:
        print ("    biggest city = "+cities[0]['name'])
        alpha3_to_city[country.alpha3] = cities[0]
    else:
        print ("Error! No cities found!")

print ("Computing Distances")
distances = {}
for alpha31,city1 in alpha3_to_city.items():
    distances[alpha31] = {}
    for alpha32,city2 in alpha3_to_city.items():
        try:
            distances[alpha31][alpha32] = distance.distance(
                (city1['lat'],city1['lng']),(city2['lat'],city2['lng'])
                ).kilometers
        except ValueError:
            print ("  Could not compute distance between "+alpha31+" and "+alpha32)
            distances[alpha31][alpha32] = "?"

print("Outputting")
with open('CSV Files/distances.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    headers = [' '] + sorted(alpha3_to_city.keys())
    csvwriter.writerow(headers)
    for alpha31 in sorted(alpha3_to_city.keys()):
        row = [alpha31]
        print("  " + alpha31)
        for alpha32 in headers[1:]:
            row.append(distances[alpha31][alpha32])
        csvwriter.writerow(row)

print("Done")
