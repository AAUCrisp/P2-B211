from djitellopy import tello
import cv2
import threading
import socket
import time
import pygame
from pygame.locals import *
import Videobehandling


FORMAT = 'utf-8'
HOST = ''
PORT = 9400
BUFFERSIZE = 2048

RELAY_ADDR = ('192.168.1.133', 8889)

tello = tello.Tello()

VIDEO_PORT = 11111
STATE_PORT = 8890

# Create video socket
VIDEO_UDP = (HOST, VIDEO_PORT)
VIDEO_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
VIDEO_client_socket.bind(VIDEO_UDP)

# Create state socket
STATE_UDP = (HOST, STATE_PORT)
STATE_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
STATE_client_socket.bind(STATE_UDP)

# Create control socket
UDP_RELAY = (HOST,PORT)
UDP_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_client_socket.bind(UDP_RELAY)

def video_stream():
    while True:
        Video = Videobehandling.BackgroundFrameRead
#        img = VIDEO_client_socket.recvfrom(BUFFERSIZE)
        img = tello.get_frame_read().frame # get the 
        #img = cv2.resize(img, (360,240))
        cv2.imshow("Live Stream", img)
        cv2.waitKey(1)


def control_drone():
    # Start Pygame
    pygame.init()

    # Initialize the joysticks
    pygame.joystick.init()
    while True:
        time.sleep(0.1)
        # Get count of joysticks.
        joystick_count = pygame.joystick.get_count()
        
        # For each joystick:
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()

        rcLR = str(int(100 * joystick.get_axis(0)))
        rcFB = str(int(-100 * joystick.get_axis(1)))
        rcY = str(int(100 * joystick.get_axis(2)))
        rcUD = str(0)

        rcc = ('rc '+rcLR+' '+rcFB+' '+rcUD+' '+rcY)

        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    print("Button A has been pressed")
                    msg = 'takeoff'
                    msg = msg.encode(encoding=FORMAT) 
                    sent = UDP_client_socket.sendto(msg, RELAY_ADDR)

                if event.button == 1:
                    print("Button B has been pressed")
                    msg = 'land'
                    msg = msg.encode(encoding=FORMAT) 
                    sent = UDP_client_socket.sendto(msg, RELAY_ADDR)

                if event.button == 2:
                    print("Button x has been pressed")
                    msg = 'CW 90'
                    msg = msg.encode(encoding=FORMAT) 
                    sent = UDP_client_socket.sendto(msg, RELAY_ADDR)

                if event.button == 3:
                    print("Button y has been pressed")
                    quit()

                if event.button == 6:
                    msg = 'streamon'
                    msg = msg.encode(encoding=FORMAT) 
                    sent = UDP_client_socket.sendto(msg, RELAY_ADDR)

                if event.button == 7:
                    msg = 'command'
                    msg = msg.encode(encoding=FORMAT) 
                    sent = UDP_client_socket.sendto(msg, RELAY_ADDR)

            if event.type == JOYAXISMOTION:
                if (-0.3 > joystick.get_axis(0)) or (-0.3 > joystick.get_axis(1)) or (-0.3 > joystick.get_axis(2)) or (-0.3 > joystick.get_axis(3)) or (joystick.get_axis(0) > 0.3) or (joystick.get_axis(1) > 0.3) or (joystick.get_axis(2) > 0.3) or (joystick.get_axis(3) > 0.3):
                    msg = rcc
                    msg = msg.encode(encoding=FORMAT) 
                    sent = UDP_client_socket.sendto(msg, RELAY_ADDR)
                    #tello.send_rc_control(0,0,-10,0)

                elif (joystick.get_axis(4) > -0.5) or (joystick.get_axis(5) > -0.5):
                    rcUD = str(int (((joystick.get_axis(5) - 1)*50) - ((joystick.get_axis(4)- 1) * 50)))
                    rcc = ('rc '+rcLR+' '+rcFB+' '+rcUD+' '+rcY)
                    print(rcLR+' '+rcFB+' '+rcUD+' '+rcY)
                    msg = rcc
                    msg = msg.encode(encoding=FORMAT) 
                    sent = UDP_client_socket.sendto(msg, RELAY_ADDR)

                else:
                    msg = 'rc 0 0 0 0' 
                    msg = msg.encode(encoding=FORMAT) 
                    sent = UDP_client_socket.sendto(msg, RELAY_ADDR)

            if event.type == JOYHATMOTION:
                #if joystick.get_hat(0)==(0,0):
                    #tello.send_rc_control(0,0,0,0)

                if joystick.get_hat(0)==(-1,0):
                    #tello.send_rc_control(-10,0,0,0)
                    print("UP")

                if joystick.get_hat(0)==(1,0):
                    #tello.send_rc_control(10,0,0,0)
                    print("down")

                if joystick.get_hat(0)==(0,-1):
                    #tello.send_rc_control(0,10,0,0)
                    print("right")

                if joystick.get_hat(0)==(0,1):
                    #tello.send_rc_control(0,-10,0,0)
                    print("left")

            # Send data
            #msg = msg.encode(encoding=FORMAT) 
            #sent = UDP_client_socket.sendto(msg, RELAY_ADDR)

"""
def recv_state():
    while True: 
        try:
            data, server = UDP_client_socket.recvfrom(1518)
            dataStats.append(data.decode(encoding=FORMAT))
        except Exception:
            print ('\nExit . . .\n')
            break
"""

#def state_print():
    #time.sleep(5)
    #print(dataStats[-1])

thread_video = threading.Thread(target=video_stream)
thread_video.start()
thread_control = threading.Thread(target=control_drone)
thread_control.start()
#thread_stats = threading.Thread(target=recv_state)
#thread_stats.start()
#thread_print = threading.Thread(target=state_print)
#thread_print.start()


