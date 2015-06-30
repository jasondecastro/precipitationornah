from bs4 import BeautifulSoup
from twilio.rest import TwilioRestClient
import urllib2
import schedule
import time
import json
import sqlite3

# s e t t i n g s
COUNTRIES = {"US":"united_states", "BH":"the_bahamas"}
RAINURL = 'http://willitrain.in/'+ COUNTRIES["US"] +'/'
ZIPURL = 'http://www.zipcodeapi.com/rest/nBEsSZboRZxT5UI0Qwbp612Lm3emKvu868BZ8MoZLVTRQBRH836e490rceOXKi5Q/info.json/[ZIP_CODE]/degrees'
TWILIO_ACC = "AC499b0b2477461f0b417fd79f0cc0a9b3"
TWILIO_TOKEN = "1a1f186e149af311706de4701b0e96a3"

def getLocationFromZIP(zipcode, number):
	try:
		response = urllib2.urlopen(ZIPURL.replace("[ZIP_CODE]", zipcode))
		data = json.loads(response.read())
		location = data[u"city"]
		print data
		print location
		con = sqlite3.connect('test.db')
		cur = con.cursor()
		cur.execute("insert into subscribers (phone_number, zip_code) values (?, ?)", (number, zipcode))
		con.commit()
		getRainInfo(location, number)
	except urllib2.HTTPError as e:
		print e.reason
		print ZIPURL.replace("[ZIP_CODE]", zipcode)
		print 'Invalid ZIP code'

def getRainInfo(location, number):
	response = urllib2.urlopen(RAINURL+location.replace(" ", "_"))
	data = response.read()
	soup = BeautifulSoup(data)
	result = soup.find("p", { "class" : "result" }).contents[0]
	print result

	if result == "Yes": result = True
	if result == "No": result = False

	sendTextMessage(result, number)

def sendTextMessage(toRainOrNotToRain, theirNumber):
	client = TwilioRestClient(TWILIO_ACC, TWILIO_TOKEN)
	if toRainOrNotToRain == True:
		message = client.messages.create(to="+1"+theirNumber, from_="+16463623998",
			body="Don't forget to bring an umbrella today!")
	elif toRainOrNotToRain != False:
		message = client.messages.create(to="+1"+theirNumber, from_="+16463623998",
			body="Well, aren't you lucky? It's not going to rain today!")

def getUserInfo():
	number = raw_input("What's your phone number? ").replace(" ", "")
	zipcode = raw_input("What's your ZIP code (first 5 digits)? ").replace(" ", "")
	getLocationFromZIP(zipcode, number)

def startApplication():
	getUserInfo()



if __name__ == '__main__':
	con = sqlite3.connect('test.db')
	cur = con.cursor()
	cur.execute("CREATE TABLE IF NOT EXISTS subscribers(id INTEGER PRIMARY KEY, phone_number TEXT, zip_code TEXT);")
	startApplication()
