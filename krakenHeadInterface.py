from PIL import Image, ImageTk
from tkinter import Tk, BOTH, BooleanVar, Checkbutton , Variable, IntVar , LEFT , ACTIVE,  TOP , Button , Label , Radiobutton , X , W , YES , NO , BOTTOM ,LabelFrame, StringVar
from tkinter.ttk import Frame, Label, Style, Combobox
from PIL import Image,ImageTk
import yaml


class ScriptGenerator(Frame):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.master.title("Script Generator")
        self.pack()
        self.master.iconbitmap("logo_rYO_icon.ico")
        self.master.geometry("1360x750")
        self.var1 = IntVar ()
        self.var2 = IntVar()
        self.var3 = IntVar()
        self.var4 = IntVar()
        self.var5 = IntVar()
        self.var6 = IntVar()
        self.var7 = IntVar()
        self.var8 = IntVar()
        self.var9 = IntVar()
        self.var10 = IntVar()
        self.v = IntVar ()
        self.reportin_box_value = "5 min"
        self.idlin_box_value = "10 min"
        self.value_of_combo = 'X'
        self.box_value = StringVar()
        self.settingsContainer = Frame(self.master)
        self.settingsContainer.pack()

        # feature_list= {'Ignition On/Off': 0, 'Poll': 0, 'Heartbeat': 0, 'Tag In/Out': 0}
        #
        # for feature in feature_list:
        #     enable_feature = IntVar()
        #     l = Checkbutton(self.master, text=feature, variable=enable_feature, command=self.test())
        #     l.pack()

        self.check_button_ignition = Checkbutton(self.settingsContainer, text="Ignition On/Off", command= lambda: self.checkbox_clicked(1), variable=self.var1)
        self.check_button_ignition.pack(expand=NO,anchor=W)
        self.check_button_ignition.select()
        self.IgnitionContainer = Frame(self.settingsContainer)
        self.IgnitionContainer.pack()
        methods = [
            ("CanBus", 1),
            ("OBD", 2),
            ("Alternator", 3),
            ("Ignition Only", 4),
            ("Ignition + Alternator", 5)
        ]

        self.Label_Frame = LabelFrame(self.IgnitionContainer,text="Ignition mode:")


        for method in methods:
            # print(method)
            val = (method[1])
            type = method[0]
            self.Radio_Button = Radiobutton(self.Label_Frame, text=type, padx=20, variable=self.v,
                                            command=lambda: self.ShowChoice(val), value=val)
            self.Radio_Button.pack(side=LEFT)
            self.Radio_Button.select()




        self.Label_Frame.pack()
        # for child in self.Label_Frame.winfo_children():
        #     child.configure(state='disable')

        self.IgnitionContainer.pack()

        self.check_button = Checkbutton(self.settingsContainer, text="Poll Enabled", command=lambda: self.checkbox_clicked(2),
                                        variable=self.var2)
        self.check_button.pack(expand=NO,anchor=W)
        self.check_button.select()
        self.check_button = Checkbutton(self.settingsContainer, text="Tag In/Out", command=lambda: self.checkbox_clicked(3),
                                        variable=self.var3)
        self.check_button.pack(expand=NO,anchor=W)
        self.check_button = Checkbutton(self.settingsContainer, text="Immobilizer Functionality", command=lambda: self.checkbox_clicked(4),
                                        variable=self.var4)
        self.check_button.pack(expand=NO,anchor=W)


        #
        self.check_button = Checkbutton(self.settingsContainer, text="Normal Reporting", command=lambda: self.checkbox_clicked(5),
                                        variable=self.var5)
        self.check_button.pack(expand=NO,anchor=W)

        self.reportin_box = Combobox(self.settingsContainer, textvariable=self.reportin_box_value)
        self.reportin_box['values'] = ('1 min', '5 min', '10 min','15 min')
        self.reportin_box.current(0)
        self.reportin_box.pack(padx=5, pady=5,anchor=W)



        self.check_button= Checkbutton(self.settingsContainer, text="HeartBeat", command=lambda: self.checkbox_clicked(6),
                                       variable=self.var6)
        self.check_button.pack(expand=NO,anchor=W)
        self.check_button = Checkbutton(self.settingsContainer, text="Idling", command=lambda: self.checkbox_clicked(7),
                                        variable=self.var7)
        self.check_button.pack(expand=NO,anchor=W)

        self.idlin_box = Combobox(self.settingsContainer, textvariable=self.idlin_box_value)
        self.idlin_box['values'] = ('1 min', '5 min', '10 min', '15 min')
        self.idlin_box.current(0)
        self.idlin_box.pack(padx=5, pady=5, anchor=W)


        self.EcoDriveContainer = Frame(self.settingsContainer)

        self.check_button = Checkbutton(self.EcoDriveContainer, text="EcoDrive",
                                        command=lambda: self.checkbox_clicked(8),
                                        variable=self.var8)
        self.check_button.pack(expand=NO, anchor=W)

        self.Label_Frame = LabelFrame(self.EcoDriveContainer, text="Ecodrive Options:")



        self.box = Combobox(self.Label_Frame, textvariable=self.box_value)
        temp_list = list()
        temp_list=self.open_ecodrive_lib()
        self.box['values'] = temp_list
        self.box.current(0)

        self.box.pack(padx=5,pady=5)



        self.Label_Frame.pack(anchor=W)
        self.EcoDriveContainer.pack(anchor=W)

        self.check_button = Checkbutton(self.settingsContainer, text="Over Speeding", command=lambda: self.checkbox_clicked(9),
                                        variable=self.var9)
        self.check_button.pack(expand=NO,anchor=W)
        self.check_button = Checkbutton(self.settingsContainer, text="Service Mode/Normal Mode",
                                        command=lambda: self.checkbox_clicked(10),
                                        variable=self.var10)
        self.check_button.pack(expand=NO, anchor=W)





        self.button = Button(self.settingsContainer,text = "Generate Script",command=self.build_settingscode)
        self.button.pack(side=BOTTOM)

    def ShowChoice(self,val):
        print(self.v.get())

    def checkbox_clicked(self, var):
        print (var)
        # print("State Changed:", self.var1.get())
        # print("State Changed:", self.var2.get())
        # print("State Changed:", self.var3.get())
        # print("State Changed:", self.var4.get())
        # print("State Changed:", self.var5.get())
        # print("State Changed:", self.var6.get())
        # print("State Changed:", self.var7.get())
        # print("State Changed:", self.var8.get())
        # print("State Changed:", self.var9.get())
        # print("State Changed:", self.var10.get())

        self.checkbox_manager(var)

    def open_ecodrive_lib(self):

        requiredDir = 'C:\\Users\\thomas\\PycharmProjects\\virtualenv\\falcomserial\\conf'

        file = open(requiredDir + "\\ecodrive-dict", 'r', errors='replace')
        newlist = list()
        newdict = dict
        yaml_collection = yaml.load(file)

        if (yaml_collection["dict"]):
            # print("data in ecodrive library")
            length = len(yaml_collection["dict"])
            ecodrive_library = yaml_collection["dict"]
            for i in range(len(yaml_collection["dict"])):
                newdict = yaml_collection["dict"][i]
                # print(yaml_collection["dict"][i])
                for i in newdict.keys():
                    if newdict[i]!= None:
                        newlist.append(i)
        else:
            print("config file corrupted")
        return (newlist)

    def get_ecodrive_value(self,vehicle):

        requiredDir = 'C:\\Users\\thomas\\PycharmProjects\\virtualenv\\falcomserial\\conf'

        file = open(requiredDir + "\\ecodrive-dict", 'r', errors='replace')
        newlist = list()
        newdict = dict
        yaml_collection = yaml.load(file)
        # print(vehicle)
        if (yaml_collection["dict"]):
            # print("data in ecodrive library")
            ecodrive_library = yaml_collection["dict"]
            length = len(ecodrive_library)
            for i in range(length):
                newdict = yaml_collection["dict"][i]
                # print(yaml_collection["dict"][i])
                for i in newdict.keys():
                    if i == vehicle:
                        ecodrive_line = newdict[i]
                        # print(ecodrive_line)



        else:
            print("config file corrupted")
        return (ecodrive_line)


    def checkbox_manager(self,var):

        if var == 1:
            print("entered true")
            for child in self.Label_Frame.winfo_children():
                child.configure(state='normal')


        if(self.v.get()==0):
            print(" Yo Mate ! you need to get your shite together - select the mode of ignition")
        else :
            print(" Listen Mate ! let me manage this boxes for you")

    def build_settingscode(self):
        print ("Generating Settings code")
        print (" {} is the combobox value".format(self.box.get()))
        print("Ecodrive line is {}".format(self.get_ecodrive_value(self.box.get())))
        print (" {} is the radio button value".format(self.v.get()))

        settings_code = str(self.var1.get())+str(self.v.get())+str(self.var2.get())+str(self.var3.get())+str(self.var4.get())+str(self.var5.get())+str(self.var6.get())+str(self.var7.get())+str(self.var8.get())+str(self.var9.get())+str(self.var10.get())
        print (settings_code)



def main():
    root = Tk()
    app = ScriptGenerator()
    root.mainloop()


if __name__ == '__main__':
    main()