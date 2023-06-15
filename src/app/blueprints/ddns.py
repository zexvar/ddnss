from flask import Blueprint, request

from app.extensions import db
from app.models import History, Record
from app.utils import cloudflare, ip_address, response

bp = Blueprint("ddns", __name__)


@bp.route("/")
def ip_info():
    ip = ip_address.get_ip()
    version = ip_address.version(ip)
    v4_verify = ip_address.verify_v4(ip)
    v6_verify = ip_address.verify_v6(ip)
    return response.success(
        "Get ip success!",
        {"ip": ip, "type": version, "v4_verify": v4_verify, "v6_verify": v6_verify},
    )


@bp.route("/<host>")
def update_record(host):
    # 查询当前host对应record是否存在
    record = Record.query.filter(Record.host == host).first()
    if record is None:
        record = Record()
        record.host = host
        record.name = cloudflare.get_record_name(record.host)
        record.id = cloudflare.get_record_id(record.name)
        record.key = request.args.get("key")
        if record.id is None:
            return response.error("Get record id error!")
        db.session.add(record)
    elif record.key is not None and request.args.get("key") != record.key:
        return response.error("Please check your key!")

    # 获取客户端ip
    new_ip = ip_address.get_ip()
    if new_ip != record.ip:
        record.ip = new_ip
        status = cloudflare.update_record(record)
        # 记录ddns历史操作
        db.session.add(History(ip=new_ip, host=host, status=status))
        db.session.commit()
        if status:
            return response.success(
                "Change ip succeed!", {"name": record.name, "ip": record.ip}
            )
        else:
            return response.error("Update record failed!")

    return response.success(
        "The current record ip is already latest!",
        {"name": record.name, "ip": record.ip},
    )
