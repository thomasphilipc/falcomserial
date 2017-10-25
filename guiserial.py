import serial
import os
import datetime
import time
import threading
import socket
import queue
import tkinter as tk
import serial.tools.list_ports


#------------------------------------------------------
#------------------------------------------------------
#-------- SCRIPT CLASS TO MANAGE SCRIPT LOG -----------
#------------------------------------------------------
#------------------------------------------------------

class script:
    script_name = None
    total_commentline = 0
    total_scriptline = 0
    commentlinelist = []
    scriptlinelist = []
    #total_alarmline = 0
    #alarmlinelist = []
    #total_macroline = 0
    #macrolinelist = []
    #total_replaceline = 0
    #replacelinelist = []
    #total_aliasline = 0
    #aliaslinelist = []
    #total_otherline = 0
    #otherlinelist = []



    def __init__(self,script_name):
        self.script_name= script_name

    def add_line(self,line,tlno):

        if line.__len__()> 0:
            if not line.startswith("$PFAL"):
                self.total_commentline += 1
                self.commentlinelist.append(tlno)
            elif line.startswith("$PFAL"):
                self.total_scriptline += 1
                self.scriptlinelist.append(tlno)
        else:
            print(line)
            print(tlno)

    def print_script_summary(self):
        print(" comment lines {} , alarmlines {}".format(self.total_commentline, self.total_scriptline))
        print (self.scriptlinelist)
        print (self.commentlinelist)


#------------------------------------------------------
#------------------------------------------------------
#--------- THREADING CONTROL - SERIAL,QUEUE -----------
#------------------------------------------------------
#------------------------------------------------------

