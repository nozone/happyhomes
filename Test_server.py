'''
Created on Feb 27, 2016

@author: Shaq
'''
#meant to test the server

import requests

if __name__ == '__main__':
    url='http://127.0.0.1:5000/prices/'
    parameters={'lat':38.930582,
         'long':-77.030789,
         'money':50}
    
    a=requests.post(url, json={'address':"Columbia Heights, DC", "money":10})
    print a.url
    print a.status_code 
    print a.json()