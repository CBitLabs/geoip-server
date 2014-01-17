"""
    Simple server to accept geo-ip requests.
"""

from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, make_response
from pygeocoder import Geocoder, GeocoderError
from time import mktime

import humanize
import datetime
import json
import os

REQ_KEYS = ['lat', 'lng', 'bssid', 'ssid', 'uuid']


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

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def as_clean_json(self):
        as_dict = self.as_dict()

        invalid_keys = []#['id']
        
        transforms = [
            ('created_at_human', lambda geoip: humanize.naturaltime(geoip['created_at'])),
            ('loc', _reverse_geo),
            ('created_at', lambda geoip: str(geoip['created_at'])),
        ]

        _clean_dict(invalid_keys, as_dict)
        _apply_transforms(transforms, as_dict)
        return as_dict

    def __repr__(self):
        return str(self.as_dict())

def _reverse_geo(d):
    try:
        return Geocoder.reverse_geocode(float(d['lat']), float(d['lng'])).formatted_address
    except GeocoderError:
        return "No location information!"

def _clean_dict(invalid_keys, d):
    for invalid in invalid_keys:
        del d[invalid]

def _apply_transforms(transforms, d):
    for key, func in transforms:
        d[key] = func(d)


@app.route("/add", methods=["GET", "POST"])
def add():
    """
        Endpoint to process a geo-ip request. 
    """
    
    data = _get_data()

    res = {key : data.get(key) for key in REQ_KEYS}

    if not all(res.values()):
        res['success'] = False
    else:
        res['ip'] = request.remote_addr
        res['success'] = True
        geoip_obj = GeoIP(**res)
        db.session.add(geoip_obj)
        db.session.commit()
    
    return jsonify(**res)

def _get_data():

    if request.method == "POST":
        
        try:
            data = request.form
            if not len(data):
                data = json.loads(request.data)
        except ValueError:
            data = {}

    elif request.method == "GET":
        data = request.args

    print "Recieved data: ", data
        
    return data

@app.route("/history/<uuid>")
def history(uuid):
    history = GeoIP.query.filter(GeoIP.uuid==uuid).order_by(GeoIP.created_at.desc()).all()
    r = make_response(json.dumps(map(lambda geoip: geoip.as_clean_json(), history)))
    r.mimetype = 'application/json'
    return r

if __name__ == "__main__":
    host = "0.0.0.0"
    port = int(os.environ.get('PORT', 8000))
    app.run(host=host, port=port)