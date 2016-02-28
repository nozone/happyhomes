import googlemaps
from googlemaps import client as _client
from googlemaps import convert

class GoogleDirections:

	def parseDirectionDump(self, directions):
		aggregateMap = {'distance': 'N/A', 'duration':'N/A"', 'BUS':0,'SUBWAY':0,'METRO_RAIL':0, 'steps':100000000000000, 'type':''}

		legs = directions[0]["legs"]
		print "there are " + str(len(legs)) + " legs \n"

		for leg in legs:
			print "there are " + str(len(leg["steps"])) + "steps"
			distinanceInMeters = leg["distance"]["value"]
			distanceInMiles = distinanceInMeters * 0.000621371192
			aggregateMap['distance'] = distanceInMiles
			aggregateMap['duration'] = leg["duration"]["value"]
			temp_steps=0
			temp_type=''
			temp_types={'BUS':0,'SUBWAY':0,'METRO_RAIL':0, 'HEAVY_RAIL':0}
			for step in leg["steps"]:
				if step["travel_mode"] == "TRANSIT":
					num_stops = step["transit_details"]["num_stops"]
					vehicle_type = step["transit_details"]["line"]["vehicle"]['type']
					temp_types[vehicle_type] = temp_types[vehicle_type] + num_stops
					#aggregateMap[vehicle_type] = aggregateMap[vehicle_type] + num_stops
					temp_type+=vehicle_type + ' '
					temp_steps+=1
				else:
					None
					#print "found a non-transit step"
			if temp_steps<aggregateMap['steps']:
				aggregateMap['steps']=temp_steps
				aggregateMap['type']=temp_type
				for i in temp_types:
					if i in ['BUS', 'SUBWAY', 'METRO_RAIL']:
						aggregateMap[i]=temp_types[i]
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

	def geoCodeAddress(self, client, address):
		jsonResult = client.geocode(address)
		lat = str(jsonResult[0]["geometry"]["bounds"]["northeast"]["lat"])
		lng = str(jsonResult[0]["geometry"]["bounds"]["northeast"]["lng"])
		latlng = lat + "," + lng
		return latlng

if __name__ == '__main__': 
	dctobmore=["Washington DC, Baltimore"]
	sample1=["38.918842,-77.011821", "38.906585,-77.039662"]

	client = googlemaps.Client(key="AIzaSyD6z37kjR2tSz48dTM_SOEdwduLzuwImuo")
	
	directions = client.directions(sample1[0],sample1[1], mode="transit")
	googleDirections = GoogleDirections()
	#print googleDirections.geoCodeAddress(client, "Salisbury, MD")

	aggregateData = googleDirections.parseDirectionDump(directions)

	print aggregateData
	#print googleDirections.generateCostModel(aggregateData)
