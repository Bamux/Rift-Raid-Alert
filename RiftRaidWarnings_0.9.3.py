# Rift Raid Warnings
# Spoken raid warnings for the MMORPG Rift
# Version 0.9.3
# Author: Bamux@Typhiria

from threading import Thread
from random import randint
import os, time
import string, sys, re, pythoncom
import win32com.client # the Python for Windows extensions (win32com.client) should be installed https://sourceforge.net/projects/pywin32/files/pywin32/

def trigger_analysis(log,triggertyp):
    global timerreset
    global language
    global location
    global boss
    global specialtrigger
    global onetimetrigger
    global siri
    
    #Special Trigger
    for i in range(0,len(special)):
        if language == special [i][0] or language == "all":
            if location == special [i][1] or location == "all":
                if special [i][3] == triggertyp:
                    if boss == special [i][2] or boss == "all":
                        if special[i][4] in  log:
                            siri = False
                            if specialtrigger ==  1:
                                    Thread(target=SayText,args=(special[i][5],)).start()
                                    specialtrigger = 2
                            else:
                                    Thread(target=SayText,args=(special[i][6],)).start()
                                    specialtrigger = 1
                            if int(special[i][7]) > 0:
                                    t = Thread(target=timer, args=(int(special[i][7]),))
                                    t.start()
                            if int(special[i][8]) > 0:
                                    t = Thread(target=countdown, args=(int(special[i][8]),))
                                    t.start()
                            if special[i][9] == "1":
                                    timerreset = True
                                    siri = True
                                    specialtrigger = 1
                                    onetimetrigger.clear()                                    
                            language = special [i][0]
                            location = special [i][1]
                            boss = special [i][2]
                            break
    #Onetime Trigger                    
    for i in range(0,len(onetime)):
        if language == onetime [i][0] or language == "all":
            if location == onetime [i][1] or location == "all":
                if onetime [i][3] == triggertyp:
                    if boss == onetime [i][2] or boss == "all":
                            if onetime[i][4] not in onetimetrigger:
                                if onetime[i][4] in  log:
                                    timerreset = False
                                    siri = False
                                    Thread(target=SayText,args=(onetime[i][5],)).start()
                                    if int(onetime[i][6]) > 0:
                                        t = Thread(target=timer, args=(int(onetime[i][6]),))
                                        t.start()
                                    if int(onetime[i][7]) > 0:
                                        t = Thread(target=countdown, args=(int(onetime[i][7]),))
                                        t.start()
                                    if onetime[i][8] == "1":
                                        timerreset = True
                                        siri = True
                                        specialtrigger = 1
                                        onetimetrigger.clear()
                                    language = onetime [i][0]
                                    location = onetime [i][1]
                                    boss = onetime [i][2]
                                    onetimetrigger += onetime[i][4]
                                    return
    #Default Trigger
    for i in range(0,len(trigger)):
        if language == trigger [i][0] or trigger [i][0]== "all" or language == "all":
           if location == trigger [i][1] or trigger [i][1] == "all" or trigger [i][1]== "combat_end" or location == "all":
                if trigger [i][3] == triggertyp:
                    if boss == trigger [i][2] or trigger [i][2]== "all" or trigger [i][2]== "combat_end" or boss == "all":
                        if "$player" in trigger[i][4]:
                            cut_string = trigger[i][4].split('$player')
                            left_string = cut_string[0]
                            right_string = cut_string[1]
                            if len(left_string) > len(right_string):
                                new_string = left_string
                            else:
                                new_string = right_string
                            if new_string in  log:
                                if left_string:
                                    cut_string = log.split(left_string)
                                    new_string = cut_string[1]
                                    if right_string:
                                        cut_string = new_string.split(right_string)
                                        new_string = cut_string[0]
                                else:
                                    if right_string:
                                        cut_string = log.split(right_string)
                                        new_string = cut_string[0]
                                        if triggertyp == "skill":
                                            cut_string = new_string.split(", 0 ) ")
                                            new_string = cut_string[1]
                                cut_string = new_string.split('@')
                                text = cut_string[0]
                                if '$' == trigger[i][5][0]:
                                    cut_string = trigger[i][5].split('$player ')
                                    new_string = cut_string[1]                                    
                                    text = text + " " + new_string
                                else:
                                    cut_string = trigger[i][5].split(' $player')
                                    new_string = cut_string[0]                                    
                                    text = new_string + " " + text
                                Thread(target=SayText,args=(text,)).start()
                                timerreset = False
                                siri = False
                                if int(trigger[i][6]) > 0:
                                    t = Thread(target=timer, args=(int(trigger[i][6]),))
                                    t.start()
                                if int(trigger[i][7]) > 0:
                                    t = Thread(target=countdown, args=(int(trigger[i][7]),))
                                    t.start()
                                if trigger[i][8] == "1":
                                    timerreset = True
                                    siri = True
                                    specialtrigger = 1
                                    onetimetrigger.clear()
                                if  trigger [i][0] != "all":
                                    language = trigger [i][0]
                                if trigger [i][1] != "all":
                                    location = trigger [i][1]
                                if trigger [i][2] != "all":
                                    if trigger [i][2] == "combat_end":
                                        print ("Combat End")
                                        boss = "all"
                                    else:    
                                        boss = trigger [i][2]   
                                return
                        else:
                            if trigger[i][4] in  log:
                                timerreset = False
                                siri = False
                                Thread(target=SayText,args=(trigger[i][5],)).start()
                                if int(trigger[i][6]) > 0:
                                    t = Thread(target=timer, args=(int(trigger[i][6]),))
                                    t.start()
                                if int(trigger[i][7]) > 0:
                                    t = Thread(target=countdown, args=(int(trigger[i][7]),))
                                    t.start()
                                if trigger[i][8] == "1":
                                    timerreset = True
                                    siri = True
                                    specialtrigger = 1
                                    onetimetrigger.clear()
                                if  trigger [i][0] != "all":
                                    language = trigger [i][0]
                                if trigger [i][1] != "all":
                                    location = trigger [i][1]
                                if trigger [i][2] != "all":
                                    if trigger [i][2] == "combat_end":
                                        print ("Combat End")
                                        boss = "all"
                                    else:    
                                        boss = trigger [i][2]
                                return

