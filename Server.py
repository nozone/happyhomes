'''
Created on Feb 27, 2016

@author: Shaq
'''
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse, marshal_with, fields
from Uber_cost import Uber_database
from Estimate import Estimates
from Cost_function import return_best_locations_to_live
#import request

app = Flask(__name__)
api = Api(app)
Uber_database=Uber_database()

class UberInfo(Resource):
    def get(self):
        """
        final version will output a list of places in JSON format that would be good to live
        
        
            
        
        """
        
        
        parser = reqparse.RequestParser()
        parser.add_argument('lat')
        parser.add_argument('long')
        parser.add_argument('money')
        args = parser.parse_args()
        print args['lat']
        print args['long']
        fake_lat=float(args['lat'])+1.0
        fake_long=float(args['long'])+1.0
        money=args['money']
        locations=return_best_locations_to_live(args['lat'], args['long'])
        estimate=Uber_database.get_Uber_cost_between_two_addresses([args['lat'], args['long']], [fake_lat, fake_long])
        return estimate.json()    
    
api.add_resource(UberInfo, '/')

if __name__ == '__main__':
    app.run(debug=True)