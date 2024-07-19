import requests

url = "https://api.soundon.fm/v2/client/podcasts/511455c6-f5ee-4e8f-aac3-912b277c0efe/episodes"

headers = {
    'Api-Token': 'KilpEMLQeNzxmNBL55u5' 
}

response = requests.get(url, headers=headers )

print(response)
# print(response.json())
