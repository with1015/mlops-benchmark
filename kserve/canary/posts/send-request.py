import requests
import json
import base64

with open('./test_image.jpg', 'rb') as img:
    base64_img = base64.b64encode(img.read())

host = "canary-svc.default.svc.cluster.local"
port = "8080"
url = "http://" + host + ":" + port + "/v1/models/vision:predict"

data = {"data" : base64_img.decode('utf-8')}

res = requests.post(url, data=json.dumps(data))
print(res.json())
