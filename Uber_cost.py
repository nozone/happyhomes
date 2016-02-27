'''
Created on Feb 27, 2016

@author: Shaq
'''
from rauth import OAuth2Service
import requests
import string
import uber_rides
from uber_rides.auth import AuthorizationCodeGrant


class Uber_database:
    def __init__(self):
        self.connected_to_Uber_API=False
        #auth_flow = AuthorizationCodeGrant('JGXFGFkUm3NIeYOyJ7--cj_Kby94YG56', 'DVs-HEBsxYafTXq4aulUvZ04T8Uh3xXSimyKtvGx', YOUR_REDIRECT_URL,)
        
        
        self.uber_api = OAuth2Service(
                client_id='JGXFGFkUm3NIeYOyJ7--cj_Kby94YG56',
                client_secret='DVs-HEBsxYafTXq4aulUvZ04T8Uh3xXSimyKtvGx',
                name='HappyHome',
                authorize_url='https://login.uber.com/oauth/authorize',
                access_token_url='https://login.uber.com/oauth/token',
                base_url='https://api.uber.com/v1/',
            )
        
    
    def parameterize_location(self, location, parameters, starting=False):
        if type(location)==list:
            if starting==True:
                parameters["start_latitude"]=location[0]
                parameters["start_longitude"]=location[1]
            if starting==False:
                parameters["end_latitude"]=location[0]
                parameters["end_longitude"]=location[1]
        else:
            if starting==True:
                parameters["start_place_id"]=location
            if starting==False:
                parameters["end_place_id"]=location
        
    def get_Uber_products(self, location):
        url = 'https://api.uber.com/v1/products'

        parameters = {
            'server_token': 'tPuLpfcqHgkcbXuyoQCKKuhBfX523VMEgKT1BksX',
            'latitude': location[0],
            'longitude': location[1],
        }
        #login_url = self.uber_api.get_authorize_url(**parameters)
        response = requests.get(url, params=parameters)
        
        data = response.json()
        products=[]
        for i in data:
            for x in data[i]:
                products.append(x['display_name'])
        return products
    
    def get_Uber_estimate_test(self):
        url = 'https://api.uber.com/v1/estimates/price'
                
        parameters = {
            'server_token': 'tPuLpfcqHgkcbXuyoQCKKuhBfX523VMEgKT1BksX',
            'start_latitude': 37.775818,
            'start_longitude': -122.418028,
            'end_latitude': 36.775818,
            'end_longitude': -121.418028,
        }
        #login_url = self.uber_api.get_authorize_url(**parameters)
        print parameters
        print url
        response = requests.get(url, params=parameters)
        print response
        a=response.json()['prices']
        
        for i in a:
            if i['localized_display_name']=='uberX':
                return i['low_estimate']
        
        #for i in response:
        #    print i
        #    print "-------"
        return None
        
    def get_Uber_cost_between_two_addresses(self, address_1, address_2, product_type='uberX'):
        """
        Hits the Uber API and returns the cost.
        If you have a lat/long, make it a list:e.g.,  [37.775818, -122.418028]
        
        """
        parameters = {
            'server_token': 'tPuLpfcqHgkcbXuyoQCKKuhBfX523VMEgKT1BksX',
        }
        self.parameterize_location(address_1, parameters, True)
        self.parameterize_location(address_2, parameters, False)
        
        url = 'https://api.uber.com/v1/estimates/price'
        print parameters
        response = requests.get(url, params=parameters)
        answer=None
        if response.status_code==422:
            return "IMPOSSIBLE"

        elif response.status_code==200:
            a=response.json()
            #print a
            a=a['prices']
            for i in a:
                #e=Estimates(i, address_1, address_2)
                #e.print_values()
                if i['localized_display_name']==product_type:
                    answer=Estimates(i, address_1, address_2)
        else:
            print "ERROR IN REQUEST", response.status_code
        return answer


class Estimates:
    def __init__(self, data, address_1, address_2):
        self.type=data['localized_display_name']
        self.surge=data['surge_multiplier']
        self.duration_minutes=data['duration']/60
        self.distance_miles=data['distance']
        self.price_low_estimate=data['low_estimate']
        self.price_high_estimate=data['high_estimate']
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
        print "Uber Estimate ", self.type,"\n----------------", "\nDistance : ", self.distance, "miles\nPrice : $", self.price, "\nPrice w/ surge : $", self.surge_price, "\nSurge : X", self.surge, "\nDistance :",self.duration, "miles\n-----------------"
    
    def json(self):
        return {'price':self.price, 'duration':self.duration, 'distance':self.distance, 'source_lat':self.source_lat, 'source_long':self.source_long, 'destination_lat':self.destination_lat, 'destination_long':self.destination_long} 
        
if __name__ == '__main__':
    a = Uber_database()
    #DC Address
    print a.get_Uber_products([38.930582, -77.030789])
    estimate=a.get_Uber_cost_between_two_addresses([38.930582, -77.030789], [37.930582, -76.030789])
    #Test Address
    #estimate=a.get_Uber_cost_between_two_addresses([37.775818, -122.418028], [36.930582, -121.418028])
    print estimate.print_values()
    print estimate.json()
