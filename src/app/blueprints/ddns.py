from flask import Blueprint, request

from app import app_config
from app.extensions import db
from app.models import History, Record
from app.utils import client, cloudflare, response

bp = Blueprint("ddns", __name__)

DDNS_KEY = str(app_config.get("DDNS_KEY", ""))


@bp.route("/")
def client_ip_info():
    return response.success("Get ip info success!", client.get_ip_info())


@bp.route("/<host>")
def update_record(host):
    if len(DDNS_KEY) != 0 and request.values.get("key") != DDNS_KEY:
        return response.error("Auth failed!")

    ip_info = client.get_ip_info()
    ip_addr = ip_info.get("addr")
    ip_type = ip_info.get("type")

    # 查询 host 对应 record
    record = Record.query.filter(
        db.and_(
            Record.host == host,
            Record.type == ip_type,
        )
    ).first()

    if record is None:
        record = Record(host=host, type=ip_type)
        record.name = cloudflare.get_record_name(record.host)
        record.id = cloudflare.get_record_id(record.name, record.type)
        if record.id is None:
            return response.error("Get record id failed!")

    # record no change
    if ip_addr == record.content:
        return response.success("The current record is already latest!", record)

    # set record content is new ip_addr
    record.content = ip_addr
    status = cloudflare.update_record(record.id, record.name, record.type, record.content)
    history = History(
        host=record.host,
        name=record.name,
        type=record.type,
        content=record.content,
        status=status,
    )
    db.session.add(record)
    db.session.add(history)
    db.session.commit()
    if status:
        return response.success("Update record succeed!", record)
    else:
        return response.error("Update record failed!")
