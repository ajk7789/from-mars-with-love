"""
main python file for the application. This uses the NASA and Twilio APIs to
retrieve an image from NASA's Curiosity rover and send it to a specified list
of phone numbers. I have this set in my operating system's crontab to send out
a text everyday at 10:00 AM, so anyone registered in the numbers.txt file will
receive an image that Curiosity took during the previous day.

Author: Alex Kruger
"""

import requests
from twilio.rest import Client
from datetime import date, timedelta
from dotenv import load_dotenv
import os

# loads the .env file so I can use environment variables to keep my api keys safe
load_dotenv()

# filename for the text file of phone numbers
numbersFile = 'numbers.txt'

# gets my nasa api key from environment
nasa_api_key = os.getenv('NASA_API_KEY')

# gets my account SID from twilio.com/console from environment
account_sid = os.getenv('TWILIO_ACCOUNT_SID')

# gets my auth token from twilio.com/console from enviroment
auth_token  = os.getenv('TWILIO_AUTH_TOKEN')

# my twilio phone number
twilio_phone = "+18329901883"

def read_numbers():
    """
    description: reads from the numbers file and stores all phone numbers in a list
    params: None
    returns: None
    """
    
    with open(numbersFile) as f:
        content = f.readlines()
        content = [x.strip() for x in content]
        lineNum = 0
        numbers = []
        while lineNum < len(content):
            line = content[lineNum]
            if line[0] != "$":
                numbers.append(line[0:].strip())
                lineNum += 1
            else:
                lineNum += 1
    return numbers


# retrieves twilio's client object
client = Client(account_sid, auth_token)

# gets yesterday's date in YYYY-MM-DD form so it will fit nasa's query requirements
yesterday_date = date.today() - timedelta(days = 1)

# builds the string url for the query with yesterday's date and my nasa api key
url = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date={yd}&api_key={key}&camera=FHAZ'.format(yd = yesterday_date, key=nasa_api_key)

# gets the response object from the GET request
r = requests.get(url)

# parses the json response to get the jpeg for yesterday's curiosity image
photo = r.json()["photos"][1]["img_src"]

# gets the list of phone numbers
numbers = read_numbers()

# sends the text to each number
for number in numbers:
    message = client.messages.create(
        to=number, 
        from_= twilio_phone,
        body="Good morning!\n\nHere's a photo I took from yesterday's voyages.\n\n{photo}\n\nFrom mars with love,\n\n ~ Curiosity Rover".format(photo=photo))
