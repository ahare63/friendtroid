# Imports
import json

class Origin():

    def __init__(self, name, address, weight, modality=None):
        # self.gmaps_session = gmaps_session
        self.user_name = name
        self.address = address
        self.weight = weight
        self.geocode = None

        self.modality = modality
        self.travel_dist = None
        self.time_est = None

        # 

    def get_address(self):
        return self.address

    def get_weight(self):
        return self.weight
    
    def set_weight(self, weight):
        self.weight = weight

    def get_geocode(self):
        return self.geocode

    def set_geocode(self, geocode):
        self.geocode = geocode