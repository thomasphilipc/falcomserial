import serial
import threading
import queue
import tkinter as tk
import serial.tools.list_ports



class SerialThread(threading.Thread):
    def __init__(self, queue ,serial):
        threading.Thread.__init__(self)
        self.queue = queue
        self.serial =serial
        self.serialError = False

    def run(self):
        while True:

            # replaced the inwaiting for serial in line
            #if self.serial.inWaiting():

                #text = self.serial.readline(self.serial.inWaiting())
            # reads line by line form serial port

            #text = self.serial.readline()
            #self.queue.put(text)

            try:
                text=self.serial.readline()
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
            self.serial.write(cmd.encode('ascii')+ "\r\n".encode('ascii'))
        else:
            print ("Serial Error - Cannot write")



    def script(self,type):
        # function to write script
        if self.serialError == False:
            print(type)
            if type=="can":
                cmd = '$PFAL,Cnf.EraseBackup'
                self.serial.write(cmd.encode('ascii') + "\r\n".encode('ascii'))
        else:
            print ("Serial Error - Cannot write")


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
        # a queue is present to save the read data - the data is read periodically
        self.queue = queue.Queue()
        # get which port that the device needs to be selected
        self.portselected = self.check_serial()
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
        self.read_serial()

    def write_serial(self):
        param= self.forwardcommand.get()
        print(param)
        self.forwardcommand.delete(0,'end')
        self.thread.write(param)
        print("write command")

    def read_serial(self):
        while self.queue.qsize():
            try:
                #self.text.delete(1.0, 'end')
                content =str(self.queue.get())
                # check data read for patterns here.
                if content.__contains__(''):
                    print (content)
                    # data is inserted into the GUI
                    self.MainLog.insert('end', content)
                # to show the last entry
                self.MainLog.see('end')
            except queue.Empty:
                pass
        # the function is called every 1/10 second
        self.after(100, self.read_serial)

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