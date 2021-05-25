import socket, time

BUFFER_SIZE = 2048
FORMAT = 'utf-8'

# Info connection between the user and the relaybox.
RELAY_IP = ''
CMD_PORT = 8889
Vdata = b""

TELLO_IP = '192.168.10.1'
USER_IP = '192.168.1.197'

TELLO_ADDR = (TELLO_IP, CMD_PORT)
RELAY_CMD_ADDR = (RELAY_IP, CMD_PORT)
USER_CMD_ADDR = (USER_IP, CMD_PORT)

control_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # 
control_udp.bind(RELAY_CMD_ADDR) # 


#time.sleep(2)
#run = 'command'
#run = run.encode(FORMAT)
#control_udp.sendto(run, TELLO_ADDR)
while True:
    data, addr = control_udp.recvfrom(BUFFER_SIZE) # recieve data from the user
    control_udp.sendto(data, TELLO_ADDR) # sends cmd til tello drone