import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

def updateOffers(offerJsonFile):
    json_data = None
    # update the offers array for each of the leg sets
    with open(offerJsonFile, 'r') as f:
        json_data = json.load(f)
        # loop through each element in the json data
        for element in json_data:
            # get the legosetid
            legosetid = element['legosetid']
            # get the offers array
            offers = element['offers']
            url = "https://brickmerge.de/" + legosetid
            # get the web response for https://bricksmerge.de/legosetid
            response = requests.get(url)
            if response.status_code != 200:
                # pause for a 10 seconds and retry
                time.sleep(20) 
                print("Retrying", legosetid) 
                response = requests.get(url)
            if response.status_code != 200:
                # print error code
                print(legosetid, response.status_code)
                
            # check if the response was successful
            if response.status_code == 200:
                # parse the HTML content of the response
                soup = BeautifulSoup(response.content, "html.parser")
                # find the element with the id chartcontainer
                offerList = soup.find(id="ol1st")
                if offerList is None:
                    print(legosetid, "error parsing offers")
                    continue
                # count the number of div elements with class row collapse after
                numOffers = len(offerList.find_all("div", class_="row collapse"))
                # print the number of offers
                # add an entry to the json result with the legosetid, the number of offers and the date of that of those offers
                offers.append({
                        "numOffers": numOffers,
                        "date": datetime.now().__str__()
                    }
                )
            # to avoid spamming the brickmerge server will put a 20 second dely between requests
            time.sleep(20)

    with open(offerJsonFile, 'w') as f:
        json.dump(json_data, f)
    