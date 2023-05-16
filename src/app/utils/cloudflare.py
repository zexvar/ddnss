import json
import requests
from app import config

# close https warning
requests.packages.urllib3.disable_warnings()

# read cloudflare conf
conf = config['cloudflare']

# make basic params
base_url = f"https://api.cloudflare.com/client/v4/zones/{conf['zone_id']}/dns_records/"
headers = {"content-type": "application/json", "Authorization": "Bearer " + conf['token']}
zone_name = conf['zone_name']


def get_record_name(host: str):
    return f"{host}.{zone_name}"


def get_record_id(record_name: str):
    url = base_url
    params = {"type": "AAAA", "name": record_name}
    try:
        resp = requests.get(url, params, headers=headers, verify=False).text
        record_id = json.loads(resp)["result"][0]['id']
        return record_id
    except Exception as e:
        print(e)
        return None


def update_record(record):
    # data = json.dumps(data)
    url = base_url + record.id
    data = {
        "type": "AAAA",
        "content": record.ip,
        "name": record.name,
        "ttl": 60,
        "proxied": False
    }
    try:
        resp = requests.put(url, headers=headers, data=json.dumps(data), verify=False).text
        status = json.loads(resp)["success"]
        return True if status else False
    except Exception as e:
        print(e)
        return False
