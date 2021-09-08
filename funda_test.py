import requests
import time
from datetime import datetime

#get info on total pages for a url query
def  GetTotalPages(url):
    response = requests.get(url)
    if response:
        return int(response.json()["Paging"]["AantalPaginas"])

def GetRequest(url):
    response = requests.get(url)
    if response:        #return code between 200 ---> ok
        return response.json()["Objects"]    
    return None         #error in request

#returns the top 10 agents with the higher number of properties with query parameters
def TopTenMakelaars(url):
    dict_makelaars = {}    
    totPages = GetTotalPages(url)
    i = 1
    startTime = datetime.now()
    requestPerMinute = 0
    #append i to the url to request every page
    while i <= totPages:        
        seconds = datetime.now() - startTime
        #to avoid spam on the api we count the number of requests per minute,
        #if we are approaching 100 we sleep 
        if seconds.total_seconds() < 60 and requestPerMinute >= 90:
            sleepTime = 60-seconds.total_seconds()
            print("sleep a few seconds: "+str(sleepTime))         
            time.sleep(60-seconds.total_seconds())
            requestPerMinute = 0
            startTime = datetime.now()
        #everytime a minute has passed we reset the RPM counter
        elif seconds.total_seconds() >= 60:
            requestPerMinute = 0
            startTime = datetime.now()
        #if everything is normal we proceed with the request
        else:
            print("Get request: "+url+str(i))
            objects = GetRequest(url+str(i))
            requestPerMinute += 1
            print("RPM: "+str(requestPerMinute))
            print("Total seconds: "+str(seconds.total_seconds()))
            #we store all makelaars in a map with the number of properties according to the url
            if objects:
                for o in objects:
                    if not o["MakelaarNaam"] in dict_makelaars:
                        dict_makelaars[o["MakelaarNaam"]] = 1
                    else:
                        dict_makelaars[o["MakelaarNaam"]] += 1        
                i += 1
            else:
                print("Request error")

    #sort the map by value (number of properties) in desc order and keep only the first ten
    dict_makelaars = dict(sorted(dict_makelaars.items(), key=lambda item: item[1], reverse=True ) ) 
    top_ten ={key:value for key,value in list(dict_makelaars.items())[0:10]} 

    return top_ten


t = TopTenMakelaars("http://partnerapi.funda.nl/feeds/Aanbod.svc/json/ac1b0b1572524640a0ecc54de453ea9f/?type=koop&zo=/amsterdam/&page=")
print(t)
t = TopTenMakelaars("http://partnerapi.funda.nl/feeds/Aanbod.svc/json/ac1b0b1572524640a0ecc54de453ea9f/?type=koop&zo=/amsterdam/tuin/&page=")
print(t)
