from flask import Flask, request
from socket import *
import json
import requests

app = Flask(__name__)


@app.route('/fibonacci')
def get_fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    if hostname and fs_port and number and as_ip and as_port:
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        message = "TYPE=A\nNAME={}".format(hostname)

        clientSocket.sendto(message.encode(), (as_ip, int(as_port)))
        modifiedMessage, severAddress = clientSocket.recvfrom(2048)

        clientSocket.close()
        modifiedMessage = modifiedMessage.decode()



        if 'TYPE' in modifiedMessage:
            modifiedMessage = modifiedMessage.split('\n')
            url = 'http://{}:{}/fibonacci?number={}'.format(modifiedMessage[2].split('=')[1], fs_port, number)
            x = requests.get(url)
            if x.status_code == 200:
                return x.text, 200
            else:
                return x.text, x.status_code
        else:
            return 'miss fs_ip', 400

    else:
        return 'miss some parameters', 400
    


app.run(host='0.0.0.0',
        port=8080,
        debug=True)