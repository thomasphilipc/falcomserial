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

    script = """ // Movement filtering
$PFAL,CNF.Set,AL4=Sys.Timer.e4&GPS.Nav.sFix=correct&GPS.Nav.sSpeed>=1&Sys.nvCounter.s5<60:Sys.nvCounter5.Increment=1
$PFAL,CNF.Set,AL6=Sys.Timer.e4&GPS.Nav.sFix=correct&GPS.Nav.sSpeed<1&Sys.nvCounter.s5>0:Sys.nvCounter5.Decrement=1

$PFAL,CNF.Set,AL7=Sys.Timer.e4&GPS.Nav.sFix=Invalid&Sys.nvCounter.s2=1&Sys.nvCounter.s5<20:Sys.nvCounter5.Increment=1
$PFAL,CNF.Set,AL10=Sys.Timer.e4&GPS.Nav.sFix=Invalid&Sys.nvCounter.s2=0&Sys.nvCounter.s5>0:Sys.nvCounter5.Decrement=1

$PFAL,CNF.Set,AL39=IO.Motion.eMoving?IO.Motion.sMoving:Sys.nvCounter2.set=1
$PFAL,CNF.Set,AL40=IO.Motion.eStanding?IO.Motion.sStanding:Sys.nvCounter2.set=0 """

    total_line=0
    for line in script.splitlines():
        if line:
            print(line)
            if line.startswith("$"):
                total_line += 1
                # print(re.findall(r"[\W']+", line))
                list1=re.findall(r"[\W']+", line)
                # print(re.findall(r"[\w']+", line))
                list2=re.findall(r"[\w']+", line)
                result = [None] * (len(list1) + len(list2))
                result[::2] = list1
                result[1::2] = list2
                print("Combined list")
                print(result)
                status=verify_line(line,result)
                print(status)
                if status:
                    for item in result:
                        print(item)



    print ("there are a total of {}".format(total_line))

def verify_line(line,split_list):
    my_lst_str = ''.join(map(str, split_list))
    print("back to string")
    print(my_lst_str)
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