#!/usr/bin/env python
from gopigo import *
import time, thread

minDis1 = 30
minDis2 = 14
DPR = 360.0/64
file = open("output.txt", "w")
file.write("B\n")

def turnRight90():
    pulse= int(120/DPR)
    enc_tgt(0,1,pulse)
    right_rot()
def turnLeft90():
    pulse= int(80/DPR)
    enc_tgt(0,1,pulse)
    left_rot()
def fwdOneRotation():
    enable_encoders()
    fwd()
    enc_tgt(1,1,9)
def fwdOne():
    enable_encoders()
    fwd()
    enc_tgt(1,1,5)
def stop_run(list):
    print "press 'Enter' to stop:"
    raw_input()
    list.append(None)
def run():
    set_speed(255)
    list = []
    thread.start_new_thread(stop_run, (list,))
    while not list:
        servo(66)
        time.sleep(1)
        rightDis = us_dist(15)
        if rightDis > minDis1:
            servo(30)
            time.sleep(1)
            rightDis = us_dist(15)
            if rightDis < minDis2:
                fwdOne()
                time.sleep(1)
            fwdOne()
            time.sleep(1)
            turnRight90()
            time.sleep(1)
            file.write("C\n")
            fwdOne()
            time.sleep(1)
            file.write("1\n")
        else:
            servo(150)
            time.sleep(1)
            dis = us_dist(15)
            if dis > minDis2:
                fwdOneRotation()
                time.sleep(1)
                file.write("1\n")
            else:
                turnLeft90()
                time.sleep(1)
                file.write("A\n")
                servo(150)
                time.sleep(1)
                dis = us_dist(15)
                if dis < minDis2:
                    turnLeft90()
                    time.sleep(1)
                    file.write("A\n")
    file.write("B")
    
if __name__ == "__main__":
    run()