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
import pycountry

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


GOOGLE_TRANSLATE_API_BASE   = 'https://www.googleapis.com/language/translate/v2?key='
GOOGLE_API_KEY              = 'AIzaSyCjKsqtqWQI4-C5rxQEGPTLqaVwN63UURU'
GOOGLE_TRANSLATE_API_PARAMS = '&target=en&q='

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

def translate(body):
    url = GOOGLE_TRANSLATE_API_BASE + GOOGLE_API_KEY + GOOGLE_TRANSLATE_API_PARAMS + body
    r = requests.get(url)
    ret = json.loads(r.content).get('data').get('translations')
    #logging.info(self.request)
    translatedText          = ret[0].get('translatedText')
    detectedSourceLanguage  = ret[0].get('detectedSourceLanguage')
    '''detectedSourceLanguage  = pycountry.languages.get(iso639_1_code=ret[0].get('detectedSourceLanguage')).name'''
    msg = "Did you just say \"" + translatedText + "\" in " + detectedSourceLanguage + "?"

    return msg


class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.write('MainPage')

class Guestbook(webapp2.RequestHandler):

    def get(self):
        self.response.write("get")

    def post(self):
        self.response.write("post")

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
            
            logging.info(data)
            logging.info(msg)
            body = translate(body)
            sendmsg(body, to, chatId)             

            self.response.write('')

class KikApi_SendMsg(webapp2.RequestHandler):
        def get(self):
            msg = translate(u"我要吃汉堡包")
            #sendmsg(msg)
            self.response.write(msg)


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
        logging.info('post FBApi_Webhook')
        logging.info(self.request)
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

