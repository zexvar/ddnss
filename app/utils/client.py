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


def get_ip_type(addr):
    try:
        ip_ver = ipaddress.ip_address(addr).version
        return "A" if ip_ver == 4 else "AAAA"
    except Exception:
        return None


def get_ip_info():
    ip_addr = get_ip_addr()
    ip = ipaddress.ip_address(ip_addr)
    return {
        "addr": ip_addr,
        "type": get_ip_type(ip_addr),
        "LAN": ip.is_private,
        "XRI": request.headers.get("X-Real-Ip"),
        "XFF": request.headers.get("X-Forwarded-For"),
        "XFH": request.headers.get("X-Forwarded-Host"),
    }
