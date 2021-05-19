import socket, time, threading

BUFFER_SIZE = 2048
FORMAT = 'utf-8'

# Info connection between the user and the relaybox.
RELAY_IP = ''
VIDEO_PORT = 11111

USER_IP = '192.168.1.197'

# Relay addresses
RELAY_VIDEO_ADDR = (RELAY_IP, VIDEO_PORT)


# User address
USER_VIDEO_ADDR = (USER_IP, VIDEO_PORT)


video_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # 
video_udp.bind(RELAY_VIDEO_ADDR) # 



# sends the tello drones videofeed to the user

while True:
    data, addr = video_udp.recvfrom(BUFFER_SIZE) # recieve data from the tello drone
    video_udp.sendto(data, USER_VIDEO_ADDR) # sends videofeed to the user

