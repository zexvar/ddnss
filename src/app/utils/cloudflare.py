import requests

from app import config

# close https warning
requests.packages.urllib3.disable_warnings()

# read cloudflare conf
conf = config["CLOUDFLARE"]
token = conf["TOKEN"]
zone_id = conf["ZONE_ID"]
zone_name = conf["ZONE_NAME"]

# make basic params
base_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/"
headers = {"content-type": "application/json", "Authorization": "Bearer " + token}


def get_record_name(record_host):
    return f"{record_host}.{zone_name}"


def get_record_id(record_name, record_type):
    url = base_url
    params = {"name": record_name, "type": record_type}
    try:
        resp = requests.get(url, params=params, headers=headers, verify=False).json()
        record_id = resp["result"][0]["id"]
        return record_id
    except Exception as e:
        print(e)
        return None


def update_record(record_id, record_name, record_type, record_content):
    url = base_url + record_id
    data = {
        "name": record_name,
        "type": record_type,
        "content": record_content,
        "ttl": 60,
        "proxied": False,
    }

    try:
        resp = requests.put(url, json=data, headers=headers, verify=False).json()
        success = resp.get("success", False)
        return success
    except Exception as e:
        print(e)
        return False
