# Rift Raid Alert
# Spoken raid warnings for the MMORPG Rift
# Version 0.1.5
# Author: Bamux@Typhiria

import os
import pythoncom
import sys
import time
import win32com.client
import winshell as winshell
from random import randint
from threading import Thread


def trigger_analysis(log):
    global timerreset, language, location, boss, specialtrigger, timeout_trigger, siri, stacks, stacks_trigger, depending, counter1, counter2
    trigger_found = False
    stacks_found = False
    first = False

    # Default Trigger
    for i in range(0, len(trigger)):
        if language == trigger[i][0] \
                or trigger[i][0] == "all" \
                or language == "all":
            if location == trigger[i][1] \
                    or trigger[i][1] == "all" \
                    or trigger[i][1] == "combat_end" \
                    or trigger[i][1] == "combat_begin" \
                    or location == "all":
                        if "$player" in trigger[i][4]:
                            cut_string = trigger[i][4].split('$player')
                            left_string = cut_string[0]
                            right_string = cut_string[1]
                            if len(left_string) > len(right_string):
                                new_string = left_string
                            else:
                                new_string = right_string
                            if new_string in log:
                                if not first:
                                    first = True
                                    print(log)
                                if int(trigger[i][10]) != 0:
                                    if int(trigger[i][10]) > 0:
                                        depending = int(trigger[i][10])
                                    if int(trigger[i][10]) < 0:
                                        if int(trigger[i][10]) + depending == 0:
                                            trigger_found = True
                                if not trigger_found:
                                    for z in range(0, len(timeout_trigger)):
                                        if trigger[i][4] == timeout_trigger[z]:
                                            trigger_found = True
                                            break
                                if not trigger_found:
                                    if "[Rift Raid Alert] " in log:
                                        cut_string = log.split("[Rift Raid Alert] ")
                                        log = cut_string[1]
                                    else:
                                        if ":" in log[0:5]:
                                            cut_string = log.split(": ", 1)
                                            log = cut_string[1]
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
                                    cut_string = new_string.split('@')
                                    player = cut_string[0]
                                    cut_string = player.split(' ')
                                    player = cut_string[0]
                                    if "$player" in trigger[i][5]:
                                        if '$' == trigger[i][5][0]:
                                            cut_string = trigger[i][5].split('$player ')
                                            new_string = cut_string[1]
                                            new_string = player + " " + new_string
                                        else:
                                            cut_string = trigger[i][5].split(' $player')
                                            new_string = cut_string[0]
                                            new_string = new_string + " " + player
                                    else:
                                        new_string = trigger[i][5]

                                    if int(trigger[i][9]) > 0:
                                        for z in range(0, len(stacks_trigger)):
                                            if player == stacks_trigger[z][0]:
                                                stacks_found = True
                                                trigger_found = True
                                                stacks_trigger[z][1] += 1
                                                print(stacks_trigger)
                                                if stacks_trigger[z][1] == int(trigger[i][9]):
                                                    if len(stacks_trigger) == 1:
                                                        trigger_found = False
                                                    else:
                                                        for x in range(0, len(stacks_trigger)):
                                                            if stacks_trigger[x][1] < int(trigger[i][9]):
                                                                trigger_found = False
                                        if not stacks_found:
                                            stacks_trigger += [[str(player), 1]]
                                            trigger_found = True
                                            print(stacks_trigger)

                                    if not trigger_found:
                                        if int(trigger[i][9]) < 0:
                                            if stacks_trigger:
                                                z = 0
                                                while z < len(stacks_trigger):
                                                    if player in stacks_trigger[z][0]:
                                                        del stacks_trigger[z]
                                                        print(stacks_trigger)
                                                        z += 1
                                                if stacks_trigger:
                                                    if stacks_trigger[0][1] >= abs(int(trigger[i][9])):
                                                        if int(trigger[i][6]) == 0:
                                                            Thread(target=saytext, args=(trigger[i][5],)).start()
                                        else:
                                            # print(stacks_trigger)
                                            if int(trigger[i][6]) == 0:
                                                Thread(target=saytext, args=(new_string,)).start()

                                        # timerreset = False
                                        siri = False
                                        if trigger[i][11] == "1":
                                            siri = True
                                            specialtrigger = 5
                                            timerreset.clear()
                                            stacks_trigger.clear()
                                        if int(trigger[i][6]) > 0:
                                            t = Thread(target=timer, args=(int(trigger[i][6]), trigger[i][4], trigger[i][5]))
                                            t.start()
                                        if int(trigger[i][7]) > 0:
                                            t = Thread(target=countdown, args=(int(trigger[i][7]), trigger[i][4]))
                                            t.start()
                                        if int(trigger[i][8]) > 0:
                                            t = Thread(target=timeout, args=(int(trigger[i][8]), trigger[i][4]))
                                            t.start()
                                        if trigger[i][0] != "all":
                                            language = trigger[i][0]
                                        if trigger[i][1] != "all":
                                            location = trigger[i][1]
                                        if trigger[i][2] != "all":
                                            if trigger[i][2] == "combat_end":
                                                timeout_trigger.clear()
                                                counter1 = 0
                                                counter2 = 0
                                                # print("Combat End")
                                                boss = "all"
                                            elif trigger[i][2] == "combat_begin":
                                                timeout_trigger.clear()
                                                counter1 = 0
                                                counter2 = 0
                                                # print("Combat Begin")
                                                boss = "all"
                                            else:
                                                boss = trigger[i][2]

                        else:
                            if trigger[i][4] in log:
                                if not first:
                                    first = True
                                    print(log)
                                text_to_speech = trigger[i][5]
                                if int(trigger[i][10]) != 0:
                                    if int(trigger[i][10]) > 0:
                                        depending = int(trigger[i][10])
                                        # print(trigger[i][4])
                                    if int(trigger[i][10]) < 0:
                                        if int(trigger[i][10]) + depending == 0:
                                            trigger_found = True
                                            counter2 += 1
                                            # Thread(target=saytext, args=("stop",)).start()
                                            if counter1 + counter2 == 3:
                                                counter1 = 0
                                                counter2 = 0
                                        else:
                                            print(trigger[i][3])
                                            if trigger[i][2] == "Lord Arak":
                                                counter1 += 1
                                                text_to_speech = trigger[i][5] + " " + str(counter1)
                                                if counter1 + counter2 == 3:
                                                    counter1 = 0
                                                    counter2 = 0
                                if not trigger_found:
                                    if int(trigger[i][9]) > 0:
                                        for z in range(0, len(stacks_trigger)):
                                            if trigger[i][4] == stacks_trigger[z][0]:
                                                stacks_found = True
                                                if stacks_trigger[z][1] < int(trigger[i][9]):
                                                    stacks_trigger[z][1] += 1
                                                    trigger_found = True
                                                else:
                                                    stacks_trigger[z][1] += 1
                                                    trigger_found = False
                                        if not stacks_found:
                                            stacks_trigger += [[trigger[i][4], 2]]
                                            trigger_found = True
                                        print(stacks_trigger)
                                    for z in range(0, len(timeout_trigger)):
                                        if trigger[i][4] == timeout_trigger[z]:
                                            trigger_found = True
                                            break
                                    if not trigger_found:
                                        # timerreset = False
                                        siri = False
                                        # print(log)
                                        if int(trigger[i][6]) == 0:
                                            Thread(target=saytext, args=(text_to_speech,)).start()
                                        if trigger[i][11] == "1":
                                            siri = True
                                            specialtrigger = 5
                                            timerreset.clear()
                                            stacks_trigger.clear()
                                        if int(trigger[i][6]) > 0:
                                            t = Thread(target=timer, args=(int(trigger[i][6]), trigger[i][4], trigger[i][5]))
                                            t.start()
                                        if int(trigger[i][7]) > 0:
                                            t = Thread(target=countdown, args=(int(trigger[i][7]), trigger[i][4]))
                                            t.start()
                                        if int(trigger[i][8]) > 0:
                                            t = Thread(target=timeout, args=(int(trigger[i][8]), trigger[i][4]))
                                            t.start()
                                        if trigger[i][0] != "all":
                                            language = trigger[i][0]
                                        if trigger[i][1] != "all":
                                            location = trigger[i][1]
                                        if trigger[i][2] != "all":
                                            if trigger[i][2] == "combat_end":
                                                timeout_trigger.clear()
                                                counter1 = 0
                                                counter2 = 0
                                                # print("Combat End")
                                                boss = "all"
                                            elif trigger[i][2] == "combat_begin":
                                                timeout_trigger.clear()
                                                counter1 = 0
                                                counter2 = 0
                                                # print("Combat Begin")
                                                boss = "all"
                                            else:
                                                boss = trigger[i][2]

    # Special Trigger
    for i in range(0, len(special)):
        if language == special[i][0] or language == "all":
            if location == special[i][1] or location == "all":
                if boss == special[i][2] or boss == "all":
                    strigger = special[i][4]
                    if " || " in strigger:
                        content = strigger.rsplit(" || ")
                        print(content)
                        for value in content:
                            if value in log:
                                strigger = value
                                break
                    if strigger in log:
                        print(log)
                        siri = False
                        Thread(target=saytext, args=(special[i][specialtrigger],)).start()
                        specialtrigger += 1
                        if specialtrigger == len(special[i]):
                            specialtrigger = 5
                        language = special[i][0]
                        location = special[i][1]
                        boss = special[i][2]
                        break


