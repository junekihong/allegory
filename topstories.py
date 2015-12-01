import requests
from datetime import date
from pprint import pprint
import os,pickle

# SPECIFY YOUR API KEY AS api_key:
# api_key = "yourkeyhere"
from secret import topstories as api_key

API_ROOT = "http://api.nytimes.com/svc/topstories/v1/"
#sections = ["home","world","national","politics","nyregion","business","opinion","technology","science","health","sports","arts","fashion","dining","travel","magazine","realestate"]
section = "world"
response_format = "json"
URL = API_ROOT + section + "." + response_format + "?api-key=" + api_key

# API CALL
r = requests.get(URL)
results = r.json()
results = results["results"]


# ------------------------------------------------------------------------------

directory = str(date.today())
if not os.path.exists(directory):
    os.mkdir(directory)

    
pickle.dump(results, open(directory+"/results.p", "w"))

