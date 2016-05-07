import json
import requests

GOOGLE_GEOCODE_API_BASE     = 'https://maps.googleapis.com/maps/api/geocode/json?key='
GOOGLE_TRANSLATE_API_BASE   = 'https://www.googleapis.com/language/translate/v2?key='
GOOGLE_DETECT_API_BASE      = 'https://www.googleapis.com/language/translate/v2/detect?key='
GOOGLE_API_KEY              = 'AIzaSyCjKsqtqWQI4-C5rxQEGPTLqaVwN63UURU'
GOOGLE_TRANSLATE_API_PARAMS = '&target=en&q='
DS_API                      = 'https://api.forecast.io/forecast/04e2a312ccb44bb2c4cc196f41a681bc/' 


class WITAPI:
    @staticmethod
    def parse(s):
        resp = client.message(s)
        #print resp
        return str(resp)


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
