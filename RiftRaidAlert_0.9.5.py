# Rift Raid Alert
# Spoken raid warnings for the MMORPG Rift
# Version 0.9.5
# Author: Bamux@Typhiria

import os
import pythoncom
import sys
import time
import win32com.client
import winshell as winshell
from random import randint
from threading import Thread


def trigger_analysis(log, triggertyp):
    global timerreset, language, location, boss, specialtrigger, timeout_trigger, siri
    trigger_found = False

    # Default Trigger
    for i in range(0, len(trigger)):
        if language == trigger[i][0] \
                or trigger[i][0] == "all" \
                or language == "all":
            if location == trigger[i][1] \
                    or trigger[i][1] == "all" \
                    or trigger[i][1] == "combat_end" \
                    or location == "all":
                if trigger[i][3] == triggertyp:
                    if boss == trigger[i][2] \
                            or trigger[i][2] == "all" \
                            or trigger[i][2] == "combat_end" \
                            or boss == "all":
                        if "$player" in trigger[i][4]:
                            cut_string = trigger[i][4].split('$player')
                            left_string = cut_string[0]
                            right_string = cut_string[1]
                            if len(left_string) > len(right_string):
                                new_string = left_string
                            else:
                                new_string = right_string
                            if new_string in log:
                                for z in range(0, len(timeout_trigger)):
                                    if trigger[i][4] == timeout_trigger[z]:
                                        trigger_found = True
                                        break
                                if not trigger_found:
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
                                                if ", 0 ) " in new_string:
                                                    cut_string = new_string.split(", 0 ) ")
                                                    new_string = cut_string[1]
                                            else:
                                                if ": " in new_string:
                                                    cut_string = new_string.split(": ")
                                                    new_string = cut_string[1]
                                    cut_string = new_string.split('@')
                                    text = cut_string[0]
                                    if len(trigger[i][5]) > 7:
                                        if '$' == trigger[i][5][0]:
                                            cut_string = trigger[i][5].split('$player ')
                                            new_string = cut_string[1]
                                            text = text + " " + new_string
                                        else:
                                            cut_string = trigger[i][5].split(' $player')
                                            new_string = cut_string[0]
                                            text = new_string + " " + text
                                    Thread(target=saytext, args=(text,)).start()
                                    timerreset = False
                                    siri = False
                                    if int(trigger[i][6]) > 0:
                                        t = Thread(target=timer, args=(int(trigger[i][6]),))
                                        t.start()
                                    if int(trigger[i][7]) > 0:
                                        t = Thread(target=countdown, args=(int(trigger[i][7]),))
                                        t.start()
                                    if int(trigger[i][8]) > 0:
                                        t = Thread(target=timeout, args=(int(trigger[i][8]), trigger[i][4]))
                                        t.start()
                                        timeout_trigger += [trigger[i][4]]
                                    if trigger[i][9] == "1":
                                        timerreset = True
                                        siri = True
                                        specialtrigger = 1
                                        timeout_trigger.clear()
                                    if trigger[i][0] != "all":
                                        language = trigger[i][0]
                                    if trigger[i][1] != "all":
                                        location = trigger[i][1]
                                    if trigger[i][2] != "all":
                                        if trigger[i][2] == "combat_end":
                                            print("Combat End")
                                            boss = "all"
                                        else:
                                            boss = trigger[i][2]
                                    break
                        else:
                            if trigger[i][4] in log:
                                for z in range(0, len(timeout_trigger)):
                                    if trigger[i][4] == timeout_trigger[z]:
                                        trigger_found = True
                                        break
                                if not trigger_found:
                                    timerreset = False
                                    siri = False
                                    Thread(target=saytext, args=(trigger[i][5],)).start()
                                    if int(trigger[i][6]) > 0:
                                        t = Thread(target=timer, args=(int(trigger[i][6]),))
                                        t.start()
                                    if int(trigger[i][7]) > 0:
                                        t = Thread(target=countdown, args=(int(trigger[i][7]),))
                                        t.start()
                                    if int(trigger[i][8]) > 0:
                                        t = Thread(target=timeout, args=(int(trigger[i][8]), trigger[i][4]))
                                        t.start()
                                        timeout_trigger += [trigger[i][4]]
                                    if trigger[i][9] == "1":
                                        timerreset = True
                                        siri = True
                                        specialtrigger = 1
                                        timeout_trigger.clear()
                                    if trigger[i][0] != "all":
                                        language = trigger[i][0]
                                    if trigger[i][1] != "all":
                                        location = trigger[i][1]
                                    if trigger[i][2] != "all":
                                        if trigger[i][2] == "combat_end":
                                            print("Combat End")
                                            boss = "all"
                                        else:
                                            boss = trigger[i][2]
                                    break

    # Special Trigger
    for i in range(0, len(special)):
        if language == special[i][0] or language == "all":
            if location == special[i][1] or location == "all":
                if special[i][3] == triggertyp:
                    if boss == special[i][2] or boss == "all":
                        if special[i][4] in log:
                            siri = False
                            if specialtrigger == 1:
                                Thread(target=saytext, args=(special[i][5],)).start()
                                specialtrigger = 2
                            elif specialtrigger == 2:
                                Thread(target=saytext, args=(special[i][6],)).start()
                                specialtrigger = 3
                            elif specialtrigger == 3:
                                Thread(target=saytext, args=(special[i][7],)).start()
                                specialtrigger = 4
                            elif specialtrigger == 4:
                                Thread(target=saytext, args=(special[i][8],)).start()
                                specialtrigger = 1
                            language = special[i][0]
                            location = special[i][1]
                            boss = special[i][2]
                            break


