import urequests
import network
import time
import ujson


def get_credentials(fname='credentials.json'):
    with open(fname) as f:
        return ujson.loads(f.read())


credentials = get_credentials()

SSID = credentials['SSID']
PASSWORD = credentials['PASSWORD']
SERVER_IP = credentials['IP']
SERVER_PORT = credentials['PORT']
SERVER_URL = 'http://{SERVER_IP}:{SERVER_PORT}/{ENDPOINT}'


def connect_wifi(ssid, password):
    """
    Connecting to the provided ssid
    :param ssid:
    :param password:
    :return:
    """
    print('Attempting to connect to {0}'.format(ssid))

    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to WiFi...')
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            time.sleep(1)
    print('Network config:', sta_if.ifconfig())


def register():
    response = urequests.get(SERVER_URL.format(SERVER_IP=SERVER_IP, SERVER_PORT=SERVER_PORT, ENDPOINT='register'))
    uuid = response.json()['device_id']
    return uuid


def get(endpoint):
    res = urequests.get(endpoint)
    res.close()
    return res


if __name__ == '__main__':
    connect_wifi(SSID, PASSWORD)
    uuid = register()

    while True:
        try:
            get(SERVER_URL.format(SERVER_IP=SERVER_IP, SERVER_PORT=SERVER_PORT,
                                  ENDPOINT='status_update/{0}'.format(uuid)))
        except:
            pass
        time.sleep(5)
