import json
import requests
import logging
from langdetect import detect

from wit import Wit

GOOGLE_GEOCODE_API_BASE     = 'https://maps.googleapis.com/maps/api/geocode/json?key='
GOOGLE_TRANSLATE_API_BASE   = 'https://www.googleapis.com/language/translate/v2?key='
GOOGLE_DETECT_API_BASE      = 'https://www.googleapis.com/language/translate/v2/detect?key='
GOOGLE_API_KEY              = 'AIzaSyCjKsqtqWQI4-C5rxQEGPTLqaVwN63UURU'
GOOGLE_TRANSLATE_API_PARAMS = '&target=en&q='
DS_API                      = 'https://api.forecast.io/forecast/04e2a312ccb44bb2c4cc196f41a681bc/' 
WIT_TOKEN                   = '26WCUF6D6T2KL6FOH2PEK2HNXDIU2EZ3'
FB_API_SENDMSG              = 'https://graph.facebook.com/v2.6/me/messages?access_token='
FB_PAGE_ACCESSTOKEN         = 'EAAQvFtXCf0gBAE7M2gBGwO51pZACZAGxmcFi3eF3gNxfHygZAdqRmFZBCh78cBILqs4ZAff9YMsfRv9jKppAMZCSy1qo43FXG3BP3RtY47UBZBX059lfA0ZA7DUI8zmozR4RYLg9pSP5bDMAyYzSgRMjkT52bwZCbmgocM0myQZCUcrgZDZD'
def say(session_id, context, msg):
    print(msg)

def merge(session_id, context, entities, msg):
    return context

def error(session_id, context, e):
    print(str(e))

actions = {
    'say': say,
    'merge': merge,
    'error': error,
}

client = Wit(WIT_TOKEN, actions)

class WITAPI:
    @staticmethod
    def req(access_token, meth, path, params, **kwargs):

        rsp = requests.request(
            meth,
            'https://api.wit.ai/' + path,
            headers={
                'authorization': 'Bearer ' + access_token,
                'accept': 'application/vnd.wit.20160330+json'
            },
            params=params,
            **kwargs
        )
        
        if rsp.status_code > 200:
            logging.info('Wit responded with status: ' + str(rsp.status_code) +
                           ' (' + rsp.reason + ')')
        json = rsp.json()
        if 'error' in json:
            raise WitError('Wit responded with an error: ' + json['error'])
        return json



    @staticmethod
    def parse(s):
        resp = client.message(s)
        print resp
        return resp



    @staticmethod
    def getIntentFromText(r, i):
        outcomes = r.get('outcomes')
        for o in outcomes:
            entities = o.get('entities')
            if entities.get(i) is not None:
                loc =  entities.get('location')[0].get('value')
                return loc
        
        return None


    @staticmethod
    def getIntentFromAudio(s, i):
        return s


class DARKSKY:
    @staticmethod
    def getWeather(lat, lng):
        url = DS_API + str(lat) + ',' + str(lng)
        r = requests.get(url)
        ret = json.loads(r.content)
        return ret


class GCLOUD:

    @staticmethod
    def translate(body, language='en'):
        url = GOOGLE_TRANSLATE_API_BASE + GOOGLE_API_KEY + '&target=' + language + '&q=' + body
        r = requests.get(url)
        ret = json.loads(r.content).get('data').get('translations')
        #logging.info(self.request)
        translatedText          = ret[0].get('translatedText')
        detectedSourceLanguage  = ret[0].get('detectedSourceLanguage')
        #msg = "Did you just say \"" + translatedText + "\" in " + detectedSourceLanguage + "?"
        #return msg
        return translatedText


    @staticmethod
    def geocode(addr):
        url = GOOGLE_GEOCODE_API_BASE + GOOGLE_API_KEY + "&address=" + addr
        r = requests.get(url)
        ret = json.loads(r.content)
        return ret

    @staticmethod
    def detect(body):
        url = GOOGLE_DETECT_API_BASE + GOOGLE_API_KEY + '&q=' + body
        r = requests.get(url)
        ret = json.loads(r.content)
        print ret
        return ret.get('data').get('detections')[0][0].get('language')


class FBAPI:

    def __init__(self, id):
        self.user_id = id



    def sendMSG(self, body):
        url     = FB_API_SENDMSG + FB_PAGE_ACCESSTOKEN
        params  = {
            "recipient":{
                "id":self.user_id
            },
            "message":{
                "text":"test"
            }
        } 
        print params
        rsp = requests.request(
            'POST',
            url,
            headers={
                'Content-Type': 'application/json'
            },
            params=params,
        )

        return ''



    def getMSG(self, body):
        text = body  

        language = GCLOUD.detect(text)
        q_en = text
        if language != "en":
            logging.info('Translating from ' + language)
            q_en = GCLOUD.translate(text)
        

        logging.info(q_en)
        r = WITAPI.parse(q_en)
        intent = WITAPI.getIntentFromText(r, 'location')
        ret = GCLOUD.geocode(intent)
        print ret
        return ''
        lat = ret.get('results')[0].get('geometry').get('location').get('lat')
        lng = ret.get('results')[0].get('geometry').get('location').get('lng')
        weather = DARKSKY.getWeather(lat, lng)
        currently = weather.get('currently')
        output = "It is " + currently.get('summary').lower() + " right now in " + intent + ". The temperature is " + str(int(currently.get('temperature'))) + "."
        print output

        return output