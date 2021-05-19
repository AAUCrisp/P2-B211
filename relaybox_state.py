import socket, time, threading

BUFFER_SIZE = 2048
FORMAT = 'utf-8'

# Info connection between the user and the relaybox.
RELAY_IP = ''
STATE_PORT = 8890

USER_IP = '192.168.1.197'

# Relay addresses
RELAY_STATE_ADDR = (RELAY_IP, STATE_PORT)

# User addresses
USER_STATE_ADDR = (USER_IP, STATE_PORT)

# Socket object 
state_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # 
state_udp.bind(RELAY_STATE_ADDR) # 

# sends state info from tello drone to the user

while True:
    data, addr = state_udp.recvfrom(BUFFER_SIZE) # recieve data from the tello drone
    state_udp.sendto(data, USER_STATE_ADDR) # sends state info to the user 

