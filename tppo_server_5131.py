from flask import Flask, request
from flask_socketio import SocketIO
import argparse
import os
import threading


parser = argparse.ArgumentParser(description='Ip and port of Server')
parser.add_argument('server_ip', type=str, help='Ip of Server')
parser.add_argument('server_port', type=int, help='Port of Server')
args = parser.parse_args()

app = Flask(__name__)
socketio = SocketIO(app)

def read_txt():
    path = 'blinds.txt'
    with open(path, 'r') as file:
        data = file.readlines()
    shear_percent = int(data[0].split()[-1])
    flux_percent = int(data[1].split()[-1])
    current_illumination  = int(data[2].split()[-1])
    vals = [shear_percent, flux_percent, current_illumination]
    return vals

def write_txt(data):
    path = 'blinds.txt'
    with open(path, 'w') as file:
        file.write(data)

@app.route('/blinds/<parameter>')
def main(parameter):
    vals = read_txt()
    idx = ['shaer', 'flux', 'illumination'].index(parameter)
    return {parameter: vals[idx]}

@app.route('/blinds')
def blinds():
    shaer = request.args.get('shaer')
    flux = request.args.get('flux')
    vals = read_txt()

    if shaer!=None:
        vals[0] = shaer
        data = 'shear_percent {}\nflux_percent {}\ncurrent_illumination {}\n'.format(vals[0], vals[1], vals[2])
        write_txt(data)
        return {"shaer":shaer}
    elif flux!=None:
        vals[1] = flux
        data = 'shear_percent {}\nflux_percent {}\ncurrent_illumination {}\n'.format(vals[0], vals[1], vals[2])
        write_txt(data)
        return {"flux":flux}

@socketio.on('connect')
def connect():
    blinds_changes_thread = threading.Thread(target=blinds_changes)
    blinds_changes_thread.start()
    print("[NEW CONNECTION] connected!")

def blinds_changes():
    vals = read_txt()
    parameters = ['shaer', 'flux', 'illumination']
    deviceFileName = 'blinds.txt'
    _cached_stamp = os.stat(deviceFileName).st_mtime
    while (True):
        stamp = os.stat(deviceFileName).st_mtime
        if(stamp != _cached_stamp):
            _cached_stamp = stamp
            new_vals = read_txt()
            for idx in range(3):
                if new_vals[idx] != vals[idx]:
                    socketio.emit("blinds_changes", {"parameter":parameters[idx], "value":new_vals[idx]}, broadcast=True)
                    vals[idx] = new_vals[idx]

if (__name__ == "__main__"):
    socketio.run(app, args.server_ip, args.server_port)   