from flask import request

from app.blueprints import Blueprint
from app.core.auth import Auth
from app.core.resp import Rest
from app.models import History, Record
from app.utils import client, cloudflare, domain

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/")
def client_ip_info():
    return Rest.success("Get ip info success!", client.ip.info())


@bp.route("/update")
@Auth.required
def update_record():
    name = None
    name = request.values.get("zone", name)
    name = request.values.get("host", name)
    name = request.values.get("hostname", name)

    addr = client.ip.addr()
    addr = request.values.get("ip", addr)
    addr = request.values.get("myip", addr)
    addr = request.values.get("myipv4", addr)
    addr = request.values.get("myipv6", addr)

    type = request.values.get("type", client.ip.type(addr))

    zone_name = domain.split_zone(name)
    zone_id = cloudflare.get_zone(zone_name)["id"]

    record = Record.get_or_none(
        Record.host == domain.split_host(name),
        Record.name == name,
        Record.type == type,
    )

    if record is None:
        record = Record(
            host=domain.split_host(name),
            name=name,
            type=type,
        )

        record.id = cloudflare.get_record(zone_id, record.name, record.type)["id"]
        if record.id is None:
            return Rest.error("Get record id failed!")

    # record no change
    if addr == record.content:
        return Rest.success("The current record is already latest!", record)

    # set record content is new ip_addr
    record.content = addr
    status = cloudflare.update_record(zone_id, record.id, record.name, record.type, record.content)
    history = History(
        host=record.host,
        name=record.name,
        type=record.type,
        content=record.content,
        status=status,
    )
    record.save()
    history.save()

    if status:
        return Rest.success("Update record succeed!", record)
    else:
        return Rest.error("Update record failed!")
