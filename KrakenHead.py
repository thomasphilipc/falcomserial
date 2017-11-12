################## YAML SAMPLE FOR CONFIGURATION ########################

# function_id : 1001
# name: Ignition Detection via Alternator
# version: 1.0
# description: Ignition detection is carried out via alternator
# uid: IGN01AFE
# exclusive: True
# dependancies: [1009,1003]
# hardware_io_used:
# 	- [fox3,01]
# 	- [fox2,01]
# 	- [bolero,02]
# counter_used:[01,02]
# trigger_used:[01,02]]
# state_used:[01,02]
# alarmlines_used:
# date_updated: [25,26]
# user_updated:

import os
import yaml
import re

# conf = """kraken-script-configuration:
# - updated-timestamp: 08-Nov-2017
# - updated-by: thomas.philip@roamworks.com
# - version-number : 10001
# - total-libs : 1
# lib-info:
#   - {name: ignition Detection via Alternator, version: 1.0, description: Ignition detection is carried out via alternator, uid: IGN01AFE, exclusive: True, hardware_io_used : {fox3: 01, fox2: 01,bolero: 02 }, counter-used: [01,02], trigger-used: [01,02 ], state-used: [01,02], alarmlines-used: [25,26], timestamp-updated : 08-Nov-2017, user-updated: thomas.philip@roamworks.com}
# """
#







def initialize():
    print("Read configuration file")

    requiredDir = 'C:\\Users\\thomas\\PycharmProjects\\virtualenv\\falcomserial\\conf'


    file = open(requiredDir + "\\init.conf", 'r', errors='replace')

    yaml_collection = yaml.load(file)

    # print("below is the contents in config file")
    # print(yaml_collection)
    # print("total collections in config file")
    # print(len(yaml_collection))

    if (yaml_collection["kraken-script-configuration"]):
        # print("length of contents in kraken script")
        # length = len(yaml_collection["kraken-script-configuration"])
        # print(length)
        # print("data in kraken inforation")
        # print(yaml_collection["kraken-script-configuration"])
        list = yaml_collection["kraken-script-configuration"]
        updated_timestamp=list[0]["updated-timestamp"]
        updated_by=list[1]["updated-by"]
        version_number=list[2]["version-number"]
        total_libs=list[3]["total-libs"]
        print(" The file was last update on {} by {} . Version number = {} contains {} libraries".format(updated_timestamp,updated_by,version_number,total_libs))
    else:
        print("config file corrupted")

    if (yaml_collection["lib-info"]):
        print("data in library")
        length = len(yaml_collection["lib-info"])
        for i in range(len(yaml_collection["lib-info"])):
            print(yaml_collection["lib-info"][i]["name"])
    else:
        print("config file corrupted")

