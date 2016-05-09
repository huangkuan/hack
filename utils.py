import json
import requests
from languages import ISO639_2


def getLanShortCode(lang):
    #get the short code of a specific language
    for k in ISO639_2:
        if ISO639_2[k].lower() == lang.lower():
            return k

    return None    
    



