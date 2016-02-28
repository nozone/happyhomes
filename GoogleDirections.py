import googlemaps
from googlemaps import client as _client
import json

class GoogleDirections:

	def parseDirectionDump(self, directions):
		aggregateMap = {'BUS':0,'SUBWAY':0,'METRO_RAIL':0}

		legs = directions[0]["legs"]
		print "there are " + str(len(legs)) + " legs \n"

		for leg in legs:
			print "there are " + str(len(leg["steps"])) + "steps"
			for step in leg["steps"]:
				if step["travel_mode"] == "TRANSIT":
					num_stops = step["transit_details"]["num_stops"]
					vehicle_type = step["transit_details"]["line"]["vehicle"]['type']
					print vehicle_type
					print num_stops
					aggregateMap[vehicle_type] = aggregateMap[vehicle_type] + num_stops
				else:
					print "found a non-transit step"

		return aggregateMap


	def generateCostModel(self, aggregateMap):
		totalCost = 0

		if aggregateMap['BUS'] > 0:
			print "adding bus fee"
			totalCost += 1.75

		if aggregateMap['SUBWAY'] > 8:
			print "adding subway fee"
			totalCost += 6
		elif aggregateMap['SUBWAY'] > 0:
			print "adding subway fee"
			totalCost += 3

		return totalCost


if __name__ == '__main__': 
	dctobmore=["Washington DC, Baltimore"]
	sample1=["38.918842,-77.011821", "38.906585,-77.039662"]

	client = googlemaps.Client(key="AIzaSyD6z37kjR2tSz48dTM_SOEdwduLzuwImuo")
	directions = client.directions(sample1[0],sample1[1], mode="transit")

	googleDirections = GoogleDirections()

	aggregateData = googleDirections.parseDirectionDump(directions)

	print aggregateData
	print googleDirections.generateCostModel(aggregateData)
