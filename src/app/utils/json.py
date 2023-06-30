from datetime import date, datetime

from flask.json.provider import DefaultJSONProvider


class JSONProvider(DefaultJSONProvider):
    def default(self, o):
        if isinstance(o, date) or isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        return super().default(o)
