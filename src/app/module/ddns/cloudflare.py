import json
import requests


class Conf:
    init: bool = False
    base_url: str
    headers: dict
    zone_name: str


def init(conf: dict):
    # close https warning
    # requests.packages.urllib3.disable_warnings()
    Conf.init = True
    Conf.base_url = f"https://api.cloudflare.com/client/v4/zones/{conf['zone_id']}/dns_records/"
    Conf.headers = {
        "content-type": "application/json",
        "Authorization": "Bearer " + conf['token'],
    }
    Conf.zone_name = conf['zone_name']


def get_record_name(host: str):
    zone_name = Conf.zone_name
    return f"{host}.{zone_name}"


def get_record_id(record_name: str):
    url = Conf.base_url
    params = {"type": "AAAA", "name": record_name}
    try:
        resp = requests.get(url, params, headers=Conf.headers, verify=False).text
        record_id = json.loads(resp)["result"][0]['id']
        return record_id
    except Exception:
        return None


def update_record(record):
    # data = json.dumps(data)
    url = Conf.base_url + record.id
    data = {
        "type": "AAAA",
        "content": record.ip,
        "name": record.name,
        "ttl": 60,
        "proxied": False
    }
    try:
        resp = requests.put(url, headers=Conf.headers, data=json.dumps(data), verify=False).text
        status = json.loads(resp)["success"]
        return True if status else False
    except Exception:
        return False
