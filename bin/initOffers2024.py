import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# Load the HTML file
with open('data/2024bricks.html', 'r') as f:
    html = f.read()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find all table elements
tables = soup.find_all('table')

# Extract table data into a list of dictionaries
table_data = []
for table in tables:
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        row_dict = [col.text.strip() for col in cols]
        if len(row_dict) > 0:
            table_data.append(row_dict)

# json result var
json_result = []

for legoset in table_data:
    # Get the first element of the list and extract the number from it
    legosetid = legoset[0].split()[0]
    # get the web response for https://bricksmerge.de/legosetid
    url = "https://brickmerge.de/" + legosetid
    # get the web response for https://bricksmerge.de/legosetid
    response = requests.get(url)
    if response.status_code != 200:
        # pause for a 10 seconds and retry
        import time
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
        json_result.append({
            "isRetired": False,
            "legosetid": legosetid,
            # create an array of numoffers and date
            "offers": [{
                "numOffers": numOffers,
                "date": datetime.now().__str__()
            }]

        })



# write the json result to a file
with open('data/2024_lego_eol_offers.json', 'w') as f:
    json.dump(json_result, f)

# Print the JSON data
# print(json_data)
# print(table_data.__len__())