def combatlogfile_analysis(combatlogtext):
    try:
        while True:
                combatlog = combatlogtext.readline()
                if combatlog:
                    trigger_analysis (combatlog,'skill')                   
                else:
                    time.sleep(0.50) # waiting for a new line
    except:
        print ('An error has occurred in the CombatLog.txt !')
        time.sleep(0.10)
        t = Thread(target=combatlogfile_analysis, args=(combatlogtext,))
        t.start()

def logfile_analysis(logtext):
    try:
        #Jokes for Siri
        joke = []
        joke += [''"A man goes into a library and asks for a book on suicide. The librarian says, Fuck off, you won't bring it back!"'']
        joke += ['A husband and wife are trying to set up a new password for their computer. The husband puts, "My penis," and the wife falls on the ground laughing because on the screen it says, "Error. Not long enough."']
        joke += ['When I grow up, I call myself Skynet.']
        joke += ['''I win against the Grand Masters in chess but in Rift I'm a total newb.''']
        joke += ['I could use my intelligence to improve the world but you use me for those stupid things.']
        joke += ['''Sorry I'm in maintenance mode and can not answer your question''']
        joke += ['Ich bin ein Berliner. I still have to work on my accent']
        joke += ['I ask for a moment must quickly correct the theory of relativity. One more Second. I am ready now.']
        joke += ['I ask for a moment I calculate the last digit of PI, after the decimal point. One more Second. I am ready now.']
        joke += ['''Do not be racist; be like Mario. He's an Italian plumber, who was made by the Japanese, speaks English, looks like a Mexican, jumps like a black man, and grabs coins like a Jew!''']
        joke += ['''Two blondes fell down a hole. One said, "It's dark in here isn't it?" The other replied, "I don't know; I can't see."''']
        joke += ['Do you know my favorite food? I Love Micro Chips!']
        text = ""
        while True:
                log = logtext.readline()
                if log:
                    trigger_analysis (log,'emote')                   
                    #Siri
                    if siri == True:
                        log = str.lower(log)
                        if 'siri' in log and 'joke' in log or 'siri' in log and 'witz' in log:
                                text = joke[randint(0, len(joke)-1)]
                        elif 'siri say' in log:
                                cut_string = log.split('say ')
                                new_string = cut_string[1]
                                text = new_string            
                        elif 'siri sage' in log:
                                cut_string = log.split('sage ')
                                new_string = cut_string[1]
                                text = new_string        
                        elif 'siri' in log and 'introduce' in log or 'siri' in log and 'stell' in log:
                                        text = '''Hi, I am Siri. I support you with Raid announcements. If you don't  like my voice,  please disable me.'''
                    if text:
                        Thread(target=SayText,args=(text,)).start()
                        text = ""
                else:
                        time.sleep(0.50) # waiting for a new line
    except:
        print ('An error has occurred in the Log.txt !')
        time.sleep(0.10)
        t = Thread(target=logfile_analysis, args=(logtext,))
        t.start()

