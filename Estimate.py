'''
Created on Feb 27, 2016

@author: Shaq
'''

class Estimates:
    def __init__(self, data, address_1, address_2):
        self.type=data['localized_display_name']
        self.surge=data['surge_multiplier']
        self.duration_minutes=data['duration']/60
        self.distance_miles=data['distance']
        try:
            self.price_low_estimate=data['low_estimate']
            self.price_high_estimate=data['high_estimate']
        except:
            self.price_low_estimate==None
            self.price_high_estimate==None
        if self.price_low_estimate==None or self.price_high_estimate==None:
            self.price_average=None
            self.price=None
            self.surge_price=self.price
        else:
            self.price_average=(self.price_low_estimate+self.price_high_estimate)/2

            self.price=self.price_average/self.surge
            self.surge_price=self.price*self.surge
        self.duration=self.duration_minutes
        self.distance=self.distance_miles
        self.source_lat=address_1[0]
        self.source_long=address_1[1]
        self.destination_lat=address_2[0]
        self.destination_long=address_2[1]
        
    
    def print_values(self):
        print "Estimate ", self.type,"\n----------------", "\nDistance : ", self.distance, "miles\nPrice : $", self.price, "\nPrice w/ surge : $", self.surge_price, "\nSurge : X", self.surge, "\nDistance :",self.duration, "miles\n-----------------"
    
    def json(self):
        return {'price':self.price, 'duration':self.duration, 'distance':self.distance, 'source_lat':self.source_lat, 'source_long':self.source_long, 'destination_lat':self.destination_lat, 'destination_long':self.destination_long}