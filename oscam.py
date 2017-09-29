#!/usr/bin/python

import requests
from requests.auth import HTTPDigestAuth
import xmltodict

# modify this: set this to the name of your local cardreader
local_cardname = 'my-local-cardreaders-name'

# modify this: API connection details 
url      = 'http://localhost:16002/oscamapi.html?part=status'
username = 'myusername'
password = 'supers3cr3t'

# modify this: define service status by "bad" cards
ok   = '0';   # service is OK if 0 bad cards
warn = '4';   # service is WARN if greather or equal than n bad card


filtered = dict()

def receive():
  data = requests.get(url, auth=HTTPDigestAuth(username, password)).content
  data = xmltodict.parse(data)
  return data

def filter(e, filtered):
  if e['@type'] == 'p' or e['@type'] == 'r':
    filtered[e['@name']] = e['connection']['#text']



xml = receive()
for i in xml['oscam']['status']['client']:
  filter(i, filtered)


cardsTotal = len(filtered)
cardsGood = sum(1 for x in filtered.values() if x == 'CARDOK' or x == 'CONNECTED')
cardsBad = cardsTotal - cardsGood

state = 0
if cardsTotal - cardsGood >= warn:
  state = 1
if filtered[local_cardname] != 'CARDOK':
  state = 2

print '%d oscam_cards count=%d|good=%d|bad=%d %d cards, %d bad, %d good' % (state, cardsTotal, cardsGood, cardsBad, cardsTotal, cardsBad, cardsGood)
