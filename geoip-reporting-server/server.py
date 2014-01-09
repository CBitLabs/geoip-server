"""
    Simple server to accept geo-ip requests.
"""
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

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
    
    return jsonify(**res)


if __name__ == "__main__":
    DEBUG = True
    HOST = "0.0.0.0"
    PORT = 8000
    app.debug = DEBUG
    app.run(host=HOST, port=PORT)