"""
    Simple server to accept geo-ip requests.
"""

from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
import datetime
import json
import os


def setup_app():
    app = Flask(__name__)
    app.config.from_pyfile('env.py')

    if "DATABASE_URL" in os.environ:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

    db = SQLAlchemy(app)
    return app, db

app, db = setup_app()

class GeoIP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.String(80))
    lng = db.Column(db.String(80))
    bssid = db.Column(db.String(80))
    ssid = db.Column(db.String(80))
    uuid = db.Column(db.String(80))
    ip = db.Column(db.String(80))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, **kwargs):
        self.lat = kwargs['lat']
        self.lng = kwargs['lng']
        self.bssid = kwargs['bssid']
        self.ssid = kwargs['ssid']
        self.uuid = kwargs['uuid']
        self.ip = kwargs['ip']

    def __repr__(self):
        keys = ['lat', 'lng', 'bssid', 'ssid', 'uuid', 'ip', 'created_at']
        return "{%s}" % "".join(map(lambda key : "'%s' : %s, " % (key, self.__dict__[key]), keys))

@app.route("/geoip", methods=["GET", "POST"])
def geoip():
    """
        Endpoint to process a geo-ip request. 
    """
    
    if request.method == "POST":
        data = _get_data(request)
    elif request.method == "GET":
        data = request.args


    res = {
        'success': True,
        'lat' : data.get('lat'),
        'lng' : data.get('lng'),
        'bssid' : data.get('bssid'),
        'ssid' : data.get('ssid'),
        'uuid' : data.get('uuid'),
        'ip' : request.remote_addr,
    }

    if not all(res.values()):
        res['success'] = False
    else:
        geoip_obj = GeoIP(**res)
        db.session.add(geoip_obj)
        db.session.commit()
    
    return jsonify(**res)

def _get_data(request):
    try:
        data = json.loads(request.data)
    except ValueError:
        data = {}
    return data


if __name__ == "__main__":
    host = "0.0.0.0"
    port = int(os.environ.get('PORT', 8000))
    app.run(host=host, port=port)