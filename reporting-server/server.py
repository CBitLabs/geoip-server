"""
    Simple server to accept geo-ip requests.
"""
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/geo_ip")
def geo_ip():
    """
        Endpoint to process a geo-ip request. 
    """
    
    res = {
        'success': True,
        'lat' : request.args.get('lat'),
        'lng' : request.args.get('lng'),
        'mac_addr' : request.args.get('mac_addr'),
        'dev_id' : request.args.get('dev_id'),
        'ip' : request.remote_addr,
    }

    if not all(res.values()):
        res['success'] = False
    
    return jsonify(**res)


if __name__ == "__main__":
    DEBUG = True
    HOST = "127.0.0.1"
    PORT = 8000
    app.debug = DEBUG
    app.run(host=HOST, port=PORT)