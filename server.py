"""
    Simple server to accept geo-ip requests.
"""

from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, make_response
from sqlalchemy.dialects import postgresql
from pygeocoder import Geocoder, GeocoderError
from time import mktime
from constants import *

import humanize
import datetime
import json
import os

import util

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
    
    lat = db.Column(db.Float())
    lng = db.Column(db.Float())
    loc = db.Column(db.String(250))
    
    bssid = db.Column(db.String(80))
    ssid = db.Column(db.String(80))
    uuid = db.Column(db.String(80))

    ip = db.Column(db.String(80))#postgresql.INET)
    remote_addr = db.Column(db.String(80))#postgresql.INET)
    
    datasrc = db.Column(db.String(80))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, **kwargs):
        self.lat = kwargs['lat']
        self.lng = kwargs['lng']
        self.loc =  GeoIP._reverse_geo(self.lat, self.lng)

        self.bssid = kwargs['bssid']
        self.ssid = kwargs['ssid']
        self.uuid = kwargs['uuid']
        
        self.ip = kwargs['ip']
        self.remote_addr = kwargs.get("remote_addr", request.remote_addr)
        self.datasrc = kwargs['datasrc']

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @staticmethod
    def _reverse_geo(lat, lng):
        try:
            return Geocoder.reverse_geocode(lat, lng).formatted_address
        except GeocoderError:
            return NO_LOCATION

    def as_clean_json(self):
        as_dict = self.as_dict()
        
        transforms = [
            ('created_at_human', lambda geoip: humanize.naturaltime(geoip['created_at'])),
            ('created_at', lambda geoip: str(geoip['created_at'])),
        ]

        util.apply_transforms(transforms, as_dict)
        return as_dict

    def __repr__(self):
        return str(self.as_dict())

@app.route("/add", methods=["GET", "POST"])
def add():
    """
        Endpoint to process a geo-ip request.
        Input values: {
            'lat' : req,
            'lng' : req,
            'ip' : req,
            'bssid' : req,
            'ssid' : req,
            'uuid' : req,
        }
    """
    
    data = _get_data()
    res = {key : data.get(key) for key in REQ_KEYS}
    res = _process_res(res, HTTP)
    
    return jsonify(**res)

@app.route("/dnsadd", methods=["GET", "POST"])
def dns_add():
    """
        Endpoint to process dns forwarding
    """
    data = _get_data()
    res = util.parse_dns(data)
    res = _process_res(res, DNS)
    with open("/home/ubuntu/log", 'w') as f:
        f.write(str(data))
        f.write(str(res))
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
        
    return data

def _process_res(res, src):
    transforms = [
        ('lat', lambda d: util.atof(d['lat'])),
        ('lng', lambda d: util.atof(d['lng'])),
    ]

    util.apply_transforms(transforms, res)
    success = _is_valid(res)
    res["success"] = success
    res["datasrc"] = src

    if success:
        res = _write_db(res)

    return res

def _is_valid(res):
    for k, v in res.iteritems():
        if v is None:
            return False
    return True

def _write_db(d):
    geoip_obj = GeoIP(**d)
    db.session.add(geoip_obj)
    db.session.commit()
    d.update(geoip_obj.as_dict())
    return d

@app.route("/history/<uuid>")
def history(uuid):
    page = _get_page()
    history = history_query(uuid, page)

    r = make_response(json.dumps(map(lambda geoip: geoip.as_clean_json(), history)))
    r.mimetype = 'application/json'

    return r

def history_query(uuid, page):
    return GeoIP.query.filter(GeoIP.uuid==uuid).\
        order_by(GeoIP.created_at.desc()).\
            limit(PAGE_SIZE).offset(page*PAGE_SIZE).all()

def _get_page():
    page = util.atoi(request.args.get("page"), 0)
    return max(page - 1, 0)

if __name__ == "__main__":
    host = "0.0.0.0"
    port = int(os.environ.get('PORT', 8000))
    app.run(host=host, port=port)