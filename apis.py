import json
import requests
import logging
from langdetect import detect
from wit import Wit
from models import UserSettings


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
                loc =  entities.get(i)[0].get('value')
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
        self.settings = 0

    
    def incomingMSG(self, body):
        entry         = body.get('entry')
        sender_id     = entry[0].get('messaging')[0].get('sender').get('id')
        message       = entry[0].get('messaging')[0].get('message')
        attachments   = message.get('attachments')
        ret           = None

        if attachments is not None:
            t = attachments[0].get('type')
            url = attachments[0].get('payload').get('url')
            self.sendAttachment(t, url)
        else:
            text = message.get('text')
            q = UserSettings.query(UserSettings.userid==111)
            r = q.fetch()                        
            self.settings = r[0].settings    
            if "reply with native language" in text.lower():
                r[0].settings = 1
                r[0].put()
                self.settings = 1
                ret = ":*"
            elif "go nuts" in text.lower():
                r[0].settings = 2
                r[0].put()
                self.settings = 2
                ret = "OK. I'm on fire now."
            elif "reply with english" in text.lower():
                r[0].settings = 0
                r[0].put()
                self.settings = 0
                ret = ":like:"
            elif "thank you" in text.lower():
                ret = "Any time baby <3"
            elif "sup poncho" in text.lower():
                ret = "Hey there"

            else:
                ret = self.getMSG(text)

        return ret
    
    def sendAttachment(self, type, payload_url):
        url     = FB_API_SENDMSG + FB_PAGE_ACCESSTOKEN
        params  = {
            'recipient':{
                'id':self.user_id
            },
            'message':{
                'attachment':{
                    'type'      :type,
                    'payload'   :{
                        "url": payload_url
                    }
                }
            }
        }
        
        print params
        rsp = requests.post(
            url, 
            headers={
                'Content-Type': 'application/json'
            },
            data=json.dumps(params)
        )

        if rsp.status_code > 200:
            logging.info('FB Chat Attachment API responded with status: ' + str(rsp.status_code) + ' (' + rsp.reason + ')')

        return ''


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
        location                = WITAPI.getIntentFromText(r, 'location')
        weather_condition       = WITAPI.getIntentFromText(r, 'weather_condition')
        weather_accessory       = WITAPI.getIntentFromText(r, 'weather_accessory')


        if location is None:
            return ERR_MSG

        ret = GCLOUD.geocode(location)
        lat = ret.get('results')[0].get('geometry').get('location').get('lat')
        lng = ret.get('results')[0].get('geometry').get('location').get('lng')
        weather = DARKSKY.getWeather(lat, lng)
        currently = weather.get('currently')
        temp = int(currently.get('temperature'))
        if language != "en":
            temp = int(round((int(temp)-32)*5/9.0))

        #hack
        current_condition = currently.get('summary').lower()
        if current_condition == "clear":
            current_condition = "sunny"

        if weather_accessory is None and weather_condition is None:
            output = "The weather in " + location + " now is " + current_condition + ". The temperature is " + str(temp) + " degree."
        else:
            if weather_condition is not None:
                if weather_condition in current_condition or weather_condition in current_condition.replace("drizzle", "rain"):
                    output = "Yes, it is. And the temperature is " + str(temp) + " degree."
                else:
                    output = "Nope. The weather in " + location + " now is " + current_condition + "."
            else:
                if "glass" in weather_accessory and "sunny" in current_condition:
                    output = "Yup 8-), bring that with you. The weather in " + location + " now is " + current_condition + "."
                elif "umbrella" in weather_accessory and "rain" in current_condition.replace("drizzle", "rain"):
                    output = "Yup, bring that with you. The weather in " + location + " now is " + current_condition + "."
                else:
                    output = "Nope. You're all good. The weather there now is " + current_condition + "."
            

        print self.settings

        if self.settings == 0:
            return output
        else:
            if language != "en":
                return GCLOUD.translate(output, language) 
            else:
                return output




