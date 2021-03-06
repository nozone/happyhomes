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
import operator
from flask import jsonify

def return_best_locations_to_live(lat, long, max_cost, partial_dataset=True):
    """
    Needs to be sorted by the highest recommended
    
    """
    df='zipcode_data (extended).json'
    if partial_dataset==True:
        df='zipcode_data.json'
    with open(df) as data_file:    
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
        aggregateData = googleDirections.parseDirectionDump(directions)
        google_cost=googleDirections.generateCostModel(aggregateData)
        google_travel_type=''
        transfers=0
        """
        for method in ['BUS', 'SUBWAY', 'METRO_RAIL']:
            for integ in range(aggregateData[method]):
                if google_travel_type!="":
                    google_travel_type+=" + "
                google_travel_type+=method
                
                transfers+=1
        print google_travel_type
        """
        google_travel_type=aggregateData['type']
        print google_travel_type
        transfers=aggregateData['steps']
        google_travel_distance=aggregateData['distance']
        google_travel_duration=aggregateData['duration']
        google_travel_transfers=transfers-1
        google_travel_duration=google_travel_duration/60
        
        
        #print googleDirections.geoCodeAddress(client, "Salisbury, MD")
        cost_per_duration=max_cost/30
        fits_in_cost_tolerance=True
        max_cost_per_10_minutes=max_cost
        #Price of Uber over PT
        cost_difference=uberinfo.price-google_cost
        #Duration of PT over Uber
        minute_difference=google_travel_duration-uberinfo.duration
        uber_cost_premium_for_10_minutes=99999999999
        if minute_difference>0:
            print cost_difference, minute_difference
            
            uber_cost_premium_for_10_minutes=(cost_difference/minute_difference)*10
        else:
            fits_in_cost_tolerance=False
        if uber_cost_premium_for_10_minutes>max_cost:
            fits_in_cost_tolerance=False
        
        winner='Uber'
        
        print "Cost:", google_cost,uberinfo.price
        print "Cost Tolerance:", uber_cost_premium_for_10_minutes, max_cost, fits_in_cost_tolerance
        print "Distance", google_travel_distance, uberinfo.distance
        print "Duration", google_travel_duration, uberinfo.duration
        print "Transfers", google_travel_transfers, 0
        explanation='We selected the method with the lowest cost, all else being equal'
        
        
        
        print uber
        
        
        #-1
        #-1 minutes
        #-1/-1= cost per minute
        add_payment_premium_to_description=True
        convenience_statement=" The $" + str(cost_difference) + " extra for Uber is within your price tolerance."
        
        if google_travel_transfers>9999:
            explanation="Public transit is impossible so use Uber."
            winner='Uber'
        elif google_travel_transfers>5:
            explanation="Public transit requires " + str(google_travel_transfers) + " transfers to get to work, so use Uber."
            if add_payment_premium_to_description:
                explanation = explanation + convenience_statement
            winner='Uber'
        elif google_travel_duration-uberinfo.duration>25  and fits_in_cost_tolerance==True:
            explanation="Public transportation takes " + str(google_travel_duration-uberinfo.duration)+ " minutes longer than Uber, so use Uber."
            if add_payment_premium_to_description:
                explanation = explanation + convenience_statement
            winner='Uber'
        elif uberinfo.duration-google_travel_duration>10:
            explanation="Uber takes a route " + str(uberinfo.duration-google_travel_duration) + " minutes longer than public transportation, so use public transportation."
            winner='PT'
        elif google_travel_distance-uberinfo.distance>5 and fits_in_cost_tolerance==True:
            explanation="Public transportation takes a route " +  str(google_travel_distance-uberinfo.distance) + " miles longer than Uber, so use Uber."
            if add_payment_premium_to_description:
                explanation = explanation + convenience_statement
            winner='Uber'
        elif uberinfo.distance-google_travel_distance>5:
            explanation="Uber takes a route" + str(uberinfo.distance-google_travel_distance)+  " miles longer than public transportation, so use public transportation."
            winner='PT'
        elif uberinfo.price-google_cost>15:
            if add_payment_premium_to_description==True:
                explanation="Uber costs $"+ str(uberinfo.price-google_cost) + " more than public transportation, which is more than your price tolerance, so use public transportation."
            else:
                explanation="Uber costs $"+ str(uberinfo.price-google_cost) + " more than public transportation, so use public transportation."
            winner='PT'    
        elif google_cost - uberinfo.price>0:
            explanation="Public transportation is more expensive than Uber, so use Uber."
            winner='Uber'    
        else:
            uberinfo.price-google_cost
            explanation="Uber is similar to public transportation in cost, duration, and distance. Use public transportation because it's $"+ str(uberinfo.price-google_cost) + " cheaper."
            winner='PT'    
        
            
        print explanation
        #Testing uberinfo
        
        if winner=='Uber':
            answer[i]={'living_index':data["Live"], 'rent':data["Cost"], 'best_travel_method':uberinfo.type, 'distance':uberinfo.distance, 'cost_of_best_travel_method':uberinfo.price, 'travel_duration':uberinfo.duration, 'explanation':explanation}
        else:
            answer[i]={'living_index':data["Live"], 'rent':data["Cost"], 'best_travel_method':google_travel_type, 'distance':google_travel_distance, 'cost_of_best_travel_method':google_cost, 'travel_duration':google_travel_duration, 'explanation':explanation}
        answer[i]['uber_premium_for_10_minutes']=uber_cost_premium_for_10_minutes
        print answer[i]
    for i in answer:
        print i, answer[i]
    return answer 
    #algorithm to determine the best
    
    
    
    
    max=0
    min=1000000000000000000000000
    min_living_index=1000
    max_rent=0
    max_distance=0
    max_cost_of_travel=0
    max_travel_duration=0
    for i in answer:
        
        if answer[i]['cost_of_best_travel_method']>max:
            max=answer[i]['cost_of_best_travel_method']
        if answer[i]['cost_of_best_travel_method']<min:
            min=answer[i]['cost_of_best_travel_method']
    for i in answer:
        """
        each factor weighed equally. squared to give exponetial cost 
        """
        rent=0
        living_index=100-0
        max_living_index=100-min_living_index
        distance=0
        cost_of_travel=0
        travel_duration=0
        i['secret_cost_function']= (rent/max_rent)**2 + (living_index/min_living_index) + (distance/max_distance)**2 + (cost_of_travel/max_cost_of_travel)**2 + (travel_duration/max_travel_duration)**2 + (living_index/max_living_index)**2 
 
     
    
    
    
    
    
    return  

if __name__ == '__main__':
    import json
    with open('data.json', 'w') as outfile:
        json.dump(return_best_locations_to_live(38.933958, -77.019679, 6.0, False), outfile)