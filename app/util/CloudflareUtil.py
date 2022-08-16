import json
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class CloudflareUtil:
    auth = None
    headers = None

    def __init__(self, auth):
        self.auth = auth
        self.headers = {
            "X-Auth-Email": auth['email'],
            "X-Auth-Key": auth['key'],
            "content-type": "application/json"
        }

    def get_zone_id(self):
        url = "https://api.cloudflare.com/client/v4/zones?name" + self.auth['zone']['name']
        result = json.loads(requests.get(url, headers=self.headers).text)
        print(result["success"])
        zone_id = result["result"][0]['id']
        print(zone_id)
        return zone_id

    def get_record_id(self, record_name):
        url = f"https://api.cloudflare.com/client/v4/zones/{self.auth['zone']['id']}/" \
              f"dns_records?type=AAAA&name={record_name}"
        result = json.loads(requests.get(url, headers=self.headers).text)
        print(result["success"])
        record_id = result["result"][0]['id']
        print(record_id)
        return record_id

    def update_record(self, record_name, record_ip, record_id):
        data = {
            "type": "AAAA",
            "name": record_name,
            "content": record_ip,
            "ttl": 1,
            "proxied": False
        }
        data = json.dumps(data)

        url = f"https://api.cloudflare.com/client/v4/zones/{self.auth['zone']['id']}/dns_records/{record_id}"
        result = json.loads(requests.put(url, headers=self.headers, data=data).text)
        # print(result)
        print(result["success"])
