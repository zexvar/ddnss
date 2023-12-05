import ipaddress

from flask import request


def get_ip_addr():
    # XFF ip or direct ip
    xff = request.headers.get("X-Forwarded-For")
    ip = xff.split(",")[0] if xff else request.remote_addr
    # ipv4-mapped-ipv6 to ipv4
    if ip.startswith("::ffff:"):
        ip = ip[7:]
    return ip


def get_ip_version(addr):
    try:
        return ipaddress.ip_address(addr).version
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
