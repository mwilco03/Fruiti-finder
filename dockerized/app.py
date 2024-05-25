import requests
import blackboxprotobuf
import re
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Check for the What3Words API key in the environment variables
use_w3 = False
W3W_API = os.getenv('W3W_API')
if W3W_API:
    use_w3 = True

def w3w_data(lat, lon):
    url = "https://api.what3words.com/v3/convert-to-3wa"
    params = {"key": W3W_API, "coordinates": f"{lat},{lon}"}
    w3w_resp = requests.get(url, params=params)
    return w3w_resp.json()

def sanitize_bssid(bssid):
    return re.match(r'^[0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5}$', bssid) is not None

def apple_bssid(bssid):
    x = {'bssid': bssid}
    data_bssid = f'\x12\x13\n\x11{bssid}\x18\x00\x20\01'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = '\x00\x01\x00\x05en_US\x00\x13com.apple.locationd\x00\x0a8.1.12B411\x00\x00\x00\x01\x00\x00\x00' + chr(len(data_bssid)) + data_bssid
    response = requests.post('https://gs-loc.apple.com/clls/wloc', headers=headers, data=data)
    try:
        decoded_response = blackboxprotobuf.decode_message(response.content)[0]
        lat = decoded_response['2'][0]['2']['1'] / 10**8
        lon = decoded_response['2'][0]['2']['2'] / 10**8
        x['lat'] = '{:.8f}'.format(lat)
        x['lon'] = '{:.8f}'.format(lon)
        x['google_maps'] = f"https://www.google.com/maps/dir/{lat},{lon}"
        if use_w3:
            x['w3'] = w3w_data(lat, lon)
    except Exception as e:
        x['error'] = f"Not Found: {e}"
    return x

@app.route('/scan', methods=['GET'])
def scan():
    bssid = request.args.get('bssid')
    if not bssid or not sanitize_bssid(bssid):
        return jsonify({"error": "Invalid BSSID format"}), 400

    try:
        data = apple_bssid(bssid)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9080)
