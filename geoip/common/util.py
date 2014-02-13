from common.constants import LAT, LNG, SSID, BSSID, UUID, IP


def get_test_geoip_obj(lat=LAT, lng=LNG, ssid=SSID,
                       bssid=BSSID, uuid=UUID, ip=IP):
    return {
        "lat": lat,
        "lng": lng,
        "ssid": ssid,
        "bssid": bssid,
        "uuid": uuid,
        "ip": ip,
        "remote_addr": ip
    }
