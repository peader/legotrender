# parse the 2024lego_eol_offers.json file
import json
import os
from updateOffers import updateOffers
from telethon import TelegramClient

offerJsonFile = 'data/2024_lego_eol_offers.json'
isSkipOfferUpdate = True

async def sendResultMessage(resultMessage):
    await client.send_message('me', resultMessage)

api_id = os.getenv('telegram_api_id')
api_hash = os.getenv('telegram_api_hash')
client = TelegramClient('legotrender', api_id, api_hash)
if(not isSkipOfferUpdate):
    updateOffers(offerJsonFile)

resultMessage = []
with open(offerJsonFile, 'r') as f:
    json_data = json.load(f)

    for element in json_data:
        offers = element['offers'] 
        legosetid = element['legosetid']
        if(len(offers)) <= 1:
            continue
        if element['isRetired']:
            continue
        if offers[-1]['numOffers'] == 0:
            element['isRetired'] = True
            continue
        # if the last offer is equal to one then send a telegram message to the trends group
        if offers[-1]['numOffers'] == 1:
            # send a telegram message to the trends group            
            print('only one seller left for: ', legosetid)
            resultMessage.append('only one seller left for: ' + legosetid)
        if (offers[-1]['numOffers'] - offers[-2]['numOffers']) >= 3:
            resultMessage.append('This legoset has sold out from more than 3 sellers since last checked: ' + legosetid)
            print('This legoset has sold out from more than 3 sellers since last checked: ', legosetid)
        if(len(offers) >= 3):
            if (offers[-1]['numOffers'] > offers[-2]['numOffers'] and offers[-2]['numOffers'] > offers[-3]['numOffers']  ):
                resultMessage.append('the last 3 trend checks shows fewer sellers for' + legosetid)
                print('the last 3 trend checks shows fewer sellers for', legosetid )
with client:
    client.loop.run_until_complete(sendResultMessage("\n".join(resultMessage)))




             