def umlaute(log):
    log = log.replace('Ã„', 'Ae')
    log = log.replace('Ã–', 'Oe')
    log = log.replace('Ãœ', 'Ue')
    log = log.replace('Ã¤', 'ae')
    log = log.replace('Ã¤', 'ae')
    log = log.replace('Ã¶', 'oe')
    log = log.replace('Ã¼', 'ue')
    log = log.replace('ÃŸ', 'ss')
    return log


def logfile_analysis(logtext):
    try:
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
        lasttime = -1
        combat = False

        while True:
            log = logtext.readline()
            log = log.rstrip()
            log = umlaute(log)
            if log:
                if playback:
                    if "Combat Begin" in log:
                        combat = True
                        # print("Combat Begin")
                    if combat:
                        cut_string = log.split(":")
                        logtime = int(cut_string[2])
                        if lasttime < 0:
                            lasttime = logtime
                        if logtime >= lasttime:
                            wait = logtime - lasttime
                        else:
                            wait = logtime + 60 - lasttime
                        if wait > 0:
                            # print(str(logtime) + ", " + str(lasttime) + ", " + str(wait))
                            time.sleep(wait)
                        lasttime = logtime
                    if "Combat End" in log:
                        combat = False
                        lasttime = -1

                trigger_analysis(log)
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
                        text = '''Hi, I am Siri. I support you with Raid announcements. If you don't  like my voice, please disable me.'''
                if text:
                    Thread(target=saytext, args=(text,)).start()
                    text = ""
            else:
                time.sleep(0.50)  # waiting for a new line
    except:
        print('An error has occurred in the Log.txt !')
        time.sleep(0.10)
        t = Thread(target=logfile_analysis, args=(logtext,))
        t.start()


