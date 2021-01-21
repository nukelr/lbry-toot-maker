import requests
import json 
import yaml
from pathlib import Path
from mastodon import Mastodon
import time
import subprocess
import psutil
import logging
  
yaml_file = open("config.yaml", 'r')
yaml_content = yaml.load(yaml_file)
api_url = yaml_content["api_url"]
username = yaml_content["username"]
password = yaml_content["password"]
channelId = yaml_content["channelID"]

logging.basicConfig(filename='lbrytooter.log', format ='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO)


if "lbrynet" in (p.name() for p in psutil.process_iter()):
	logging.info("lbrynet is running...")
else:
	'''try:
		subprocess.run(["lbrynet", "start"], stdin=None, stdout=None, stderr=None, shell=False)
		logging.info("lbrynet is starting...")
	except:
		logging.error("Cannot run lbrynet")
		exit(-1)
	'''
	logging.error("lbrynet is not running")
	exit(-1)
if Path('lbrytooter_client.sec').is_file():
	try:
		mastodon = Mastodon(client_id = 'lbrytooter_client.sec', api_base_url = api_url)
	except Exception as e: 
		exit(-1)
else:
	try:
		logging.info("Creating app...")
		Mastodon.create_app('lbry-toot-maker', api_base_url = api_url, to_file = 'lbrytooter_client.sec')
		mastodon = Mastodon(client_id = 'lbrytooter_client.sec', api_base_url = api_url)
	except Exception as e:
		logging.error("Cannot Create App")
		exit(-1)

if Path('lbrytooter_user.sec').is_file():
	mastodon = Mastodon( access_token = 'lbrytooter_user.sec', api_base_url = api_url)
else:
	try:
		logging.info("logging in...")
		mastodon.log_in(username, password, to_file = 'lbrytooter_user.sec')
		mastodon = Mastodon( access_token = 'lbrytooter_user.sec', api_base_url = api_url)
	except Exception as e: 
		logging.error("Login Error")
		exit(-1)	
	



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
    logging.info("Checking last post...")
    if(claimId != lastClaimId):
        try:
            logging.info("Tooting...")
            mastodon.status_post('Posted with lbry-toot-maker. Join us on LBRY\n ' + 'https://open.lbry.com/'+ name + "#" )
            f = open("last_claim_id.txt", "w")
            f.write(claimId)
            f.close()
            logging.info(name + " with Claim ID: " + claimId + " has been tooted!")
            logging.shutdown()
        except: 
            exit(-1)
    else:
         logging.info("No new content found...exiting") 
    exit(0)
    