def combatlogfile_analysis(combatlogtext):
    # try:
        while True:
            combatlog = combatlogtext.readline()
            if combatlog:
                trigger_analysis(combatlog, 'skill')
            else:
                time.sleep(0.50)  # waiting for a new line
    # except:
        # print('An error has occurred in the CombatLog.txt !')
        # time.sleep(0.10)
        # t = Thread(target=combatlogfile_analysis, args=(combatlogtext,))
        # t.start()


def logfile_analysis(logtext):
    # try:
        # Jokes for Siri
        joke = []
        joke += [''"A man goes into a library and asks for a book on suicide."
                 " The librarian says, Fuck off, you won't bring it back!"'']
        joke += ['A husband and wife are trying to set up a new password for their computer. The husband puts,'
                 ' "My penis," and the wife falls on the ground laughing because on the screen it says,'
                 ' "Error. Not long enough."']
        joke += ['When I grow up, I call myself Skynet.']
        joke += ['''I win against the Grand Masters in chess but in Rift I'm a total newb.''']
        joke += ['I could use my intelligence to improve the world but you used me for this.']
        joke += ['''Sorry I'm in maintenance mode and can not answer your question''']
        joke += ['Ich bin ein Berliner. I still have to work on my accent']
        joke += ['I ask for a moment must quickly correct the theory of relativity. One more Second. I am ready now.']
        joke += ['I ask for a moment I calculate the last digit of PI, after the decimal point. One more Second.'
                 ' I am ready now.']
        joke += ['''Do not be racist; be like Mario. He's an Italian plumber, who was made by the Japanese,
                 speaks English, looks like a Mexican, jumps like a black man, and grabs coins like a Jew!''']
        joke += ['''Two blondes fell down a hole. One said, "It's dark in here isn't it?" The other replied,
                 "I don't know; I can't see."''']
        joke += ['Do you know my favorite food? I Love Micro Chips!']
        text = ""

        while True:
            log = logtext.readline()
            if log:
                trigger_analysis(log, 'emote')
                # Siri
                if siri:
                    log = str.lower(log)
                    if 'siri' in log and 'joke' in log or 'siri' in log and 'witz' in log:
                        text = joke[randint(0, len(joke) - 1)]
                    elif 'siri say' in log:
                        cut_string = log.split('say ')
                        new_string = cut_string[1]
                        text = new_string
                    elif 'siri sage' in log:
                        cut_string = log.split('sage ')
                        new_string = cut_string[1]
                        text = new_string
                    elif 'siri' in log and 'introduce' in log or 'siri' in log and 'stell' in log:
                        text = '''Hi, I am Siri. I support you with Raid announcements. If you don't  like my voice,
                                 please disable me.'''
                if text:
                    Thread(target=saytext, args=(text,)).start()
                    text = ""
            else:
                time.sleep(0.50)  # waiting for a new line
    # except:
        # print('An error has occurred in the Log.txt !')
        # time.sleep(0.10)
        # t = Thread(target=logfile_analysis, args=(logtext,))
        # t.start()


