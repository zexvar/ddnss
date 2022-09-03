from flask import Blueprint, current_app, jsonify, request

from app.entity.History import History
from app.entity.Record import Record
from app.exts.db import db
from app.util.CloudflareUtil import CloudflareUtil

record_bp = Blueprint('record_bp', __name__, url_prefix='/ddns')

app = current_app


@record_bp.route("/<host>")
def update_record(host):
    # 实例化工具类
    cloudflare = CloudflareUtil(current_app.config['AUTH'])
    # 获取客户端ip
    new_ip = request.remote_addr
    # 尝试获取mac值
    mac = None
    if len(request.args) != 0:
        mac = request.args.to_dict().get('mac')
    # 拼接完整子域名
    record_name = cloudflare.make_record_name(host)
    # 查询record是否存在
    record = Record.query.filter(Record.host == host).first()
    if record is None:
        key = cloudflare.get_record_id(record_name)
        record = Record(host=host, key=key, mac=mac)
        db.session.add(record)
    else:
        # mac地址认证
        if mac != record.mac:
            if record.mac is not None:
                return jsonify({'code': -2, 'msg': 'Operation failed!', })
            else:
                record.mac = mac

    if new_ip != record.ip:
        status = cloudflare.update_record(record.host, new_ip, record.key)
        record.ip = new_ip if status else record.ip
        # 记录ddns历史操作
        history = History(ip=new_ip, host=host, status=status)
        db.session.add(history)
        db.session.commit()

        return jsonify({'code': 0 if status else -1,
                        'msg': 'Operation succeed!' if status else 'Operation failed!',
                        'data': {'host': record.host, 'ip': record.ip}
                        })
    return jsonify({'code': 0,
                    'msg': 'The current record is up to date!',
                    'data': {'host': record.host, 'ip': record.ip}
                    })
