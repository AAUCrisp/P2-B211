import socket, time, threading

BUFFER_SIZE = 2048
FORMAT = 'utf-8'

# Info connection between the user and the relaybox.
RELAY_IP = ''
CMD_PORT = 8889
STATE_PORT = 8890
VIDEO_PORT = 11111

TELLO_IP = '192.168.10.1'
USER_IP = '192.168.1.197'

TELLO_ADDR = (TELLO_IP, CMD_PORT)

# Relay addresses
RELAY_CMD_ADDR = (RELAY_IP, CMD_PORT)
RELAY_VIDEO_ADDR = (RELAY_IP, VIDEO_PORT)
RELAY_STATE_ADDR = (RELAY_IP, STATE_PORT)

# User addresses
USER_CMD_ADDR = (USER_IP, CMD_PORT)
USER_VIDEO_ADDR = (USER_IP, VIDEO_PORT)
USER_STATE_ADDR = (USER_IP, STATE_PORT)

# Socket object 
control_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # 
control_udp.bind(RELAY_CMD_ADDR) # 

video_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # 
video_udp.bind(RELAY_VIDEO_ADDR) # 

state_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # 
state_udp.bind(RELAY_STATE_ADDR) # 

# sends the users control commands to the tello drone
def forward_control_cmd():
    time.sleep(2)
    run = 'command'
    run = run.encode(FORMAT)
    control_udp.sendto(run, TELLO_ADDR)
    while True:
        data, addr = control_udp.recvfrom(BUFFER_SIZE) # recieve data from the user
        control_udp.sendto(data, TELLO_ADDR) # sends cmd til tello drone

        print(data)
        cmd = data.decode(FORMAT)
        print(cmd)
   
# sends the tello drones videofeed to the user
def backward_videofeed():
    while True:
        data, addr = video_udp.recvfrom(BUFFER_SIZE) # recieve data from the tello drone
        video_udp.sendto(data, USER_VIDEO_ADDR) # sends videofeed to the user
        time.sleep(0.1)
        print(data)
  

# sends state info from tello drone to the user
def backward_state():
    while True:
        data, addr = state_udp.recvfrom(BUFFER_SIZE) # recieve data from the tello drone
        state_udp.sendto(data, USER_STATE_ADDR) # sends state info to the user 

        #state = data.decode(FORMAT)
        #print(state)



# main program
def run_program():

    print('[RELAY BOX] Relay box is running')
    print(f'Listening for incoming connections ...\n')
    
    # Start threads 
    control_thread = threading.Thread(target=forward_control_cmd)
    control_thread.start()
    video_thread = threading.Thread(target=backward_videofeed)
    video_thread.start()
    state_thread = threading.Thread(target=backward_state)
    state_thread.start()

    print('All threads are running')

    
run_program()