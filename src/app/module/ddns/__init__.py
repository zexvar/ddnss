from flask import Blueprint, current_app, request

from app.entity.history import History
from app.entity.record import Record
from app.exts import db
from app.util import response
from . import cloudflare

bp = Blueprint('ddns', __name__, url_prefix='/ddns')


@bp.route("/<host>")
def update_record(host):
    if not cloudflare.Conf.init:
        cloudflare.init(current_app.config['cloudflare'])

    # 获取客户端ip
    new_ip = request.headers.get('X-Real-IP')
    if new_ip is None:
        new_ip = request.remote_addr

    # 查询record是否存在
    record = Record.query.filter(Record.host == host).first()
    if record is None:
        record = Record()
        record.host = host
        record.name = cloudflare.get_record_name(record.host)
        record.id = cloudflare.get_record_id(record.name)
        record.key = request.args.get('key')
        if record.id is None:
            return response.error("Get record id error!")
        db.session.add(record)
    elif record.key is not None and request.args.get('key') != record.key:
        return response.error("Please check your key!")

    if new_ip != record.ip:
        record.ip = new_ip
        status = cloudflare.update_record(record)
        # 记录ddns历史操作
        db.session.add(History(ip=new_ip, host=host, status=status))
        db.session.commit()
        if status:
            return response.success("Operation succeed!", {'name': record.name, 'ip': record.ip})
        else:
            return response.error("Update record failed!")

    return response.success("The current record is up to date!", {'name': record.name, 'ip': record.ip})