def logfilecheck():
    global logfile
    logtext = ""

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
    if log_exists:
        if playback:
            logtext.seek(0, 1)  # reading from line 1
        else:
            logtext.seek(0, 2)  # jump to the end of the Log.txt
        t = Thread(target=logfile_analysis, args=(logtext,))
        t.start()
    else:
        print('use /log in Rift and edit the path to your Logfile in the Rift_Raid_Warnings.ini !')
        time.sleep(20)
        logfilecheck()


def timeout(timeout_time, trigger_content):
    global timeout_trigger
    timeout_trigger += [trigger_content]
    for i in range(0, timeout_time):
        if len(timeout_trigger) > 0:
            time.sleep(1)
        else:
            return
    z = 0
    while z < len(timeout_trigger):
        if trigger_content == timeout_trigger[z]:
            del timeout_trigger[z]
            break
        z += 1
    # print(timeout_trigger)


def timer(seconds, timer_name, text):
    global timerreset
    print('Start timer with ' + str(seconds) + ' seconds.')
    timerreset += [timer_name]
    for i in range(0, seconds):
        z = 0
        timer_found = False
        while z < len(timerreset):
            if timer_name == timerreset[z]:
                timer_found = True
                break
            z += 1
        if timer_found is True and len(timerreset) > 0:
            time.sleep(1)
        else:
            print('Stop timer.')
            return
    Thread(target=saytext, args=(text,)).start()
    i = 0
    while i < len(timerreset):
        if timer_name == timerreset[i]:
            del timerreset[i]
            break
        i += 1
    print(timerreset)