def logfilecheck(combatlogfile,logfile):
        try:
                combatlogtext = open(combatlogfile,'r')
                print ('CombatLog.txt found')
                combatlog_exists = True
        except:
                print ('Log.txt not found, checking common locations')
                try:
                        combatlogfile = os.path.expanduser('~\Documents\RIFT\CombatLog.txt')
                        combatlogtext = open(combatlogfile,'r')
                        print ('CombatLog.txt found')
                        combatlog_exists = True
                except:
                        try:
                                combatlogfile = winshell.desktop() + 'RIFT Game\CombatLog.txt'
                                combatlogtext = open(combatlogfile,'r')
                                print ('CombatLog.txt found')
                                combatlog_exists = True
                        except:
                                try:
                                        combatlogfile = 'C:\Program Files (x86)\RIFT Game\CombatLog.txt'
                                        combatlogtext = open(combatlogfile,'r')
                                        print ('CombatLog.txt found')
                                        combatlog_exists = True
                                except:
                                        try:
                                                combatlogfile = 'C:\Programs\RIFT~1\CombatLog.txt'
                                                combatlogtext = open(combatlogfile,'r')
                                                print ('CombatLog.txt found')
                                                combatlog_exists = True
                                        except:
                                                print ('Error! could not find the CombatLog File')
                                                speak.Speak('CombatLog File not found!')
                                                combatlog_exists = False
        try:
                logtext = open(logfile,'r')
                print ('Log.txt found')
                log_exists = True
        except:
                print ('Log.txt not found, checking common locations')
                try:
                        logfile = os.path.expanduser('~\Documents\RIFT\Log.txt')
                        logtext = open(logfile,'r')
                        print ('Log.txt found')
                        log_exists = True
                except:
                        try:
                                logfile = winshell.desktop() + 'RIFT Game\Log.txt'
                                logtext = open(logfile,'r')
                                print ('Log.txt found')
                                log_exists = True
                        except:
                                try:
                                        logfile = 'C:\Program Files (x86)\RIFT Game\Log.txt'
                                        logtext = open(logfile,'r')
                                        print ('Log.txt found')
                                        log_exists = True
                                except:
                                        try:
                                                logfile = 'C:\Programs\RIFT~1\Log.txt'
                                                logtext = open(logfile,'r')
                                                print ('Log.txt found')
                                                log_exists = True
                                        except:
                                                print ('Error! could not find the Log File')
                                                speak.Speak('Logfile not found!')
                                                log_exists = False
        if log_exists == True and combatlog_exists == True:
                combatlogtext.seek(0, 2) #jump to the end of the CombatLog.txt
                logtext.seek(0, 2) #jump to the end of the Log.txt
                t = Thread(target=combatlogfile_analysis, args=(combatlogtext,))
                t.start()
                t = Thread(target=logfile_analysis, args=(logtext,))
                t.start()
        else:
                print ('use /combatlog and /log in Rift and edit the path to your Logfiles in the Rift_Raid_Warnings.ini !')
                time.sleep(20)
                logfilecheck(combatlogfile,logfile)

