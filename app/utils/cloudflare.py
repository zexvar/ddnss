import httpx

from app.settings import CONFIG

token = CONFIG.CLOUDFLARE_API_TOKEN
api_url = "https://api.cloudflare.com/client/v4"
headers = {
    "content-type": "application/json",
    "Authorization": f"Bearer {token}",
}


def get_zone(zone_name):
    url = api_url + f"/zones"
    params = {"name": zone_name}
    try:
        resp = httpx.get(url, params=params, headers=headers, verify=False).json()
        return resp["result"][0]
    except Exception as e:
        print(e)
        return None


def get_record(zone_id, record_name, record_type):
    url = api_url + f"/zones/{zone_id}/dns_records"
    params = {"name": record_name, "type": record_type}
    try:
        resp = httpx.get(url, params=params, headers=headers, verify=False).json()
        return resp["result"][0]
    except Exception as e:
        print(e)
        return None


def update_record(zone_id, record_id, record_name, record_type, record_content):
    url = api_url + f"/zones/{zone_id}/dns_records/{record_id}"
    data = {
        "name": record_name,
        "type": record_type,
        "content": record_content,
        "ttl": 60,
        "proxied": False,
    }
    try:
        resp = httpx.put(url, json=data, headers=headers, verify=False).json()
        success = resp.get("success", False)
        return success
    except Exception as e:
        print(e)
        return False
