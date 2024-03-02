from socket import *

serverPort = 53533
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(("", serverPort))

registration_map = {}

while True:
    message, clientAddress = serverSocket.recvfrom(2048)

    modifiedMessage = message.decode()
    modifiedMessage = modifiedMessage.split('\n')

    if len(modifiedMessage) == 4:
        hostname = modifiedMessage[1].split('=')[1]
        ip = modifiedMessage[2].split('=')[1]

        registration_map[hostname] = ip
        serverSocket.sendto('SUCCESS'.encode(), clientAddress)

    elif len(modifiedMessage) == 2:
        hostname = modifiedMessage[1].split('=')[1]

        if hostname in registration_map:
            message = "TYPE=A\nNAME={}\nVALUE={}\nTTL=10".format(hostname, registration_map[hostname])
            serverSocket.sendto(message.encode(), clientAddress)

    else:
        print('Incorrect message:{}'.format(modifiedMessage))