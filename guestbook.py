#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START imports]
import os
import json
import jinja2
import webapp2
import logging
import requests
from apis import GCLOUD
from apis import DARKSKY
from apis import WITAPI
from apis import FBAPI
from utils import *
from gcloud import datastore





JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'
KIK_API_CONFIGURL   = 'https://api.kik.com/v1/config'
KIK_API_MSG         = 'https://api.kik.com/v1/message'
KIK_APIKEY          = '440f7eeb-d558-4a09-8ca9-d5a1cbf1513f'
KIK_USERNAME        = 'hiponcho'
KIK_SENDMSG         = 'https://kikapi-1298.appspot.com/kikapi_sendmsg'
KIK_RECEIVEMSG      = 'https://kikapi-1298.appspot.com/kikapi_receivemsg'




# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent. However, the write rate should be limited to
# ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('Guestbook', guestbook_name)

def sendmsg(body, to=None, chatId=None):
    if chatId is None:
        chatId  = '9d58dc9cc7fd994bbb575c9399e4335781ee55105d0784d7cb348f09d7337607'
    
    if to is None:
        to      = 'huangkuan'

    requests.post(
        KIK_API_MSG,
        auth=(KIK_USERNAME, KIK_APIKEY),
        headers={
            'Content-Type': 'application/json'
        },
        data=json.dumps({
            'messages': [
                {
                    'body':     body, 
                    'to':       to, 
                    'type':     'text', 
                    'chatId':   chatId,
                }
            ]
        })
    )

class MainPage(webapp2.RequestHandler):

    def get(self):
        client = datastore.Client('kikapi-1298')
        q = client.query(kind='UserProfile')
        q.add_filter('uid', '=', '12345')
        r = list(q.fetch())[0]
        print r

        #key = client.key('UserProfile')
        #u = datastore.Entity(key)
        #u.update({'mode':'0'})
        #client.put(u)
        #print u.key
        #q = client.query(kind='UserProfile', id='5629499534213120')
        #for a in q.fetch():
        #    print a

        self.response.write('MainPage')


class KikApi(webapp2.RequestHandler):
    def get(self):
        #print self.request
        logging.info('kik get api.')
        self.response.write("Testing page for Kik API GET")

    def post(self):
        #logging.info('kik post api.')
        self.response.write("Testing page for Kik API POST")

class KikApi_Config(webapp2.RequestHandler):
    def get(self):
        r = requests.get(
            KIK_API_CONFIGURL,
            auth=(KIK_USERNAME, KIK_APIKEY)
        )
        
        self.response.write(r.content)


    def post(self):
        #r = requests.post()
        r = requests.post(
            KIK_API_CONFIGURL,
            auth=(KIK_USERNAME, KIK_APIKEY),
            headers={
                'Content-Type': 'application/json'
            },
            data=json.dumps({
                "webhook": KIK_RECEIVEMSG,
                "features": {
                    "manuallySendReadReceipts": False,
                    "receiveReadReceipts": False,
                    "receiveDeliveryReceipts": False,
                    "receiveIsTyping": False
                }
            })
        )
        self.response.write(r.content)

class KikApi_ReceiveMsg(webapp2.RequestHandler):

        def get(self):
            self.response.write('')


        def post(self):
            
            data    = json.loads(self.request.body)
            msg     = data.get('messages')[0]
            body    = msg.get('body')
            to      = msg.get('from')
            chatId  = msg.get('chatId')

            r       = WITAPI.parse(body)
            intent  = WITAPI.getIntentFromText(r, 'location')
 
            #lan  = GCLOUD.detect(body)
            #body = GCLOUD.translate(body, lan)

            sendmsg(intent, to, chatId)             

            self.response.write('')

class KikApi_SendMsg(webapp2.RequestHandler):
        def get(self):
            self.response.write('')


        def post(self):
            logging.info(self.request)
            self.response.write('')

class FBApi_Webhook(webapp2.RequestHandler):
    def get(self):
        #print self.request
        logging.info('get FBApi_Webhook')
        logging.info(self.request.get('hub.verify_token'))
        self.response.write(self.request.get('hub.challenge'))


    def post(self):

        data        = json.loads(self.request.body)
        sender_id   = data.get('entry')[0].get('messaging')[0].get('sender').get('id')
        text        = data.get('entry')[0].get('messaging')[0].get('message').get('text')

        p = FBAPI(str(sender_id))
        m = p.incomingMSG(data)
        #m = p.getMSG(text)

        if m is not None:
            p.sendText(m)

        self.response.write('')


# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    #('/sign', Guestbook),
    ('/kikapi', KikApi),
    ('/kikapi_config', KikApi_Config),
    ('/kikapi_sendmsg', KikApi_SendMsg),    
    ('/kikapi_receivemsg', KikApi_ReceiveMsg),
    ('/fbapi_webhook', FBApi_Webhook),


], debug=True)
# [END app]

