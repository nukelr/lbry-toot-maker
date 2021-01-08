import requests
import json 
import yaml
from pathlib import Path
from mastodon import Mastodon
import time

yaml_file = open("config.yaml", 'r')
yaml_content = yaml.load(yaml_file)
api_url = yaml_content["api_url"]
username = yaml_content["username"]
password = yaml_content["password"]
channelId = yaml_content["channelID"]

if Path('lbrytooter_client.sec').is_file():
	try:
		mastodon = Mastodon(client_id = 'lbrytooter_client.sec', api_base_url = api_url)
	except Exception as e: 
		exit(-1)
else
	try:
		Mastodon.create_app('lbry-toot-maker', api_base_url = api_url, to_file = 'lbrytooter_client.sec')
		mastodon = Mastodon(client_id = 'lbrytooter_client.sec', api_base_url = api_url)
	except Exception as e:
		exit(-1)

if Path('lbrytooter_user.sec').is_file():
	mastodon = Mastodon( access_token = 'lbrytooter_user.sec', api_base_url = api_url)
else
	mastodon.log_in(username, password, to_file = 'lbrytooter_user.sec')
	mastodon = Mastodon( access_token = 'lbrytooter_user.sec', api_base_url = api_url)


for number_of_tries in range(5):
    try:
        json = requests.post("http://localhost:5279", json={"method": "claim_search", "params": {"channel": channelId,
                                                                                         "stream_types": ["video",
                                                                                         "document"], 
                                                                                         "order_by": ["release_time"]}}).json()
        items = json["result"]["items"]
    except:
        time.sleep(5)
        continue

    for item in items:
        claimId = item["claim_id"]
        title = item["value"]["title"]
        url = item["permanent_url"]
        name = item['name']
     
        break

    Path("last_claim_id.txt").touch()
    lastClaimId = open("last_claim_id.txt", "r").read()

    if(claimId != lastClaimId):
        try:
            mastodon.toot('Check my most recent LBRY post, join us ''https://open.lbry.com/'+ name + "#" + claimId)
            f = open("last_claim_id.txt", "w")
            f.write(claimId)
            f.close()
        except: 
            exit(-1)

    exit(0)
