import json
import requests
from wit import Wit

GOOGLE_GEOCODE_API_BASE     = 'https://maps.googleapis.com/maps/api/geocode/json?key='
GOOGLE_TRANSLATE_API_BASE   = 'https://www.googleapis.com/language/translate/v2?key='
GOOGLE_DETECT_API_BASE      = 'https://www.googleapis.com/language/translate/v2/detect?key='
GOOGLE_API_KEY              = 'AIzaSyCjKsqtqWQI4-C5rxQEGPTLqaVwN63UURU'
GOOGLE_TRANSLATE_API_PARAMS = '&target=en&q='
DS_API                      = 'https://api.forecast.io/forecast/04e2a312ccb44bb2c4cc196f41a681bc/' 
WIT_TOKEN                   = '26WCUF6D6T2KL6FOH2PEK2HNXDIU2EZ3'

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
