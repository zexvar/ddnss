from IPy import IP
from flask import request


def get_ip():
    nginx_ip = request.headers.get('X-Real-IP')
    if nginx_ip is None:
        return request.remote_addr
    return nginx_ip


def version(address):
    try:
        return IP(address).version()
    except Exception as e:
        return 0


def verify_v4(ip):
    try:
        address = IP(ip)
        if str(address) == str(ip) and address.version() == 4:
            return True
        else:
            return False
    except Exception as e:
        return False


def verify_v6(ip):
    try:
        address = IP(ip)
        if str(address) == str(ip) and address.version() == 6:
            return True
        else:
            return False
    except Exception as e:
        return False
