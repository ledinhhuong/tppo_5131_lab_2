import socketio
import argparse
import requests

parser = argparse.ArgumentParser(description='Ip and port of Server')
parser.add_argument('server_ip', type=str, help='Ip of Server')
parser.add_argument('server_port', type=int, help='Port of Server')
args = parser.parse_args()

sio = socketio.Client()

@sio.event
def connect():
    print("[CONNECTED] Client connected to server at http://{}:{}".format(args.server_ip, args.server_port))
    print("Parameters: shaer (0..100); flux (0..100); illumination (0..5000)")
    print("Syntax:\n\
    get <parameter>\n\
    set <parameter> <value>")
    while(True):
            try:
                text = input()
                elements = text.split()
                parameters = ['shaer', 'flux', 'illumination']
                if len(elements)==3 and elements[0]=='set' and elements[1] in parameters[0:2] and 0<=float(elements[2])<=100:
                    url = " http://{}:{}/blinds?{}={}".format(args.server_ip, args.server_port, elements[1], elements[2])
                    response = requests.get(url)
                    print("SERVER RESPONSE: ", response.json())
                elif len(elements)==2 and elements[0]=='get' and elements[1] in parameters:
                    url = "http://{}:{}/blinds/{}".format(args.server_ip, args.server_port, elements[1])
                    response = requests.get(url)
                    print("SERVER RESPONSE: ", response.json())
                else:
                    print('Syntax error')
            except:
                print('Syntax error')

@sio.on('blinds_changes')
def blinds_changes(data):
    print('NOTIFICATION SERVER: {} has been changed to {}'.format(data['parameter'], data['value']))

sio.connect("http://{}:{}".format(args.server_ip, args.server_port))