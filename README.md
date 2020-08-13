# Experimenting with MicroPython on the ESP32

Python is my main programing language and I also want to play around embedded devices. MicroPython is therefore 
the perfect starting point. I have previously messed around with Arduinos while in college but disliked the `C` syntax. 

The aim for this repo is to document my experimentation with MicroPython and hopefully create some cool projects.

### Run your python file on the ESP32

Similar to Arduino we need to upload our files to the ESP32. I found `ampy` to be a good basic option. Adafruit have provided a 
nice [getting started with MicroPython](https://learn.adafruit.com/micropython-basics-load-files-and-run-code/install-ampy) that I strongly recommend having a look at.

The following command runs main.py on your ERP32 
```commandline
ampy --port /dev/tty.SLAB_USBtoUART run main.py
```

### Connect to WIFI

The ESP32 has built in WIFI and Bluetooth. You can easily connect to WIFI using the following function. 
Note this function has been taken from [Miguel Grinberg](https://blog.miguelgrinberg.com/post/micropython-and-the-internet-of-things-part-iv-wi-fi-and-the-cloud). 
He provides great tutorials on his blog and is the writer of [Flask Web Development](https://www.amazon.co.uk/Flask-Web-Development-Developing-Applications/dp/1449372627)

```python
import network
import time

def connect_wifi(ssid, password):
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
```

### Making requests

`urequests` can be used to make HTTP requests. When working with urequests I found it necessary to manually close the socket. 
After about 10 requests a `OSError: 23` was thrown. After some digging around it is caused by urequests 
not closing sockets. Checkout this [thread](https://forum.pycom.io/topic/1747/urequests-with-ussl-causes-an-oserror/6) for more info   

A simple fix is to wrap urequests get method as shown below.
```python

import urequests

def get(endpoint):
    res = urequests.get(endpoint)
    res.close()
    return res
```

### Sending requests to a locally running Flask server

One main reason I bought the Esp32 is to have it interfacing with a web server running on a Raspberry Pi to 
provide constant feedback of some description. A basic Flask server is provided in [app.py](iot_server/app.py).
Code to run on an ESP32 is shown in [contact_server.py](contact_server.py)

The server allows a device to register with it and assigns it a UUID to be used in later requests

```python
@app.route('/register', methods=['POST'])
def register_device():
    """
    Register device data with the server
    :return: UUID for device
    """

    device_details = {'device_id': str(uuid4()), 'register_date': str(datetime.now()), 'last_update': str(datetime.now())}
    devices.append(device_details)
    return jsonify(device_details)
``` 

The ESP32 can then register with the Flask server and update its status every 5 seconds.
**Note**: These example are very basic/

```python
if __name__ == '__main__':

    connect_wifi('some_ssid', 'some_password')

    uuid = register()
    while True:
        get(SERVER_URL.format(endpoint='status_update/{0}'.format(uuid)))
        time.sleep(5)
```