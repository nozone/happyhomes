'''
Created on Feb 27, 2016

@author: Shaq
'''
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse, marshal_with, fields
from Uber_cost import Uber_database
from Estimate import Estimates
from Cost_function import return_best_locations_to_live
from GoogleDirections import GoogleDirections
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
        
        locations=return_best_locations_to_live(args['lat'], args['long'], args['money'])
        return locations

    def post(self):
        content = request.get_json(force=True)
        gd = GoogleDirections()
        destLatLng = gd.geoCodeAddress(gd.establishClient(), content["address"])
        filteredHousingLocations=return_best_locations_to_live(destLatLng["lat"], destLatLng["lng"], content["money"])
        return jsonify(filteredHousingLocations)

    
api.add_resource(UberInfo, '/')

if __name__ == '__main__':
    app.run(debug=True)