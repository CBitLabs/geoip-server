"""
    Simple server to accept geo-ip requests.
"""
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

class GeoIP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.String(80))
    lng = db.Column(db.String(80))
    bssid = db.Column(db.String(80))
    ssid = db.Column(db.String(80))
    uuid = db.Column(db.String(80))
    ip = db.Column(db.String(80))

    def __init__(self, **kwargs):
        self.lat = kwargs['lat']
        self.lng = kwargs['lng']
        self.bssid = kwargs['bssid']
        self.ssid = kwargs['ssid']
        self.uuid = kwargs['uuid']
        self.ip = kwargs['ip']

@app.route("/geoip", methods=["GET", "POST"])
def geoip():
    """
        Endpoint to process a geo-ip request. 
    """
    
    try:
        data = json.loads(request.data)
    except ValueError:
        data = {}

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


if __name__ == "__main__":
    DEBUG = True
    HOST = "0.0.0.0"
    PORT = 8000
    app.debug = DEBUG
    app.run(host=HOST, port=PORT)