class SerialThread(threading.Thread):
    def __init__(self, queue ,serial):
        threading.Thread.__init__(self)
        self.queue = queue
        self.serial =serial
        self.serialError = False

    def run(self):
        # this function runs to put the serial read line to the queue
        while True:

            # replaced the inwaiting for serial in line
            #if self.serial.inWaiting():

                #text = self.serial.readline(self.serial.inWaiting())
            # reads line by line form serial port

            #text = self.serial.readline()
            #self.queue.put(text)

            try:
                text=self.serial.readline()
                # text received is in byte string and therefore needs to be decoded.
                text=text.decode()
                self.queue.put(text)

            except serial.serialutil.SerialException:
                self.serialError = True
                print ("error occured")
                break

    def write(self,command):
        # function to write command entered in the line to the serial port
        # receives the command to write to the serial port
        if self.serialError == False:
            print(command)
            if command:
                cmd = str(command)
            else:
                # assigns a default command if a blank sent is entered
                cmd = '$PFAL,GSM.IMEI'
            # converts data to be sent to the serial into asciii
            data = (cmd.encode('ascii') + "\r\n".encode('ascii'))
            # print the data
            print(data)
            # write to the serial port
            #\r\n is CR+LF carrriage return and line feed
            self.serial.write(data)
        else:
            print ("Serial Error - Cannot write")

    def parse_command(self,cmd):
        #fucntion to add Carriage Return and Line Feed
        data = (cmd.encode('ascii') + "\r\n".encode('ascii'))
        return data

    def script_device(self,type):

        requiredDir = 'C:\\falcomserial'


        # function to write script

        #if there is a serial no error on serial connection then proceed
        if self.serialError == False:



            print(type)
            #checks if type is script . currently this is the only feature
            if type=="script":

                ack = True
                success = 0
                fail = 0

                # set command to obtain IMEI number
                cmd = "$PFAL,GSM.IMEI"

                content = self.parse_command(cmd)
                # if ack is true , as this is the first command we write
                if ack:
                    self.serial.write(content)
                    # after write we set ack to false as we need to wait for confirmation on success
                    ack = False
                    # below loop keeps running and reading responses on the serial line
                    while True:
                        content = str(self.queue.get())
                        #  check data read for patterns here.
                        line = content
                        if line.__contains__("IMEI"):
                            print(line)
                        elif line.__contains__("SUCCESS"):
                            print(cmd)
                            print(line)
                            success += 1
                            ack = True
                            break
                        elif line.__contains__("ERROR"):
                            print(cmd)
                            print(line)
                            fail += 1
                            ack = True
                            break

                print("IMEI queried")

                ack = True
                success = 0
                fail = 0

                cmd = "$PFAL,Cnf.Get,DEVICE.NAME"

                content = self.parse_command(cmd)
                # if ack is true , write the next command
                if ack:
                    self.serial.write(content)
                    # after write we set ack to false as we need to wait for confirmation on success
                    ack = False
                    # below loop keeps running and reading
                    while True:
                        content = str(self.queue.get())
                        #  check data read for patterns here.
                        line = content

                        if line.__contains__("DEVICE.NAME"):
                            print(line)
                        elif line.__contains__("SUCCESS"):
                            print(cmd)
                            print(line)
                            success += 1
                            ack = True
                            break
                        elif line.__contains__("ERROR"):
                            print(cmd)
                            print(line)
                            fail += 1
                            ack = True
                            break

                print("DeviceName queried")






                # iterates through each file in the folder called falcomeserial
                for filename in os.listdir(requiredDir):
                    print(filename)
                    # opening the file
                    file = open(requiredDir + "\\" + filename, 'r', errors='replace')
                    newfile_flag = 1
                    filename = filename.split('.txt')
                    print('Parsing {}'.format(filename[0]))
                    currentscript = script(filename[0])
                    tlno = 0
                    # setting ack to true before first line read
                    ack = True
                    success=0
                    fail=0
                    scriptlines=0
                    for line in file:
                        tlno += 1
                        currentscript.add_line(line, tlno)
                        if line.startswith("$PFAL"):
                            scriptlines+=1
                            line=line.replace('\n', '')
                            cmd=line
                            #calling a parse command to set it in the required fromat to be send via serial
                            content = self.parse_command(cmd)
                            # if ack is true , meaning we received a success or if first command then write
                            if ack:
                                self.serial.write(content)
                            #after write we set ack to false as we need to wait for confirmation on success
                            ack=False
                            # below loop keeps running and reading
                            while True:
                                content = str(self.queue.get())
                                #  check data read for patterns here.
                                line = content
                                if line.__contains__("SUCCESS"):
                                    print (cmd)
                                    print(line)
                                    success+=1
                                    ack = True
                                    break
                                elif line.__contains__("ERROR"):
                                    print(cmd)
                                    print(line)
                                    fail+=1
                                    ack = True
                                    break






                    currentscript.print_script_summary()
                    print("scripting completed")
                    result = "Script Summary | Total Lines Send {} | Successful {} | Failed {}".format(scriptlines, success, fail)
                    print(result)
                    return result


        else:
            print ("Serial Error - Cannot write")



    def check_ack(self,command):

        print ("entered checkack")
        ack = True
        success = 0
        fail = 0
        responseline = "not avaialable"

        # set command to obtain IMEI number
        cmd = command

        content = self.parse_command(cmd)
        # if ack is true , as this is the first command we write
        if ack:
            self.serial.write(content)
            # after write we set ack to false as we need to wait for confirmation on success
            ack = False
            # below loop keeps running and reading responses on the serial line
            while True:
                content = str(self.queue.get())
                #  check data read for patterns here.
                line = content
                if line.__contains__("IMEI"):
                    print(line)
                    responseline = line
                elif line.__contains__("SUCCESS"):
                    print(cmd)
                    print(line)
                    success += 1
                    ack = True
                    break
                elif line.__contains__("ERROR"):
                    print(cmd)
                    print(line)
                    fail += 1
                    ack = True
                    break

        if success>0 :
            state = "True"
        elif fail>0:
            state = "False"
        else:
            state = "Not Obtained"

        result = "Command:{}|ResponseState:{}|ResponseLine:{}".format(cmd,state,responseline)

        print("ack completed")
        print(result)


#------------------------------------------------------
#------------------------------------------------------
#--------- SERIAL CONNECTION CONTROL ------------------
#------------------------------------------------------
#------------------------------------------------------


class serialport:
    # this is a class that saves relevant data for the serial ports
    serial_number = 'not init'
    port = 'none detected'
    description = 'none available'

    def __init__(self,serial_number,port,description):
        self.serial_number=serial_number
        self.port=port
        self.description=description

    def print_port_details(self):
        print("{} | {} | {} ".format(self.serial_number, self.port, self.description))

def return_port (serial_number, serialport = []):
    # fucntion that returns the port name for the selection from the serial port list , this returns a Port name
    for thisport in serialport:
        print (serial_number)
        print (thisport.serial_number)
        if int(serial_number) == int(thisport.serial_number):
            print ("Correct port found")
            return thisport.port



#------------------------------------------------------
#------------------------------------------------------
#-------- ASSET CLASS TO MANAGE ASSET UPDATE ----------
#------------------------------------------------------
#------------------------------------------------------

