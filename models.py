import json
from google.appengine.ext import ndb


class UserProfile(ndb.Model):
    userid = ndb.IntegerProperty()
    settings = ndb.IntegerProperty()


def create_user():
	sandy = UserProfile(userid=111, settings=0)
	return sandy


def save_user(sandy):
	sandy_key = sandy.put()
	return sandy_key


def get_user(sandy_key):
	sandy = sandy_key.get()
	return sandy


def update_user(key, value):
	sandy_key = key.get()
	sandy.settings =  value
	sandy.put()