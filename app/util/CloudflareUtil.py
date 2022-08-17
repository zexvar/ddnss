import json
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class CloudflareUtil:
    def __init__(self, auth):
        self.auth = auth
        self.zone_id = auth['zone']['id']
        self.headers = {
            "X-Auth-Email": auth['email'],
            "X-Auth-Key": auth['key'],
            "content-type": "application/json"
        }

    def make_record_name(self, record_host):
        record_name = record_host + '.' + self.auth['zone']['name']
        return record_name

    def get_zone_id(self):
        url = "https://api.cloudflare.com/client/v4/zones?name" + self.auth['zone']['name']
        try:
            result = json.loads(requests.get(url, headers=self.headers, verify=False).text)
            return result["result"][0]['id']
        except Exception:
            return None

    def get_record_id(self, record_name):
        url = f"https://api.cloudflare.com/client/v4/zones/{self.zone_id}/" \
              f"dns_records?type=AAAA&name={record_name}"
        try:
            result = json.loads(requests.get(url, headers=self.headers, verify=False).text)
            return result["result"][0]['id']
        except Exception:
            return None

    def update_record(self, record_name, record_ip, record_id):
        data = {"type": "AAAA",
                "name": record_name,
                "content": record_ip,
                "ttl": 1,
                "proxied": False
                }
        data = json.dumps(data)

        url = f"https://api.cloudflare.com/client/v4/zones/{self.zone_id}/dns_records/{record_id}"
        try:
            result = json.loads(requests.put(url, headers=self.headers, data=data, verify=False).text)
            return True if result["success"] else False
        except Exception:
            return False
