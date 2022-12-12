import json
import requests


class Cloudflare:
    headers: dict
    base_url: str
    zone_name: str

    @classmethod
    def load(cls, conf: dict):
        # close https warning
        requests.packages.urllib3.disable_warnings()

        # make token
        token = "Bearer " + conf['token']
        cls.headers = {
            "content-type": "application/json",
            "Authorization": token,
        }
        # set base_url
        cls.base_url = f"https://api.cloudflare.com/client/v4/zones/{conf['zone_id']}/dns_records/"
        cls.zone_name = conf['zone_name']

    @classmethod
    def get_record_id(cls, record_name):
        url = cls.base_url
        params = {"type": "AAAA", "name": record_name}
        try:
            resp = requests.get(url, params, headers=cls.headers, verify=False).text
            record_id = json.loads(resp)["result"][0]['id']
            return record_id
        except Exception:
            return None

    @classmethod
    def update_record(cls, record):
        # data = json.dumps(data)
        url = cls.base_url + record.id
        data = {
            "type": "AAAA",
            "content": record.ip,
            "name": record.name,
            "ttl": 60,
            "proxied": False
        }
        try:
            resp = requests.put(url, headers=cls.headers, data=json.dumps(data), verify=False).text
            status = json.loads(resp)["success"]
            return True if status else False
        except Exception:
            return False
