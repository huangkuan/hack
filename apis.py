import json
import requests
import logging
from langdetect import detect

from wit import Wit

ERR_MSG                     = 'My boss has not taught me that.'
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

    '''
    def incomingMSG(self, body):
        entry         = json.loads(body).get('entry')
        sender_id     = entry[0].get('messaging')[0].get('sender').get('id')
        message       = entry[0].get('messaging')[0].get('message')
        attachment    = message.get('attachment')

        if attachment is not None:
            print 'has attachment'
        else:
            text = message.get('text')
            print "no attachment"

        return ''
    '''

    def sendText(self, body):
        url     = FB_API_SENDMSG + FB_PAGE_ACCESSTOKEN
        params  = {
            'recipient':{
                'id':self.user_id
            },
            'message':{
                'text':body
            }
        }

        rsp = requests.post(
            url, 
            headers={
                'Content-Type': 'application/json'
            },
            data=json.dumps(params)
        )

        if rsp.status_code > 200:
            logging.info('FB Chat API responded with status: ' + str(rsp.status_code) + ' (' + rsp.reason + ')')
        
        return ''


    def getMSG(self, body):
        if body is None:
            return ERR_MSG

        text = body  
        language = "en"
        try:
            language = GCLOUD.detect(text)
            #language = detect(text)
        except:
            logging.info('Failed to detect language. Default to en.')

        q_en = text
        if language != "en":
            logging.info('Translating from ' + language)
            q_en = GCLOUD.translate(text)
        

        logging.info(q_en)
        r = WITAPI.parse(q_en)
        intent = WITAPI.getIntentFromText(r, 'location')
        
        if intent is None:
            return ERR_MSG

        ret = GCLOUD.geocode(intent)
        lat = ret.get('results')[0].get('geometry').get('location').get('lat')
        lng = ret.get('results')[0].get('geometry').get('location').get('lng')
        weather = DARKSKY.getWeather(lat, lng)
        currently = weather.get('currently')
        #output = "The weather is " + currently.get('summary').lower() + " right now in " + intent + ". The temperature is " + str(int(currently.get('temperature'))) + "."
        temp = int(currently.get('temperature'))
        if language != "en":
            temp = int(round((int(temp)-32)*5/9.0))

        output = "The weather in " + intent + " right now is " + currently.get('summary').lower() + ". The temperature is " + str(temp) + " degree."
        if language != "en":
            return GCLOUD.translate(output, language) 
        else:
            return output