def countdown(count, countdown_name):
    global timerreset
    print('Start countdown with ' + str(count) + ' seconds.')
    timerreset += [countdown_name]
    print(timerreset)
    for i in range(0, count):
        z = 0
        countdown_found = False
        while z < len(timerreset):
            if countdown_name == timerreset[z]:
                countdown_found = True
                break
            z += 1
        if countdown_found is True and len(timerreset) > 0:
            if count - i < 4:
                Thread(target=saytext, args=(count - i,)).start()
            time.sleep(1)
        else:
            print('Stop countdown.')
            return
    i = 0
    while i < len(timerreset):
        if countdown_name == timerreset[i]:
            del timerreset[i]
            break
        i += 1
    print(timerreset)


def saytext(text):
    if text:
        try:
            pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
        except:
            pass
        # text = str(text.replace("Ã¼", "ü"))
        print("Siri: " + str(text))
        speak.Speak(text)


print("Raid Rift Alert Version 0.1.5")
print('Make sure you use /log in Rift after each game restart !')
volume = 100
# get parametrs from Rift_Raid_Warnings.ini
try:
    ini = open('RiftRaidAlert.ini', 'r')
    print('RiftRaidAlert.ini found')
    try:
        trigger = []
        special = []
        stacks = []
        for para_line in ini:
            paraline = str.rstrip(para_line)
            type_end = paraline.find('= ') + 2
            liste = []

            if 0 < type_end < len(paraline):
                line_type = str.lower(paraline[0:type_end])
                line_data = str.rstrip(paraline[type_end:])
                line_data = umlaute(line_data)
                # line_data_lower = str.lower(paraline[type_end:])
                if '#' not in line_type:
                    if 'logfile' in line_type:
                        logfile = line_data
                    if 'combatfile' in line_type:
                        combatlogfile = line_data
                    if 'volume' in line_type:
                        volume = int(line_data)
                        if volume < 0 or volume > 100:
                            volume = 100
                    if 'trigger' in line_type:
                        s = line_data
                        zaehler = 0
                        for char in s:
                            if char == ';':
                                zaehler += 1
                        if zaehler == 11:
                            parameter = s.rsplit("; ", 11)
                            for found in parameter:
                                liste += [found]
                            trigger += [liste]
                            del [liste]
                        else:
                            print("Incorrect syntax: " + s)
                    if 'special' in line_type:
                        liste = []
                        s = line_data
                        parameter = s.rsplit("; ")
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


speak = win32com.client.Dispatch('Sapi.SpVoice')
speak.Volume = volume
timerreset = []
siri = True
location = "all"
boss = "all"
language = "all"
specialtrigger = 5
timeout_trigger = []
stacks_trigger = []
depending = 0
counter1 = 0
counter2 = 0
playback = False  # only for Playback a logfile from line 1
logfilecheck()