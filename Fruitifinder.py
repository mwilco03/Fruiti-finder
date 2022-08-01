import requests
import blackboxprotobuf
import sys

def apple_bssid(bssid):
    print(bssid)
    x = {}
    x['bssid'] = bssid
    data_bssid = f'\x12\x13\n\x11{bssid}\x18\x00\x20\01'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = '\x00\x01\x00\x05en_US\x00\x13com.apple.locationd\x00\x0a8.1.12B411\x00\x00\x00\x01\x00\x00\x00' + chr(len(data_bssid)) + data_bssid
    response = requests.post('https://gs-loc.apple.com/clls/wloc', headers=headers, data=data)
    try:
        x['lat'] = blackboxprotobuf.decode_message(response.content)[0]['2'][0]['2']['1']/10**8
        x['lon'] = blackboxprotobuf.decode_message(response.content)[0]['2'][0]['2']['2']/10**8
    except:
        x['error'] = "Not Found"
    return x

def main():
    found = apple_bssid(sys.argv[1])
    if x['error']:
        print("Nothing found.")
    else: 
        print("found " + found['bssid'] + " at https://google.com/maps/dir/" + str(found['lat']) + ',' + str(found['lon']))

if __name__=="__main__":
    main()
