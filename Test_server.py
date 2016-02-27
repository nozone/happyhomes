'''
Created on Feb 27, 2016

@author: Shaq
'''
import requests

if __name__ == '__main__':
    url='http://127.0.0.1:5000/'
    parameters={'lat':38.930582,
         'long':-77.030789,
         'money':50}
    
    a=requests.get(url, data=parameters, params=parameters)
    print a.url
    print a.status_code 
    print a.json()
    """
    a=requests.put(url, params=parameters)
    print a.status_code 
    print a.json()
    """