# Imports
import googlemaps
import json
import pprint

# Local imports
import origin


class Centroid():

    # Initialize the calculation
    def __init__(self, prefs=None, radius=500, departure_time=None, arrival_time=None):
        # Get API key
        with open("./credentials.json", "r") as f:
            credentials = json.load(f)
        self.maps_key = credentials.get("maps_api_key")
        self.gmaps_client = googlemaps.Client(key=self.maps_key)
        self.prefs = prefs
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.radius = radius

        self.origins = []
        self.lat_est = None
        self.long_est = None
        self.n_iterations = None

    # Given an address, set the latitude and longitude 
    def set_geocode(self, origin):
        # Check if we already have geocode info
        # If we do, no need to update (save an API call)
        if origin.get_geocode() is None:
            address = origin.get_address()
            geocode = googlemaps.geocoding.geocode(self.gmaps_client, address=address, language="en")
            origin.set_geocode(geocode)
        # print(vars(origin))


    # Add a new origin
    def add_origin(self, name, address, weight, modality=None):
        new_origin = origin.Origin(name, address, weight, modality)
        # print("New origin", vars(new_origin))
        self.set_geocode(new_origin)
        self.origins.append(new_origin)

    # Calculate the centroid of the locations in lat, long
    def calc_centroid(self):
        lat_sum = 0
        long_sum = 0
        weight_sum = 0
        for o in self.origins:
            weight = o.get_weight()
            weight_sum += weight
            geo = o.get_geocode()[0]
            lat_sum += weight*geo["geometry"]["location"]["lat"]
            long_sum += weight*geo["geometry"]["location"]["lng"]
        
        self.lat_est = lat_sum/weight_sum
        self.long_est = long_sum/weight_sum

        # print(self.lat_est, self.long_est)

    # Recommend places near the centroid
    def make_rec(self):
        # If we haven't calculated the centroid yet, find it
        if self.long_est is None or self.lat_est is None:
            self.calc_centroid()

        print(f"{self.lat_est},{self.long_est}")
        recs = googlemaps.places.places(self.gmaps_client, query=self.prefs, location=f'{self.lat_est},{self.long_est}')
        with open("./output.json", "w") as f:
            json.dump(recs, f, indent=2)

def main():
    test_cent = Centroid(prefs="mexican")
    test_cent.add_origin("Adam", "135 Charles St, Apt 3C, New York, NY 10014", weight=2)
    test_cent.add_origin("Three Lives & Co.", "Three Lives and Co.", weight=1)
    # test_cent.add_origin("Comedy Cellar", "Comedy Cellar", weight=1)
    # test_cent.calc_centroid()
    test_cent.make_rec()
    # import requests

    # url = "https://maps.googleapis.com/maps/api/place/queryautocomplete/json?input=coffee%20near%20me&language=en&loc=40.734348399999995,-74.00570929999999&key=AIzaSyDPhViWxkU6GddQkFyfeZ2j0p5AY01bDgY"

    # payload={}
    # headers = {}

    # response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.text)

if __name__ == "__main__":
    main()