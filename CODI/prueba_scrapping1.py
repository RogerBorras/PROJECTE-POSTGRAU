# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 20:49:32 2016

@author: Alba
"""

import json
"""import requests"""
import urllib2
#api_key_angela = "AIzaSyC6nZNP58pIteBnFnejU7SeE0JnxA-gX2"
#api_key_jordina = "AIzaSyCDgZyP_DMLUmtg4KF9YEOCtneOeSSzYYs"
api_key_alba= "AIzaSyBC0KL7K-aWvcVfl4P4Ck_is4BZ8TdzSZI"
url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=" + api_key_alba +"&fields=trips(tripOption/saleTotal),trips(tripOption/slice/segment/leg/departureTime),trips(tripOption/slice/segment/leg/arrivalTime),trips(tripOption/slice/segment/leg/origin),trips(tripOption/slice/segment/leg/destination),trips(tripOption/slice/segment/leg/duration)"
headers = {'content-type': 'application/json'}

params = {
  "request": {
    "slice": [
      {
        "origin": "BCN",
        "destination": "MAD",
        "date": "2016-06-30",
        "maxStops": 0,
        "preferredCabin": "COACH"
      }
    ],
    "passengers": {
      "adultCount": 1,
      "infantInLapCount": 0,
      "infantInSeatCount": 0,
      "childCount": 0,
      "seniorCount": 0
    },
    "solutions": 1,
    "refundable": False
  }
}

jsonreq = json.dumps(params, encoding = 'utf-8')
req = urllib2.Request(url, jsonreq, {'Content-Type': 'application/json'})
flight = urllib2.urlopen(req)
response = flight.read()
flight.close()
print(response)

"""
response = requests.post(url, data=json.dumps(params), headers=headers)
data = response.json()

print data

data"""
