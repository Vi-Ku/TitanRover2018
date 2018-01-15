import sys
import os
from shutil import copyfile
from subprocess import Popen
import subprocess
import json

class c:
    BLUE = '\033[34m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    CYAN = '\033[36m'
    MAGENTA = '\033[35'
    RED = '\033[31m'
    DEFAULT = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


processes   = json.load(open('processes.json'))
path        = json.load(open('pathToTitanRover.json'))

cronLinesFromProcesses = []

crontab = '/etc/crontab'

if sys.platform != "linux":
        if sys.platform != "linux2":
            print("Your system: " + sys.platform)
            print(c.RED+"\nThis script was written ONLY for Linux OS."+c.DEFAULT)
            sys.exit()

if os.getuid() is not 0:
    print(c.RED+"Please run script as sudo:\n\t"+c.YELLOW+"sudo python processMan.py\n"+c.DEFAULT)
    sys.exit()

if path["path"] == None or path["path"][-1:] == "/":
    print(c.RED+"\nYou need to specify a path in the path.json file first.")
    print(" Otherwise, We cannot setup a startup process for you.")
    print(" an EXAMPLE of path.json might look like this:")
    print(c.YELLOW+"    { \"path\": \"/home/audstanley/Documents\" }"+c.DEFAULT)
    print(c.BLUE+"      Your path MUST point to where the TitanRover2018 Folder is.\n\n"+c.DEFAULT)
    print(c.BLUE+"      and you MUST NOT leave a trailing slash in your path\n\n"+c.DEFAULT)
    sys.exit()
else:
    # look to see if screen exists
    p1 = Popen([ "whereis", "screen" ], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    p2 = Popen([ "whereis", "iftop" ], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    p3 = Popen([ "whereis", "pip" ], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    p4 = Popen([ "whereis", "motion" ], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    
    # automatically install dependencies if it does not exists.
    if p1[8:] == "":
        print(c.YELLOW+"Installing screen, Please wait..."+c.DEFAULT)
        Popen([ "sudo", "apt-get", "install", "screen", "-y"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    
    if p2[7:] == "":
        print(c.YELLOW+"Installing iftop, Please wait..."+c.DEFAULT)
        Popen([ "sudo", "apt-get", "install", "iftop", "-y"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    
    if p3[5:] == "":
        print(c.YELLOW+"Installing python-pip, Please wait..."+c.DEFAULT)
        Popen([ "sudo", "apt-get", "install", "python-pip", "-y"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    if p4[8:] == "" or len(p4) == 20:
        print(c.YELLOW+"Installing motion, Please wait..."+c.DEFAULT)
        Popen([ "sudo", "apt-get", "install", "motion", "-y"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        try:
            copyfile("motionConf/motion.conf", "/etc/motion/motion.conf")
            copyfile("motionConf/thread1.conf", "/etc/motion/thread1.conf")
            copyfile("motionConf/thread2.conf", "/etc/motion/thread2.conf")
            copyfile("motionConf/thread3.conf", "/etc/motion/thread3.conf")
            copyfile("motionConf/thread4.conf", "/etc/motion/thread4.conf")
        except:
            print("There was a problem trying to copy one of the motion configure files")

    # install requests dependency, if not installed
    try:
        __import__("requests") 
    except:
        print(c.YELLOW+"Installing requests for python, Please wait..."+c.DEFAULT)
        Popen([ "sudo", "apt-get", "install", "python-requests", "-y"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    with open(crontab, 'r') as file:
        lines = file.readlines()

    file.close()

    cronLineA   = "@reboot root cd"
    cronLineB   = "&& screen -dmLS"
    cronLineC   = "&& screen -S"
    cronLineD   = "-X stuff \""
    cronLineE   = "\\015\";\n"

    for o in processes:
        # cronLineA           path["path"]                  o["path"]                                             cronLineB                 o["screenName"]      cronLineC       o["screenName"]       cronLineD        o["python"] o["script"]   cronLineD
        # {@reboot root cd} {/home/audstanley/Documents} {/TitanRover2018/rover/core/servers/ArduinoSocketServer/} {&& /usr/bin/screen -dmLS }    {mobility}       {&& screen -S }   {mobility}            { -X stuff "}   {python}     {mobility.py}  \015";\n
        cronLinesFromProcesses.append("{} {}{} {} {} {} {} {}{} {} {}".format(cronLineA, path["path"], o["path"], cronLineB, o["screenName"], cronLineC, o["screenName"], cronLineD , o["python"], o["script"], cronLineE))
                                    #  cA p1p2 cB oS cC oS cD oPoX cE
    #print(cronLinesFromProcesses)
    if len(lines) > 1 and len(cronLinesFromProcesses) > 1:
        dif = [v for v in lines if v not in cronLinesFromProcesses]
        if len(dif) > 0:
            file = open(crontab, 'w')
            for i in dif:
                file.write(i)
            for i in cronLinesFromProcesses:
                file.write(i)
            file.close()

    print(c.YELLOW+"Setup is complete"+c.DEFAULT)