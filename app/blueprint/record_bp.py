from flask import Blueprint, current_app, jsonify, request

from app.entity.history import History
from app.entity.record import Record
from app.extension.sqlalchemy import db
from app.util.cloudflare import Cloudflare

bp = Blueprint('dns', __name__, url_prefix='/dns')

app = current_app


@bp.route("/<host>")
def update_record(host):
    # 获取客户端ip
    new_ip = request.headers.get('X-Real-IP')
    if new_ip is None:
        new_ip = request.remote_addr

    # 查询record是否存在
    record = Record.query.filter(Record.host == host).first()
    if record is None:
        record = Record()
        record.host = host
        # 拼接完整子域名
        record.name = host + "." + Cloudflare.zone_name
        # 获取record_id
        record.id = Cloudflare.get_record_id(record.name)
        db.session.add(record)
    else:
        # 若没有发送key 且需要认证
        if len(request.args) == 0 and record.key is not None:
            return jsonify({'code': -2, 'msg': 'Operation failed!'})
        else:
            if record.key is None:
                record.key = request.args.to_dict().get('key')
            elif record.key != request.args.to_dict().get('key'):
                return jsonify({'code': -2, 'msg': 'Operation failed!', })

    if new_ip != record.ip:
        record.ip = new_ip
        status = Cloudflare.update_record(record)
        record.ip = new_ip if status else record.ip
        # 记录ddns历史操作
        history = History(ip=new_ip, host=host, status=status)
        db.session.add(history)
        db.session.commit()

        return jsonify({'code': 0 if status else -1,
                        'msg': 'Operation succeed!' if status else 'Operation failed!',
                        'data': {'name': record.name, 'ip': record.ip}
                        })
    return jsonify({'code': 0,
                    'msg': 'The current record is up to date!',
                    'data': {'name': record.name, 'ip': record.ip}
                    })
