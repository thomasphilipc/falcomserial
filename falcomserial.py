import serial
import time
import os
import _thread
import serial.tools.list_ports
import socket
from tkinter import *

Read_Started = False
Write_Started = False

# class to store serial ports connected to system.
class serialport:
    serial_number = 'not init'
    port = 'none detected'
    description = 'none available'

    def __init__(self,serial_number,port,description):
        self.serial_number=serial_number
        self.port=port
        self.description=description

    def print_port_details(self):
        print("{} | {} | {} ".format(self.serial_number, self.port, self.description))

# function to return port number for the selection made
def return_port (serial_number, serialport = []):
    for thisport in serialport:
        print (serial_number)
        print (thisport.serial_number)
        if int(serial_number) == int(thisport.serial_number):
            print ("Correct port found")
            return thisport.port


#function to read serial as a thread
def read_serial(ser,id,Read_Started):
    Read_Started=True
    print('Running Read thread %d' % id)
    while True:
        data = ser.readline()
        dummy = str(data)
    # if (dummy.__contains__('cyclic')):
    #    print (data)
        print(dummy)
        #updateMainDisplay(dummy)
    return Read_Started

# function to write as thread
def write_serial(ser,id,Write_Started):
    Write_Started= True
    print('Running Write thread %d' % id)
    cmd = '$PFAL,GSM.IMEI'
    while True:
        data = (cmd.encode('ascii') + "\r\n".encode('ascii'))
        print(data)
        ser.write(cmd.encode('ascii')+ "\r\n".encode('ascii'))
    return Write_Started

def check_serial():

    # array of class ports
    serialportlist=[]


    print("checking available ports")

    # all the ports are stored as a list in ports variable
    ports = list(serial.tools.list_ports.comports())
    i=1
    # iterate through the ports to build a list
    for p in ports:
        #create a port class
        currentport=serialport(i,p.device,p.description)
        #add the port to another serial list
        serialportlist.append(currentport)
        #print all the port details
        currentport.print_port_details()
        i+=1


    # get input to which port they want to connect
    print("Please select s.no for the port that you want to connect to")
    a=input()

    # get the port selection
    selectedport=return_port(a,serialportlist)


    print("you selected {}".format(selectedport))

    # return the selected port
    return selectedport

def enable_socket():
    root.mainloop()

    print ("enabling socket")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('localhost',10000)
    s.bind(server_address)


    s.listen(1)



     #Wait for a connection
    s, client_address = s.accept()




    try:
        while True:
            data = s.recv(16)
            if data:
                print("received data:", data)
            else:
                break


    finally:
    # Clean up the connection
        s.close()

def update_text(dummy):
    print("calling")
    #updateMainDisplay(dummy)

def enable_serial(portselected,baud_rate,timeout,Read_Started,Write_Started):
    ser = serial.Serial(port=portselected,baudrate=baud_rate, bytesize=8, parity='N', stopbits=1,timeout=timeout, xonxoff=0, rtscts=1)  # open serial port
    print(ser.name)  # check which port was really used
    while ser.is_open:
        print ("port is open")
        print ("Write_Started : {}".format(Write_Started))
        print("Read_Started : {}".format(Read_Started))
        if Write_Started == False:
            Write_Started=_thread.start_new(write_serial(ser, 2,Write_Started))
        if Read_Started == False:
            Read_Started=_thread.start_new(read_serial,(ser,1,Read_Started))
    return ser

# get which port that the device needs to be selected
portselected=check_serial()
#pass port to enable serial connection
baud_rate=115200
timeout=1
enabledserial=enable_serial(portselected,baud_rate,timeout,Read_Started,Write_Started)


while enabledserial.is_open == False:
    print("closing")
    break

#enabling socket
#while True:
#    enable_socket()

#set tkinter at root
root = Tk()
#set titile
root.title ("Reading Serial")

#set scroll bar
S = Scrollbar(root)
S.pack(side=RIGHT, fill=Y)
#set a text box
T = Text(root, height=30, width=50, takefocus=0)
T.pack()










