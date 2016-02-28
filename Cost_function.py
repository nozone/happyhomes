'''
Created on Feb 27, 2016

@author: Shaq
'''

import json
from Uber_cost import Uber_database
import googlemaps
from googlemaps import client as _client
from googlemaps import convert
from GoogleDirections import GoogleDirections

def return_best_locations_to_live(lat, long, max_cost, partial_dataset=True):
    """
    Needs to be sorted by the highest recommended
    
    """
    data_file='zipcode_data (extended).json'
    if partial_dataset==True:
        data_file='zipcode_data.json'
    with open('zipcode_data.json') as data_file:    
        zip_code_data = json.load(data_file)
    uber=Uber_database()
    answer={}
    for i in zip_code_data:
        #Uber cost funtion
        data=zip_code_data[i]
        uberinfo=uber.get_Uber_cost_between_two_addresses([lat, long], [data['Lat'], data['Long']])
        #insert other cost function here
        
        sample1=[str(lat)+','+str(long), str(data['Lat'])+','+str(data['Long'])]

        client = googlemaps.Client(key="AIzaSyD6z37kjR2tSz48dTM_SOEdwduLzuwImuo")
        
        directions = client.directions(sample1[0],sample1[1], mode="transit")
        googleDirections = GoogleDirections()
        #print googleDirections.geoCodeAddress(client, "Salisbury, MD")
    
        aggregateData = googleDirections.parseDirectionDump(directions)
        cost=googleDirections.generateCostModel(aggregateData)
        print "Cost:", cost,uberinfo.price

        
        #Testing uberinfo
        answer[i]={'living_index':data["Live"], 'rent':data["Cost"], 'best_travel_method':uberinfo.type, 'distance':uberinfo.distance, 'cost_of_best_travel_method':uberinfo.price, 'travel_duration':uberinfo.duration}
        print answer
    #algorithm to determine the best
    max=0
    min=1000000000000000000000000
    min_living_index=1000
    max_rent=0
    max_distance=0
    max_cost_of_travel=0
    max_travel_duration=0
    for i in answer:
        
        if answer[i]['secret_cost_function']>max:
            max=['secret_cost_function']
        if answer[i]['secret_cost_function']<min:
            min=['secret_cost_function']
    for i in answer:
        """
        each factor weighed equally. squared to give exponetial cost 
        """
        rent=0
        living_index=100-living_index
        max_living_index=100-min_living_index
        distance=0
        cost_of_travel=0
        travel_duration=0
        i['secret_cost_function']= (rent/max_rent)**2 + (living_index/min_living_index) + (distance/max_distance)**2 + (cost_of_travel/max_cost_of_travel)**2 + (travel_duration/max_travel_duration)**2 + (living_index/max_living_index)**2 
 
     
    
    
    
    
    
    return  

if __name__ == '__main__':
    return_best_locations_to_live(38.930582, -77.030789, 20)