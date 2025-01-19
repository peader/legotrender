# parse the 2024lego_eol_offers.json file
import json
import os
from updateOffers import updateOffers
import smtplib 
from email.mime.text import MIMEText
import time

def sendResultMessage(resultMessage):
    # Append the github page url
    resultMessage = resultMessage + '\n\nhttps://github.com/peader/legotrender' + '\nCheck out the logic here: https://github.com/peader/legotrender/blob/b5b313eae4a8be882ca6e81f742033567ed86e36/bin/analyzeTrends.py#L47'

    subject = "Lego Trends"
    body = resultMessage
    sender = os.environ['email_sender']
    recipients = os.environ['email_recipients'].split(',')
    password = os.environ['email_password']

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
    print("email sent")

while(True):
    offerJsonFile = os.environ['offerJsonFile']
    isSkipOfferUpdate = os.getenv("isSkipOfferUpdate", 'False').lower() in ('true', '1', 't')

    if(not isSkipOfferUpdate):
        updateOffers(offerJsonFile)

    resultMessage = []
    with open(offerJsonFile, 'r') as f:
        json_data = json.load(f)

        for element in json_data:
            offers = element['offers'] 
            legosetid = element['legosetid']
            legoseturl = " https://brickmerge.de/" + legosetid
            if(len(offers)) <= 1:
                continue
            if element['isRetired']:
                continue
            if offers[-1]['numOffers'] - 1 == 0:
                element['isRetired'] = True
                continue
            # if the last offer is equal to one then send a telegram message to the trends group
            if offers[-1]['numOffers'] - 1 == 1:
                # send a telegram message to the trends group            
                print('only one seller left for: ', legosetid)
                resultMessage.append('only one seller left for: ' + legoseturl)
            if (offers[-1]['numOffers'] - 1 - offers[-2]['numOffers'] - 1) >= 3:
                resultMessage.append('This legoset has sold out from more than 3 sellers since last checked: ' + legoseturl)
                print('This legoset has sold out from more than 3 sellers since last checked: ', legosetid)
            if(len(offers) >= 3):
                trendCounter = 0
                for i in range(len(offers),1,-1):
                    if((offers[i-1]['numOffers'] - 1) >= (offers[i-2]['numOffers'] -1 )):
                        break
                    trendCounter += 1
                if (trendCounter >= 3):
                    resultMessage.append('the last ' + str(trendCounter) + ' trend checks shows fewer sellers for' + legoseturl)
                    print('the last ', str(trendCounter), '  trend checks shows fewer sellers for', legosetid )

    sendResultMessage("\n".join(resultMessage))

    time.sleep(86400)






             


