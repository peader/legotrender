# parse the 2024lego_eol_offers.json file
import json
from updateOffers import updateOffers

offerJsonFile = 'data/2024_lego_eol_offers.json'
updateOffers(offerJsonFile)

with open(offerJsonFile, 'r') as f:
    json_data = json.load(f)

    for element in json_data:
        offers = element['offers'] 
        legosetid = element['legosetid']

        if element['isRetired']:
            continue
        if offers[-1]['numOffers'] == 0:
            element['isRetired'] = True
            continue
        # if the last offer is equal to one then send a telegram message to the trends group
        if offers[-1]['numOffers'] == 1:
            # send a telegram message to the trends group
            print('only one seller left for: ', legosetid)
        if (offers[-1] - offers[-2]) > 3:
            print('This legoset has sold out from more than 3 sellers since last checked: ', legosetid)
        if(len(offers) >= 3):
            if (offers[-1] > offers[-2] and offers[-2] > offers[-3]  ):
                print('the last 3 trend checks shows fewer sellers for', legosetid )


             


