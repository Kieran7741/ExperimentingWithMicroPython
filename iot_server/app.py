from flask import Flask, jsonify, render_template
from uuid import uuid4
from datetime import datetime

app = Flask(__name__)
temperature_list = []
devices = []


@app.route('/submit_temp/<temp>')
def temperature(temp):
    temperature_list.append(temp)
    return str({'statue': 'ok'})


@app.route('/register')
def register_device():
    """
    Register device data with the server
    :return: UUID for device
    """

    device_details = {'device_id': str(uuid4()), 'register_date': str(datetime.now()), 'last_update': str(datetime.now())}
    devices.append(device_details)
    return jsonify(device_details)


@app.route('/')
def display_devices():
    return render_template('devices.html', devices=devices)


@app.route('/status_update/<uuid>')
def update_status(uuid):
    for device in devices:
        if device['device_id'] == uuid:
            device['last_update'] = str(datetime.now())
    return jsonify({'status': 'ok'})


@app.route('/temp_history')
def display_temp_history():
    return jsonify({'temp': temperature_list})


@app.route('/time')
def test():
    return str(datetime.now())


if __name__ == '__main__':
    # Spin up server available to all devices on your local network
    app.run("0.0.0.0", port=5000, debug=True)
