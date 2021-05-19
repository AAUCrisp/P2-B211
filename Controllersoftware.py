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

RELAY_ADDR = ('192.168.10.1', 8889)

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

def takeScreenshot():

    #getting the current data and time
    timestamp = datetime.datetime.now()
    timestamp_str = timestamp.strftime("%Y-%m-%d-%H-%M-%S")
    #taking the screenshot
    newScreenshot = pyautogui.screenshot()
    #saving screenshot with datetime path
    newScreenshot.save(r'C:\\Users\Susan\Desktop\Screenshots\Screenshot {}.PNG'.format(timestamp_str)) #path should be changed to users desired file path
    print("Screenshot has been saved!")
   



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
                   #take screenshot of video
                    screenshots()

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
                    print(rcLR+' '+rcFB+' '+rcUD+' '+rcY)
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
    while True: 
        try:
            data, server = UDP_client_socket.recvfrom(1518)
            data = data.decode(FORMAT)
            print(data)
        except Exception:
            print ('\nExit . . .\n')
            break


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