def parse_script():
    print("function to parse script")

    script = """ //	This OTA version is only compatible to move from "Royal Truck Portable V2.0t" to "ROYAL-FM-FOX-MOV-DHL-AN-v2.1"
//	v2.1	:	improved TCP disconnection reboot
//				improved movement logic
//				improved blacklist for T-Mobile
//				Operator selection changed to any
//				DNS updated
//
//Device name
$PFAL,Cnf.Set,DEVICE.NAME=ROYAL-FM-FOX-MOV-DHL-AN-v2.1

////Replace for Bolero
$PFAL,Cnf.Set,REPLACE0=4 &(IMEI),&(Time),&(Date),&(Lat),&(Lon),&(Fix),&(Course),&(Speed),&(NavDist),&(Power),&(Bat),&(IN7),&(DOP),&(SatsUsed)

//Journey Periodic Timer
$PFAL,Cnf.Set,MACRO2=Sys.Timer2.start=cyclic,900000

//Synchronous timer
$PFAL,Cnf.Set,MACRO4=Sys.TIMER4.start=cyclic,1000

$PFAL,CNF.Set,AL1=SYS.Device.eStart:GPS.Nav.Position1=load1&GPS.Nav.Position0=load1&GPS.Nav.Position4=none&Sys.Trigger0.Load0&Sys.MACRO4


// Movement filtering
$PFAL,CNF.Set,AL4=Sys.Timer.e4&GPS.Nav.sFix=correct&GPS.Nav.sSpeed>=1&Sys.nvCounter.s5<60:Sys.nvCounter5.Increment=1
$PFAL,CNF.Set,AL6=Sys.Timer.e4&GPS.Nav.sFix=correct&GPS.Nav.sSpeed<1&Sys.nvCounter.s5>0:Sys.nvCounter5.Decrement=1

$PFAL,CNF.Set,AL7=Sys.Timer.e4&GPS.Nav.sFix=Invalid&Sys.nvCounter.s2=1&Sys.nvCounter.s5<20:Sys.nvCounter5.Increment=1
$PFAL,CNF.Set,AL10=Sys.Timer.e4&GPS.Nav.sFix=Invalid&Sys.nvCounter.s2=0&Sys.nvCounter.s5>0:Sys.nvCounter5.Decrement=1

$PFAL,CNF.Set,AL39=IO.Motion.eMoving?IO.Motion.sMoving:Sys.nvCounter2.set=1
$PFAL,CNF.Set,AL40=IO.Motion.eStanding?IO.Motion.sStanding:Sys.nvCounter2.set=0


// Start/Stop Moving messages
$PFAL,CNF.Set,AL8=Sys.nvCounter.s5>=15&Sys.nvCounter.s4=0:Sys.MACRO2&Sys.nvCounter4.Set=1&TCP.Client.Send,0,"STA (REPLACE0)"
$PFAL,CNF.Set,AL9=Sys.nvCounter.s5<2&Sys.nvCounter.s4=1:Sys.Timer2.stop&Sys.nvCounter4.Set=0&TCP.Client.Send,0,"STO (REPLACE0)"

//Geofence
$PFAL,CNF.Set,AL26=GPS.Geofence.eX=inside&Sys.nvCounter.s6=0:Sys.nvCounter6.Set=1&TCP.Client.Send,0,"GEOIN (REPLACE0)"
$PFAL,CNF.Set,AL27=GPS.Geofence.eX=outside&Sys.nvCounter.s6=1:Sys.nvCounter6.Set=0&TCP.Client.Send,0,"GEOEX (REPLACE0)"

// Overspeed
$PFAL,CNF.Set,AL28=GPS.Nav.sSpeed>=29&GPS.Nav.sFix=correct&Sys.nvCounter.s4=1&Sys.Trigger.s3=low:Sys.Trigger3=high&TCP.Client.Send,0,"OSPS (REPLACE0)"
$PFAL,CNF.Set,AL29=Sys.Trigger.s3=high&GPS.Nav.sSpeed<27&GPS.Nav.sFix=correct:Sys.Trigger3=low&TCP.Client.Send,0,"OSPE (REPLACE0)"

//Connection Reset
$PFAL,CNF.Set,AL30=TCP.Client.sDisconnected&SYS.TIMER.s0=inactive&Sys.nvCounter.s0=0:Sys.nvCounter0.Set=1&SYS.TIMER6.start=single,1800000
$PFAL,CNF.Set,AL31=TCP.Client.sConnected&Sys.nvCounter.s0=1:Sys.nvCounter0.Set=0&SYS.TIMER6.stop
$PFAL,CNF.Set,AL32=SYS.TIMER.e6&Sys.nvCounter.s0=1:Sys.nvCounter0.Set=0&Sys.device.reset,0

//Weekly reboot
// Weekly Reboot (once a week at Friday midnight)
$PFAL,CNF.Set,AL61=GPS.Time.sHour=20&GPS.Time.sWDay=5&GPS.Time.eMinute=1:Sys.Trigger9=high
$PFAL,CNF.Set,AL38=Sys.Trigger.s9=high&Sys.nvCounter.s4=0:Sys.Device.Reset,0

$PFAL,CNF.Set,GSM.OPERATOR.BLACKLIST="42203","41602","41603","42002","42003","42004","42005","42007","42021","42602","42604","41903","41902"
$PFAL,CNF.Set,GSM.OPERATOR.SELECTION=any

//Remove early set backup
$PFAL,Cnf.EraseBackup

//Alarm hide
$PFAL,Sys.Security.HideAlarm," R0O4A3M9W0O0R2K7S0"

//Configuration backup
$PFAL,Cnf.Backup"""

    total_line=0
    alarm_collection=[]
    counter_collection=[]
    timer_collection=[]
    for line in script.splitlines():
        if line:
            #print(line)
            if line.startswith("$"):
                line=line.capitalize()
                #print(line)
                total_line += 1
                # print(re.findall(r"[\W']+", line))
                list1=re.findall(r"[\W']+", line)
                # print(re.findall(r"[\w']+", line))
                list2=re.findall(r"[\w']+", line)
                result = [None] * (len(list1) + len(list2))
                result[::2] = list1
                result[1::2] = list2
                # print("Combined list")
                print(result)
                status=verify_line(line,result)
                # print(status)
                if status:
                    for item in result:
                        #print(item)
                        if item in ['$','PFAL']:
                            pass
                        elif str(item).startswith('al'):
                            alarm=str(item)
                            alarm_line=alarm.split('al')
                            print ("Alarm line used {}".format(alarm_line[1]))
                            alarm_collection.append(alarm_line[1])
                        elif str(item).startswith('nvcounter'):
                            counter=str(item)
                            counter_line=counter.split('nvcounter')
                            if counter_line[1]:
                                print ("Counter used {}".format(counter_line[1]))
                                counter_collection.append(counter_line[1])
                        elif str(item).startswith('timer'):
                            timer=str(item)
                            timer_line=timer.split('timer')
                            if timer_line[1]:
                                print ("Counter used {}".format(timer_line[1]))
                                timer_collection.append(timer_line[1])
                else:
                    print("issue occured")


    print ("there are a total of {} lines".format(total_line))
    print ("alarm's used are {}".format(alarm_collection))
    print ("counter's used are {}".format(counter_collection))
    print("timer's used are {}".format(timer_collection))

def verify_line(line,split_list):
    my_lst_str = ''.join(map(str, split_list))
    # print("back to string")
    # print(my_lst_str)
    if (my_lst_str == line):
        # print("sucess bois")
        return True
    else:
        # print("woops")
        return False
################# CLASS FOR FUNCTIONALITY #######################
class funtionality :
    name = "None"
    version = "None"
    description = "None"
    uid = "None"
    exclusive_flag = False
    io_used = []
    hardware_support = []
    counters_used = []
    triggers_used = []


    def load_functions(self):
        print ("calling function to load all functionalities")


#initialize()


parse_script()