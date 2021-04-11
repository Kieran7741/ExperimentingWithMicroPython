import urequests
import network
import time

SERVER_URL = 'http://192.168.8.103:5000/{endpoint}'


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
    response = urequests.get(SERVER_URL.format(endpoint='register'))
    uuid = response.json()['device_id']
    return uuid


def get(endpoint):
    res = urequests.get(endpoint)
    res.close()
    return res


if __name__ == '__main__':

    connect_wifi('some_ssid', 'some_password')

    uuid = register()
    while True:
        try:
            get(SERVER_URL.format(endpoint='status_update/{0}'.format(uuid)))
        except:
            pass
        time.sleep(5)
