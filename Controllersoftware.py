from DJITelloPy import tello
import cv2
import threading
import socket
import time
import pygame
from pygame.locals import *
import pyautogui #screenshot library
import datetime #datetime library
from databasestuff import *


FORMAT = 'utf-8'
HOST = ''
PORT = 9400
BUFFERSIZE = 2048
VIDEO_PORT = 11111
STATE_PORT = 8890

#RELAY_ADDR = ('192.168.10.1', 8889)    # Tello Direct
RELAY_ADDR = ('192.168.1.132', 8889)      # Relaybox School
# RELAY_ADDR = ('192.168.1.132', 8889)      # Relaybox Steffen Home

tello = tello.Tello()


"""
# Create video socket
VIDEO_UDP = (HOST, VIDEO_PORT)
VIDEO_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
VIDEO_client_socket.bind(VIDEO_UDP)
"""


# Create state socket
STATE_UDP = (HOST, STATE_PORT)
STATE_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
STATE_client_socket.bind(STATE_UDP)

# Create control socket
UDP_RELAY = (HOST,PORT)
UDP_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_client_socket.bind(UDP_RELAY)

#address_schema = 'udp://@{ip}:{port}'
#address = address_schema.format(ip='192.168.1.127', port=11111)
#cap = cv2.VideoCapture('udp://192.168.1.127/11111')

def video_stream():
    while True:

        img = tello.get_frame_read().frame
        cv2.namedWindow('Live Stream')
        cv2.imshow('Live Stream', img)
        cv2.waitKey(1)


def control_drone():
    # Start Pygame

    pygame.init()

    # Initialize the joysticks
    pygame.joystick.init()
    while True:
        time.sleep(0.05)
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
                   #take screenshot of video
                    screenshots()
                    print("Screenshot taken")

                if event.button == 3:
                    print("Button y has been pressed")
                    quit()

                if event.button == 6:
                    msg = 'streamon'
                    msg = msg.encode(encoding=FORMAT) 
                    sent = UDP_client_socket.sendto(msg, RELAY_ADDR)
                    thread_video.start()
                    print("Streamen er startet")

                if event.button == 7:
                    msg = 'command'
                    msg = msg.encode(encoding=FORMAT) 
                    sent = UDP_client_socket.sendto(msg, RELAY_ADDR)

            if event.type == JOYAXISMOTION:
                if (joystick.get_axis(4) > -0.5) or (joystick.get_axis(5) > -0.5):
                    rcUD = str(int (((joystick.get_axis(5) - 1)*50) - ((joystick.get_axis(4)- 1) * 50)))
                    rcc = ('rc '+rcLR+' '+rcFB+' '+rcUD+' '+rcY)
                    #print(rcLR+' '+rcFB+' '+rcUD+' '+rcY)      # Print RC Command
                    msg = rcc
                    msg = msg.encode(encoding=FORMAT) 
                    sent = UDP_client_socket.sendto(msg, RELAY_ADDR)
                
                elif (-0.3 > joystick.get_axis(0)) or (-0.3 > joystick.get_axis(1)) or (-0.3 > joystick.get_axis(2)) or (-0.3 > joystick.get_axis(3)) or (joystick.get_axis(0) > 0.3) or (joystick.get_axis(1) > 0.3) or (joystick.get_axis(2) > 0.3) or (joystick.get_axis(3) > 0.3):
                    msg = rcc
                    msg = msg.encode(encoding=FORMAT) 
                    sent = UDP_client_socket.sendto(msg, RELAY_ADDR)
                    #tello.send_rc_control(0,0,-10,0)

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

# -- Drone State Receive Function --
def recv_state():
    print("State-feed Started") 
    while True: 
        data, server = STATE_client_socket.recvfrom(3000)       # Buffer?
        data = data.decode(FORMAT)
        data = data.rsplit(";")
        # Straight Speed
        straight = float( data[9].replace("vgy:", "") ) * 0.036
        print(f"Straight-Speed: {straight}Km/h")
        # Sideways Speed
        sideways = float( data[8].replace("vgx:", "") ) * 0.036
        print(f"Sideways-Speed: {sideways}Km/h")
        # Altitude Speed
        altitude = float( data[10].replace("vgz:", "") ) * 0.036
        print(f"Altitude-Speed: {altitude}Km/h")
        # Flight Height
        height = float( data[14].replace("h:", "") ) / 100
        print(f"Flight Height: {height} meter")
        # Battery Level
        battery = data[15].replace("bat:", "")
        print(f"Battery Level: {battery}%")
        time.sleep(0.5)
        print("\n \n \n")


# def state_print():
    #time.sleep(5)
    #print(dataStats[-1])

thread_video = threading.Thread(target=video_stream)
#thread_video.start()
thread_control = threading.Thread(target=control_drone)
thread_control.start()
#thread_stats = threading.Thread(target=recv_state)
#thread_stats.start()
#thread_print = threading.Thread(target=state_print)
#thread_print.start()
thread_state = threading.Thread(target=recv_state)
thread_state.start()