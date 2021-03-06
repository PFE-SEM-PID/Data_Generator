#! /usr/bin/env python2

from serial import *
from serial.tools.list_ports import comports
import csv
import threading

timestamper = 0
ki_init = 0  # 0 - 2
kp_init = 0.9  # 0.8 - 2
kd_init = 0.8  # 0.8 - 2
recording = False

def step_backward():
    start()
    serial_port.write("p\n")
    serial_port.write("-200\n")
    time.sleep(1)
    stop()

def step_forward():
    start()
    timestamper = 0
    first_value = True
    firt_time = 0
    while timestamper <= 1000:
        if serial_port.isOpen():
            serial_port.write("p\n")
            serial_port.write("200\n")
            if serial_port.in_waiting != 0:
                data = str(serial_port.readline())
                list_data = data.split()
                if first_value:
                    firt_time = list_data[0]
                    first_value = False
                if (list_data[0] != "ORDER"):
                    list_data[0] = list_data[0] - firt_time
                    timestamper = list_data[0]
                    c.writerow(list_data)
    stop()

def start():
    global recording
    recording = True
    serial_port.write("start\n")

def stop():
    global recording,plotting, timestamp, setpoint, pos_encodeur, pwm_envoye, erreur_derivative, erreur_integrale
    serial_port.write("stop\n")
    recording = False

def set_constante(a,b,c):
    serial_port.write("kp\n")
    serial_port.write(str(a)+"\n")
    serial_port.write("ki\n")
    serial_port.write(str(b)+"\n")
    serial_port.write("kd\n")
    serial_port.write(str(c)+"\n")
"""
class MyThread(threading.Thread):
    def run(self):
        global recording,timestamp, setpoint, pos_encodeur, pwm_envoye, erreur_derivative, erreur_integrale
        while True:
            while recording == True:
                if serial_port.isOpen():
                    if serial_port.in_waiting != 0:
                        data = str(serial_port.readline())
                        list_data = data.split()
                        if(list_data[0] != "ORDER"):
                            list_data[0] = timestamper
                            timestamper += 50
                            c.writerow(list_data)
"""
if __name__ == '__main__':
    if len(comports()) == 0:
        print "No serial port"
        exit(0)
    serial_port = Serial(port=comports()[0].device, baudrate=9600)
    print "Found device"+comports()[0].device
    #c = csv.writer(open("MONFICHIER.csv", "wb"))
    #Thread = MyThread()
    #Thread.start()
    for p in range(24):
        kp = p * 0.05 + kp_init
        time.sleep(900)
        for i in range(40):
            ki = i * 0.05 + ki_init
            for d in range(24):
                kd = d*0.05 + kd_init
                serial_port.write("r\n")
                set_constante(kp, ki, kd)
                file = open("./data/{kpp}_{kii}_{kdd}.csv".format(kpp=kp,kii=ki,kdd=kd),'wb')
                c = csv.writer(file)
                step_forward()
                set_constante(0, 0, 0)
                serial_port.write("r\n")
                time.sleep(0.2)
                file.close()
