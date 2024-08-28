import requests
import json 
import sys

res = requests.get('https://api.trustedservices.intel.com/sgx/certification/v4/fmspcs')

all_data = []
all_fmpcs = json.loads(res.text)
for spec in all_fmpcs:
    res = requests.get('https://api.trustedservices.intel.com/sgx/certification/v4/tcb?fmspc='+spec['fmspc']+'&update=early')
    if res.ok == False:
        sys.exit(1)
    all_data.append(res.json())

    res = requests.get('https://api.trustedservices.intel.com/tdx/certification/v4/tcb?fmspc='+spec['fmspc']+'&update=early')
    if res.status_code == 200:
        all_data.append(res.json())
    elif res.status_code != 404:
        sys.exit(1)

print(json.dumps(all_data, indent=2))
