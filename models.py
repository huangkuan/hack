import json
from google.appengine.ext import ndb


class UserSettings(ndb.Model):
    userid = ndb.IntegerProperty()
    settings = ndb.IntegerProperty()

