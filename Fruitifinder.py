import requests
import blackboxprotobuf

def apple_bssid(bssid):
    x = {}
    x['bssid'] = bssid
    data_bssid = f'\x12\x13\n\x11{bssid}\x18\x00\x20\01'
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'Accept': '*/*',
               "Accept-Charset": "utf-8",
               "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "en-us",
               'User-Agent': 'locationd/1776 CFNetwork/711.1.12 Darwin/14.0.0'
               }
    data = '\x00\x01\x00\x05en_US\x00\x13com.apple.locationd\x00\x0a8.1.12B411\x00\x00\x00\x01\x00\x00\x00' + chr(len(data_bssid)) + data_bssid
    response = requests.post('https://gs-loc.apple.com/clls/wloc', headers=headers, data=data)
    x['lat'] = blackboxprotobuf.decode_message(response.content)[0]['2'][0]['2']['1']
    x['lon'] = blackboxprotobuf.decode_message(response.content)[0]['2'][0]['2']['2']
    return x
