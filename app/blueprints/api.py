from flask import Blueprint, request

from app.core.auth import Auth
from app.core.resp import Rest
from app.models import History, Record, Zone
from app.utils import client, cloudflare, domain

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/")
def client_ip_info():
    return Rest.success("Get ip info success!", client.ip.info())


@bp.route("/update")
@Auth.token
def update_record():
    name = (
        request.values.get("hostname")
        or request.values.get("host")
        or request.values.get("domain")
        or request.values.get("record")
    )
    addr = (
        request.values.get("myipv6")
        or request.values.get("myipv4")
        or request.values.get("myip")
        or request.values.get("ip")
        or client.ip.addr()
    )
    type = request.values.get("type", client.ip.type(addr))

    # Validate required parameters
    if not name:
        return Rest.error("The record cannot be None!", status=400)
    if not type:
        return Rest.error("The IP is invalid!", status=400)
    print(name, addr, type)
    # Retrieve or create the record
    try:
        record: Record = get_or_create_record(name, type)
    except Exception as e:
        return Rest.error(str(e), status=400)

    success = update_success_status(record, addr)

    if success is None:
        return Rest.success("The current record is already up to date!", record)
    elif success is False:
        return Rest.error("Record update failed!", status=500)
    elif success:
        return Rest.success("Record update succeeded!", record)


def get_or_create_zone(name):
    zone: Zone = Zone.get_or_none(name=name)

    if not zone:
        zone_data = cloudflare.get_zone(name)
        if not zone_data:
            raise Exception(f"Failed to retrieve zone '{name}'!")
        zone = Zone.create(**zone_data)
    return zone


def get_or_create_record(name, type):
    record: Record = Record.get_or_none(name=name, type=type)
    zone = get_or_create_zone(domain.split_zone(name))

    if not record:
        record_data = cloudflare.get_record(zone.id, name, type)
        if not record_data:
            raise Exception(f"Failed to retrieve record '{name}'!")
        record = Record.create(zone=zone, **record_data)
    return record


def update_success_status(record: Record, addr):
    # Check if update is necessary
    if record.content == addr:
        return None

    # Update the record content
    record.content = addr
    success = cloudflare.update_record(
        record.zone,
        record.id,
        record.name,
        record.type,
        record.content,
    )

    # Save record and history
    record.save()
    History.create(
        name=record.name,
        type=record.type,
        content=record.content,
        success=success,
        record=record,
    )
    return success
