from flask import request
from IPy import IP


def get_ip_addr():
    # proxy ip
    raw_ip = request.headers.get("X-Real-IP")
    if raw_ip is None:
        # direct ip
        raw_ip = request.remote_addr
    # convert ipv4-mapped ipv6 to ipv4
    if raw_ip.startswith("::ffff:"):
        raw_ip = raw_ip[6:]
    return raw_ip


def get_ip_version(addr):
    try:
        return IP(addr).version()
    except Exception as e:
        return 0


def get_ip_type(addr):
    match get_ip_version(addr):
        case 4:
            return "A"
        case 6:
            return "AAAA"
        case _:
            return None


def get_ip_info():
    ip_addr = get_ip_addr()
    ip_type = get_ip_type(ip_addr)
    return {
        "addr": ip_addr,
        "type": ip_type,
    }
