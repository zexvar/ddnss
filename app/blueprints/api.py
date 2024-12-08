from flask import request

from app.blueprints import Blueprint
from app.core.auth import Auth
from app.core.resp import Rest
from app.models import History, Record, Zone
from app.utils import client, cloudflare, domain

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/")
def client_ip_info():
    return Rest.success("Get ip info success!", client.ip.info())


@bp.route("/update")
@Auth.required
def update_record():
    name = None
    name = request.values.get("domain", name)
    name = request.values.get("record", name)
    name = request.values.get("host", name)
    name = request.values.get("hostname", name)

    addr = client.ip.addr()
    addr = request.values.get("ip", addr)
    addr = request.values.get("myip", addr)
    addr = request.values.get("myipv4", addr)
    addr = request.values.get("myipv6", addr)

    type = request.values.get("type", client.ip.type(addr))

    if not name:
        return Rest.error("The host or hostname can not be none!", status=400)
    if not type:
        return Rest.error("The ip is invalid!", status=400)

    record: Record = Record.get_or_none(name=name, type=type)
    if not record:
        zone_name = domain.split_zone(name)
        zone: Zone = Zone.get_or_none(name=zone_name)
        if not zone:
            zone_dict = cloudflare.get_zone(zone_name)
            if zone_dict:
                zone = Zone.create(**zone_dict)
            else:
                return Rest.error(f"Get zone '{zone_name}' failed!", status=400)
        record_dict = cloudflare.get_record(zone.id, name, type)
        if record_dict:
            record = Record.create(**record_dict)
        return Rest.error(f"Get record '{name}' failed!", status=400)

    if record.content == addr:
        return Rest.success("The current record is already latest!", record)
    else:
        record.content = addr

    success = cloudflare.update_record(
        record.zone,
        record.id,
        record.name,
        record.type,
        record.content,
    )

    history = History(
        name=record.name,
        type=record.type,
        content=record.content,
        success=success,
        record=record,
    )
    record.save()
    history.save()

    if success:
        return Rest.success("Update record succeed!", record)
    else:
        return Rest.error("Update record failed!")
