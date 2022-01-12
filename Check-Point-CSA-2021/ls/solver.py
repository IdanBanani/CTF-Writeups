import gzip
import json
import shutil
from pprint import pprint
#flag - CSA{K1LL_MD5_A1r34dy_p1z}

import requests

url = "https://ls.csa-challenge.com/upload-zip"

payload = None
for i in ((1,2)):
    with open(f'f{i}.zip','rb') as to_upload:
            d = to_upload.read()
            payload = d

    headers = {
      'Content-Type': 'application/zip'
    }


    response = requests.request("POST", url, headers=headers, data=payload)
    if i ==1:
        output = json.loads(json.loads(response.content)['body'])
    # pprint(output)
    # print(type(output))
        pprint(output[0].splitlines())

    else:
        pprint(response.content)

# with open('commands.txt', 'rb') as f_in:
#     with gzip.open('f1.gz', 'wb') as f_out:
#         shutil.copyfileobj(f_in, f_out)


# r = requests.post(url, data=myzip)
# flag += json.loads(json.loads(r.content)['message'])['message'][0]

