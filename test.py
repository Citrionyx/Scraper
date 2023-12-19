import json

import requests

query = "сверло"

response = requests.get(url=f"https://mail.hoffmann-group.ru:9443/search?q={query}&limit=1000&offset=0").json()

print(json.dumps(response, ensure_ascii=False, indent=3))