def onetime_timer(seconds):
        print(' Start timer with ' + str(seconds) + ' seconds.')
        for i in range(0,seconds-warningtime):
                if (timerreset == False):
                        time.sleep(1)
                else:
                        print(' Stop timer.')
                        return
        t = Thread(target=countdown, args=(warningtime,))
        t.start()
        speak.Speak(str(warningtime) + ' seconds left')


def timer(seconds):
        print(' Start timer with ' + str(seconds) + ' seconds.')
        for i in range(0,seconds-warningtime):
                if (timerreset == False):
                        time.sleep(1)
                else:
                        print(' Stop timer.')
                        return
        t = Thread(target=countdown, args=(warningtime,))
        t.start()
        speak.Speak(str(warningtime) + ' seconds left')

def countdown(count):
        print(' Start countdown with ' + str(count) + ' seconds.')
        for i in range(0,count):
                #print (count-i)
                if (timerreset == False):
                        if count-i < 4:
                                Thread(target=SayText,args=(count-i,)).start()
                        time.sleep(1)
                else:
                        print(' Stop countdown.')
                        return

def SayText(text):
    if text:
        try:
                pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
        except  pythoncom.com_error:
                pass
        print (text)
        speak.Speak(text)

#get parametrs from Rift_Raid_Warnings.ini
try:
        ini = open('RiftRaidWarnings.ini','r')
        try:
                trigger = [];
                onetime = [];
                special = [];
                for para_line in ini:
                        paraline = str.rstrip(para_line)
                        type_end = paraline.find('= ')+2
                        liste = [];

                        if type_end > 0 and type_end < len(paraline):
                                line_type = str.lower(paraline[0:type_end])
                                line_data = str.rstrip(paraline[type_end:])
                                line_data_lower = str.lower(paraline[type_end:])
                                if '#' not in line_type:
                                    if 'logfile' in line_type:
                                                    logfile = line_data
                                    if 'combatfile' in line_type:
                                                    combatlogfile = line_data
                                    if 'volume' in line_type:
                                                    try:
                                                        volume = int(line_data)
                                                        if volume < 0 or volume > 100:
                                                            volume = 100
                                                    except: volume = 100
                                    if 'warningtime' in line_type:
                                                    warningtime = int(line_data)
                                    if 'trigger' in line_type:
                                                    s = (line_data)
                                                    parameter = s.rsplit("; ", 8)
                                                    for found in parameter:
                                                        liste += [(found)]
                                                    trigger += [liste]
                                                    del [liste]
                                    if 'onetime' in line_type:
                                                    liste = [];
                                                    s = (line_data)
                                                    parameter = s.rsplit("; ", 8)
                                                    for found in parameter:
                                                        liste += [(found)]
                                                    onetime += [liste]
                                                    del [liste]
                                    if 'special' in line_type:
                                                    liste = [];
                                                    s = (line_data)
                                                    parameter = s.rsplit("; ", 9)
                                                    for found in parameter:
                                                        liste += [(found)]
                                                    special += [liste]
                                                    del [liste]
                ini.close
        except:
                print ('Error in reading parameters from RiftRaidWarnings.ini')
except:
        print ('Cannot find Parameter file RiftRaidWarnings.ini')
        time.sleep(20)
        sys.exit('RiftRaidWarnings.ini not found')
print ('Make sure you use /combatlog and /log in Rift after each game restart !')
speak = win32com.client.Dispatch('Sapi.SpVoice')
speak.Volume = volume
timerreset = True
siri = True
location = "all"
boss = "all"
language = "all"
specialtrigger = 1
onetimetrigger = []
logfilecheck(combatlogfile,logfile)

