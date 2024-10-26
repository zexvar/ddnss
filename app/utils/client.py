import ipaddress

from flask import request


class ip:
    @staticmethod
    def addr(ip_header="Cf-Connecting-Ip"):
        ip = request.headers.get(ip_header)
        if not ip:
            xff = request.headers.get("X-Forwarded-For")
            ip = xff.split(",")[0] if xff else request.remote_addr

        # IPv4-mapped IPv6 to IPv4
        if ip.startswith("::ffff:"):
            ip = ip[7:]
        return ip

    @staticmethod
    def type(addr):
        try:
            ip_version = ipaddress.ip_address(addr).version
            return "A" if ip_version == 4 else "AAAA"
        except Exception:
            return None

    @classmethod
    def info(cls):
        ip_addr = cls.addr()
        ip_type = cls.type(ip_addr)
        private = ipaddress.ip_address(ip_addr).is_private
        return {
            "addr": ip_addr,
            "type": ip_type,
            "LAN": private,
            "XRI": request.headers.get("X-Real-Ip"),
            "XFF": request.headers.get("X-Forwarded-For"),
            "XFH": request.headers.get("X-Forwarded-Host"),
        }
