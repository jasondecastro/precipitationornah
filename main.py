from bs4 import BeautifulSoup
import urllib2
from twilio.rest import TwilioRestClient
import schedule
import time

COUNTRY = {"US":"united_states", "BH":"the_bahamas"}
URL = 'http://willitrain.in/'+ COUNTRY["US"] +'/'

def getRainInfo(location, number):
	response = urllib2.urlopen(URL+location)
	data = response.read()
	soup = BeautifulSoup(data)
	result = soup.find("p", { "class" : "result" }).contents[0]
	print result

	if result == "Yes": result = True
	if result == "No": result = False

	sendTextMessage(result, number)

def sendTextMessage(toRainOrNotToRain, theirNumber):
	account = "AC499b0b2477461f0b417fd79f0cc0a9b3"
	token = "1a1f186e149af311706de4701b0e96a3"
	client = TwilioRestClient(account, token)

	if toRainOrNotToRain:
		message = client.messages.create(to="+1"+theirNumber, from_="+16463623998",
			body="Don't forget to bring an umbrella today!")

def getNumber():
	number = raw_input("What's your phone number? ").replace(" ", "")
	getLocation(number)

def getLocation(number):
	location = raw_input("What city are you in? ").replace(" ", "_")
	getRainInfo(location, number)

def startApplication():
	getNumber()

if __name__ == '__main__':
	startApplication()