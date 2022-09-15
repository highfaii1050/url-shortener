from email import header
from tokenize import group
from dotenv import load_dotenv
import requests, sys, os

load_dotenv()

urlParam = sys.argv[1]

username=os.getenv('BITLY_USERNAME')
password=os.getenv('BITLY_PASSWORD')
apiUrl=os.getenv('BITLY_URL')

auth_res = requests.post(f"{apiUrl}/oauth/access_token", auth=(username, password))
if auth_res.status_code == 200:
    access_token = auth_res.content.decode()
else:
    print("[!] Cannot get access token, exiting...")
    exit()

headers = {"Authorization": f"Bearer {access_token}"}

groups_res = requests.get(f"{apiUrl}/v4/groups", headers=headers)
if groups_res.status_code == 200:
    groups_data = groups_res.json()['groups'][0]
    guid = groups_data['guid']
else:
    print("[!] Cannot get GUID, exiting...")
    exit()

shorten_res = requests.post(f"{apiUrl}/v4/shorten", json={"group_guid" : guid, "long_url": urlParam}, headers=headers)
if shorten_res.status_code == 200:
    link = shorten_res.json().get('link')
    print("Shortened URL: ", link)