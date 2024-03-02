from flask import Flask, request
from socket import *

app = Flask(__name__)

@app.route('/register', methods = ['PUT', 'GET'])
def register():
    hostname = request.args.get('hostname')
    ip = request.args.get('ip')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    if hostname and ip and as_ip and as_port:
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        message = "TYPE=A\nNAME={}\nVALUE={}\nTTL=10".format(hostname, ip)

        clientSocket.sendto(message.encode(), (as_ip, int(as_port)))
        modifiedMessage, severAddress = clientSocket.recvfrom(2048)
        clientSocket.close()

        modifiedMessage = modifiedMessage.decode()

        if modifiedMessage == 'SUCCESS':
            return modifiedMessage, 201
        else:
            return modifiedMessage, 500
    else:
        return 'miss some parameters', 400

def compute_fibonacci(x):
    if x == 1 or x == 2:
        return 1
    else:
        return compute_fibonacci(x - 1) + compute_fibonacci(x - 2)

@app.route('/fibonacci', methods = ['GET'])
def fibonacci():
    number = request.args.get('number')
    if not number or not number.isdigit():
        return 'Fail', 400
    else:
        return str(compute_fibonacci(int(number))), 200 


app.run(host='0.0.0.0',
        port=9090,
        debug=True)