class asset:
    imei = None
    current_script = None
    required_script = None
    start_time = None
    end_time = None
    attempts = 0
    failed_lines = []
    succeeded_lines = []

    #st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    def __init__(self,imei,current_script,required_script):
        self.imei = imei
        self.current_script = current_script
        self.required_script = required_script
        self.attempts = 0

    def record_start(self):
        self.start_time=time.time()

    def record_end(self):
        self.end_time=time.time()

    def record_attmepts(self):
        self.attempts = self.attempts+1

    def record_failed_lines(self,linenumber):
        self.failed_lines.append(linenumber)

    def record_succeeded_lines(self,linenumber):
        self.succeeded_lines.append(linenumber)


#------------------------------------------------------
#------------------------------------------------------
#------ BELOW IS THE SOCKET CONTROL FOR TCP/IP --------
#------------------------------------------------------
#------------------------------------------------------



def enable_socket():

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



#------------------------------------------------------
#------------------------------------------------------
#---------- CONTROLS GUI BY TKINTER PYTHON ------------
#------------------------------------------------------
#------------------------------------------------------

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Kraken Tentacles - Falcom Local Script Loader ")
        self.geometry("1360x750")
        frameLabel = tk.Frame(self, padx=10, pady =10)
        self.MainLog = tk.Text(frameLabel, wrap='word', bg=self.cget('bg'), relief='flat')
        frameLabel.pack()
        self.scrollbar = tk.Scrollbar(frameLabel)
        self.scrollbar.pack(side='right', fill='y')
        self.MainLog.pack()
        frameLabel2 = tk.Frame(self)
        self.forwardcommand= tk.Entry(frameLabel2 ,  width = 75 )
        self.forwardcommand.pack( side='left')
        frameLabel2.pack()
        self.sendbutton = tk.Button(frameLabel2, text = "Send",  command = lambda: self.write_serial())
        self.sendbutton.pack(side='right' ,  padx=10, pady =10)
        self.scriptbutton = tk.Button(frameLabel2, text ="ScriptDevice" , command = lambda: self.script_device())
        self.scriptbutton.pack(side='right', padx=10, pady=10)
        # a queue is present to save the read data - the data is read periodically
        self.queue = queue.Queue()
        self.scripting_in_progress=False
        # get which port that the device needs to be selected
        self.portselected = self.check_serial()
        print(self.portselected)
        print(self.portselected)
        # pass port to enable serial connection
        self.baud_rate = 115200
        self.timeout = 1
        # a serial port is connected and established
        self.serial = serial.Serial(port=self.portselected,baudrate=self.baud_rate)
        # a serial port is passed along the thread along with the queue.
        self.thread = SerialThread(self.queue,self.serial)
        self.thread.start()
        # a read serial port function is called
        self.read_serial_queue()

    # function calling the script_device fucntion via GUI CLICK
    def script_device(self):
        self.scripting_in_progress=True
        result = self.thread.script_device("script")
        self.MainLog.insert('end', result)
        # to show the last entry
        self.MainLog.see('end')
        self.scripting_in_progress = False

    # function that writes command entered to serial line
    def write_serial(self):
        param= self.forwardcommand.get()
        print("written {} to serial line".format(param))
        #
        self.forwardcommand.delete(0,'end')
        self.thread.write(param)

    # function to read from the serial queue
    def read_serial_queue(self):

        if not self.scripting_in_progress:
            while self.queue.qsize():
                try:
                    content =str(self.queue.get())
                    # check data read for patterns here.

                    line=content
                    print (line)
                    if not line.startswith('$GP'):
                        # data is inserted into the GUI
                        self.MainLog.insert('end', line)
                        # to show the last entry
                        self.MainLog.see('end')
                except queue.Empty:
                    pass
            # the function is called every 1/10 second
            self.after(100, self.read_serial_queue)


    def check_serial(self):

        # array of class ports
        serialportlist = []

        print("checking available ports")

        # all the ports are stored as a list in ports variable
        ports = list(serial.tools.list_ports.comports())
        i = 1
        # iterate through the ports to build a list
        for p in ports:
            # create a port class
            currentport = serialport(i, p.device, p.description)
            # add the port to another serial list
            serialportlist.append(currentport)
            # print all the port details
            currentport.print_port_details()
            i += 1

        # get input to which port they want to connect
        print("Please select s.no for the port that you want to connect to")
        a = input()

        # get the port selection
        selectedport = return_port(a, serialportlist)

        print("you selected {}".format(selectedport))

        # return the selected port
        return selectedport


app = App()
app.mainloop()
enable_socket()