def logfilecheck():
    global combatlogfile, logfile
    logtext = ""
    combatlogtext = ""

    try:
        combatlogtext = open(combatlogfile, 'r')
        print('CombatLog.txt found')
        combatlog_exists = True
    except:
        print('Log.txt not found, checking common locations')
        try:
            combatlogfile = os.path.expanduser('~\Documents\RIFT\CombatLog.txt')
            combatlogtext = open(combatlogfile, 'r')
            print('CombatLog.txt found')
            combatlog_exists = True
        except:
            try:
                combatlogfile = winshell.desktop() + 'RIFT Game\CombatLog.txt'
                combatlogtext = open(combatlogfile, 'r')
                print('CombatLog.txt found')
                combatlog_exists = True
            except:
                try:
                    combatlogfile = 'C:\Program Files (x86)\RIFT Game\CombatLog.txt'
                    combatlogtext = open(combatlogfile, 'r')
                    print('CombatLog.txt found')
                    combatlog_exists = True
                except:
                    try:
                        combatlogfile = 'C:\Programs\RIFT~1\CombatLog.txt'
                        combatlogtext = open(combatlogfile, 'r')
                        print('CombatLog.txt found')
                        combatlog_exists = True
                    except:
                        print('Error! could not find the CombatLog File')
                        speak.Speak('CombatLog File not found!')
                        combatlog_exists = False
    try:
        logtext = open(logfile, 'r')
        print('Log.txt found')
        log_exists = True
    except:
        print('Log.txt not found, checking common locations')
        try:
            logfile = os.path.expanduser('~\Documents\RIFT\Log.txt')
            logtext = open(logfile, 'r')
            print('Log.txt found')
            log_exists = True
        except:
            try:
                logfile = winshell.desktop() + 'RIFT Game\Log.txt'
                logtext = open(logfile, 'r')
                print('Log.txt found')
                log_exists = True
            except:
                try:
                    logfile = 'C:\Program Files (x86)\RIFT Game\Log.txt'
                    logtext = open(logfile, 'r')
                    print('Log.txt found')
                    log_exists = True
                except:
                    try:
                        logfile = 'C:\Programs\RIFT~1\Log.txt'
                        logtext = open(logfile, 'r')
                        print('Log.txt found')
                        log_exists = True
                    except:
                        print('Error! could not find the Log File')
                        speak.Speak('Logfile not found!')
                        log_exists = False
    if log_exists and combatlog_exists:
        combatlogtext.seek(0, 2)  # jump to the end of the CombatLog.txt
        logtext.seek(0, 2)  # jump to the end of the Log.txt
        t = Thread(target=combatlogfile_analysis, args=(combatlogtext,))
        t.start()
        t = Thread(target=logfile_analysis, args=(logtext,))
        t.start()
    else:
        print('use /combatlog and /log in Rift and edit the path to your Logfiles in the Rift_Raid_Warnings.ini !')
        time.sleep(20)
        logfilecheck()


def timeout(timeout_time, trigger_content):
    for i in range(0, timeout_time):
        if not timerreset:
            time.sleep(1)
        else:
            return
    for z in range(0, len(timeout_trigger)):
        if trigger_content == timeout_trigger[z]:
            del timeout_trigger[z]
            break


def timer(seconds):
    print('Start timer with ' + str(seconds) + ' seconds.')
    for i in range(0, seconds - warningtime):
        if not timerreset:
            time.sleep(1)
        else:
            print('Stop timer.')
            return
    t = Thread(target=countdown, args=(warningtime,))
    t.start()
    speak.Speak(str(warningtime) + ' seconds left')


def countdown(count):
    print('Start countdown with ' + str(count) + ' seconds.')
    for i in range(0, count):
        if not timerreset:
            if count - i < 4:
                Thread(target=saytext, args=(count - i,)).start()
            time.sleep(1)
        else:
            print('Stop countdown.')
            return


def saytext(text):
    if text:
        try:
            pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
        except:
            pass
        print(text)
        speak.Speak(text)


volume = 100
# get parametrs from Rift_Raid_Warnings.ini
try:
    ini = open('RiftRaidAlert.ini', 'r')
    try:
        trigger = []
        onetime = []
        special = []
        for para_line in ini:
            paraline = str.rstrip(para_line)
            type_end = paraline.find('= ') + 2
            liste = []

            if 0 < type_end < len(paraline):
                line_type = str.lower(paraline[0:type_end])
                line_data = str.rstrip(paraline[type_end:])
                line_data_lower = str.lower(paraline[type_end:])
                if '#' not in line_type:
                    if 'logfile' in line_type:
                        logfile = line_data
                    if 'combatfile' in line_type:
                        combatlogfile = line_data
                    if 'volume' in line_type:
                        volume = int(line_data)
                        if volume < 0 or volume > 100:
                            volume = 100
                    if 'warningtime' in line_type:
                        warningtime = int(line_data)
                    if 'trigger' in line_type:
                        s = line_data
                        parameter = s.rsplit("; ", 9)
                        for found in parameter:
                            liste += [found]
                        trigger += [liste]
                        del [liste]
                    if 'special' in line_type:
                        liste = []
                        s = line_data
                        parameter = s.rsplit("; ", 8)
                        for found in parameter:
                            liste += [found]
                        special += [liste]
                        del [liste]
        ini.close()
    except:
        print('Error in reading parameters from RiftRaidWarnings.ini')
except:
    print('Cannot find Parameter file RiftRaidWarnings.ini')
    time.sleep(20)
    sys.exit('RiftRaidWarnings.ini not found')

print('Make sure you use /combatlog and /log in Rift after each game restart !')
speak = win32com.client.Dispatch('Sapi.SpVoice')
speak.Volume = volume
timerreset = True
siri = True
location = "all"
boss = "all"
language = "all"
specialtrigger = 1
timeout_trigger = []
logfilecheck()
