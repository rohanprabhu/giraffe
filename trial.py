#!/usr/bin/python

'''
from lib.network.requesthelper import RequestHelper

import urllib, urllib2, cookielib

username = 'divtext_test@rohanprabhu.com'
password = 'divtext_test'

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
login_data = urllib.urlencode({'email': username, 'password': password, 'authenticity_token': 'vGneb9ojIlpowY/Nqi9gFHxus7ri+qqpmSNQoYbu93k='})
fresp = opener.open('https://dividely.com/session', login_data)
print fresp.read()
resp = opener.open('http://dividely.com')
#print resp.read()
'''
'''
x = RequestHelper.postCall(
	url="http://dividely.com/session",
	headers={},
	data="email=divtext_test@rohanprabhu.com&password=divtext_test")

print x
'''

'''
from lib.dividely.dividelymanager import DividelyManager
from lib.dividely.credentials import Credentials

import logging

dm = DividelyManager()

logging.basicConfig(level='DEBUG')

dm.add_expense(Credentials(username="divtext_test@rohanprabhu.com", password="divtext_test"),
	"Attempting from script :)", [("text2dividely@live.com", 1102)], "09/04/2013")
'''

from lib.data.datastore import DataStore

ds = DataStore()
ds.connect()

print ds.get_friends_list("rohan")
ds.add_friend("rohan", "nevermore")
print ds.get_friends_list("rohan")
ds.disconnect()
