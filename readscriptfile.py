import os

currentWorkingDir = os.getcwd()
requiredDir = 'C:\\falcomserial'

print(requiredDir)


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



for filename in os.listdir(requiredDir):
    print (filename)
    file = open(requiredDir + "\\" + filename, 'r', errors='replace')
    newfile_flag=1

    filename = filename.split('.txt')
    print('Parsing {}'.format(filename[0]))
    currentscript = script(filename[0])
    tlno = 0
    for line in file:
        tlno += 1
        currentscript.add_line(line, tlno)
    currentscript.print_script_summary()
