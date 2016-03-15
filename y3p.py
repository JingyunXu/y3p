#!/usr/bin/env python

####################################
#         Y3P Maze Solver          #
#        GoPiGo Robot code         #
#       Jingyun Xu_10109145        #
####################################

from gopigo import *
import time
import thread

minDis1 = 30
minDis2 = 14
DPR = 360.0 / 64
trace = ["B"]


def turnRight90():
    ''' Turn right 90 degree 
        Adjust the degree number due to different fraction 
    '''
    pulse = int(120 / DPR)
    enc_tgt(0, 1, pulse)
    right_rot()


def turnLeft90():
    ''' Turn left 90 degree 
        Adjust the degree number due to different fraction 
    '''
    pulse = int(80 / DPR)
    enc_tgt(0, 1, pulse)
    left_rot()


def fwdOneRotation():
    ''' Move forward 9 cm for one step
    '''
    enable_encoders()
    fwd()
    enc_tgt(1, 1, 9)


def fwdOne():
    ''' Move forward 5 cm to make space turn right
    '''
    enable_encoders()
    fwd()
    enc_tgt(1, 1, 5)


def stop_run(list):
    ''' Termiate robot running while pressing "Enter" key
    '''
    print "press 'Enter' to stop:"
    raw_input()
    list.append(None)


def run():
    ''' Main function '''
    set_speed(255)      # set highest speed
    list = []
    thread.start_new_thread(stop_run, (list,))  # new thread listening "Enter" key pressing
    while not list:
        servo(66)       # set servo looking right 90 degree
        time.sleep(1)
        rightDis = us_dist(15)      # get distence returned by ultrasonic sensor
        if rightDis > minDis1:
            servo(30)       # set servo looking right 120 degree
            time.sleep(1)
            rightDis = us_dist(15)      # get distence returned by ultrasonic sensor
            if rightDis < minDis2:
                fwdOne()
                time.sleep(1)
            fwdOne()
            time.sleep(1)
            turnRight90()
            time.sleep(1)
            trace.append("C")
        else:
            servo(150)      # set servo looking front
            time.sleep(1)
            dis = us_dist(15)       # get distence returned by ultrasonic sensor
            if dis > minDis2:
                fwdOneRotation()
                time.sleep(1)
                trace.append("1")
            else:
                turnLeft90()
                time.sleep(1)
                trace.append("A")
                servo(150)      # set servo looking front
                time.sleep(1)
                dis = us_dist(15)       # get distence returned by ultrasonic sensor
                if dis < minDis2:
                    turnLeft90()
                    time.sleep(1)
    trace.append("B")

    for i, j in enumerate(trace[:-1]):  # parsing trace information
        if j == trace[i + 1] == "C":
            trace[i + 1] = "0"

    with open("output.txt", "w") as f:  # output trace information
        for i in trace:
            if i != "0":
                f.write(i + '\n')


if __name__ == "__main__":
    run()
