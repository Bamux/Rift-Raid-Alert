# -*- coding: utf-8 -*-

# Rift Raid Alert
# Spoken raid warnings for the MMORPG Rift
# Version 0.5.2
# Author: Bamux@Typhiria

import os
# import sys
import time
import win32com.client
import pythoncom
import winsound
import codecs
from random import randint
from threading import Thread
from tkinter import *


def trigger_analysis(log):
    global timerreset, language, location, boss, specialtrigger, timeout_trigger, siri, stacks, stacks_trigger,\
        depending, counter1, counter2, output
    trigger_found = False
    stacks_found = False
    first = False
    # Default Trigger
    for i in range(0, len(trigger)):
        # if language == trigger[i][0] \
        #         or trigger[i][0] == "all" \
        #         or language == "all":
        #     if location == trigger[i][1] \
        #             or trigger[i][1] == "all" \
        #             or trigger[i][1] == "combat_end" \
        #             or trigger[i][1] == "combat_begin" \
        #             or location == "all":
                        if "player" in trigger[i][4]:
                            cut_string = trigger[i][4].split('player')
                            left_string = cut_string[0]
                            right_string = cut_string[1]
                            if len(left_string) > len(right_string):
                                new_string = left_string
                            else:
                                new_string = right_string
                            if new_string in log:
                                if not first:
                                    first = True
                                    # guioutput(log) 123
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
                                    if "player" in trigger[i][5]:
                                        if 'p' == trigger[i][5][0]:
                                            if output == "tts":
                                                cut_string = trigger[i][5].split('player ')
                                                new_string = cut_string[1]
                                                new_string = player + " " + new_string
                                            else:
                                                if playername == player:
                                                    cut_string = trigger[i][5].split('player ')
                                                    new_string = cut_string[1]
                                                else:
                                                    if output == "mix":
                                                        cut_string = trigger[i][5].split('player ')
                                                        new_string = cut_string[1]
                                                        new_string = player + " " + new_string
                                        else:
                                            if output == "tts":
                                                cut_string = trigger[i][5].split(' player')
                                                new_string = cut_string[0]
                                                new_string = new_string + " " + player
                                            else:
                                                if playername == player:
                                                    cut_string = trigger[i][5].split(' player')
                                                    new_string = cut_string[0]
                                                else:
                                                    if output == "mix":
                                                        cut_string = trigger[i][5].split(' player')
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
                                                guioutput(str(stacks_trigger))
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
                                            guioutput(str(stacks_trigger))

                                    if not trigger_found:
                                        if int(trigger[i][9]) < 0:
                                            if stacks_trigger:
                                                z = 0
                                                while z < len(stacks_trigger):
                                                    if player in stacks_trigger[z][0]:
                                                        del stacks_trigger[z]
                                                        guioutput(str(stacks_trigger))
                                                    z += 1
                                                if stacks_trigger:
                                                    if stacks_trigger[0][1] >= abs(int(trigger[i][9])):
                                                        if int(trigger[i][6]) == 0:
                                                            Thread(target=saytext, args=(trigger[i][5],)).start()
                                        else:
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
                                                timerreset.clear()
                                                stacks.clear()
                                                stacks_trigger.clear()
                                                counter1 = 0
                                                counter2 = 0
                                                # guioutput("Combat End")
                                                boss = "all"
                                            elif trigger[i][2] == "combat_begin":
                                                timeout_trigger.clear()
                                                counter1 = 0
                                                counter2 = 0
                                                # guioutput("Combat Begin")
                                                boss = "all"
                                            else:
                                                boss = trigger[i][2]

                        else:
                            if trigger[i][4] in log:
                                if not first:
                                    first = True
                                    # guioutput(log) 123
                                text_to_speech = trigger[i][5]
                                if int(trigger[i][10]) != 0:
                                    if int(trigger[i][10]) > 0:
                                        depending = int(trigger[i][10])
                                        # guioutput(trigger[i][4])
                                    if int(trigger[i][10]) < 0:
                                        if int(trigger[i][10]) + depending == 0:
                                            trigger_found = True
                                            counter2 += 1
                                            # Thread(target=saytext, args=("stop",)).start()
                                            if counter1 + counter2 == 3:
                                                counter1 = 0
                                                counter2 = 0
                                        else:
                                            guioutput(trigger[i][3])
                                            if trigger[i][2] == "lord arak":
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
                                        guioutput(str(stacks_trigger))
                                    for z in range(0, len(timeout_trigger)):
                                        if trigger[i][4] == timeout_trigger[z]:
                                            trigger_found = True
                                            break
                                    if not trigger_found:
                                        # timerreset = False
                                        siri = False
                                        # guioutput(log)
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
                                                timerreset.clear()
                                                stacks.clear()
                                                stacks_trigger.clear()
                                                counter1 = 0
                                                counter2 = 0
                                                # guioutput("Combat End")
                                                boss = "all"
                                            elif trigger[i][2] == "combat_begin":
                                                timeout_trigger.clear()
                                                counter1 = 0
                                                counter2 = 0
                                                # guioutput("Combat Begin")
                                                boss = "all"
                                            else:
                                                boss = trigger[i][2]

    # Special Trigger

    for i in range(0, len(special)):
        # if language == special[i][0] or language == "all":
        #     if location == special[i][1] or special[i][1] == "all" or location == "all":
        #         if boss == special[i][2] or special[i][2] == "all" or boss == "all":
                    strigger = special[i][4]
                    secialtrigger_found = ""
                    if " || " in strigger:
                        content = strigger.rsplit(" || ")
                        for value in content:
                            if value in log:
                                secialtrigger_found = True
                                break
                    if " + " in strigger:
                        content = strigger.rsplit(" + ")
                        for value in content:
                            if value in log:
                                secialtrigger_found = True
                            else:
                                secialtrigger_found = False
                                break
                    if secialtrigger_found:
                        # guioutput(log) 123
                        siri = False
                        Thread(target=saytext, args=(special[i][specialtrigger],)).start()
                        # Thread(target=saytext, args=(text,)).start()
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
    log = log.replace('Ã¶', 'oe')
    log = log.replace('Ã¼', 'ue')
    log = log.replace('ÃŸ', 'ss')
    return log


def logfile_analysis(logtext):
    try:
        global trigger, special, language, location, playername, boss, timerreset, output, zone
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
        zone = ""
        text = ""
        bossname = ""
        lasttime = -1
        combat = False
        zone_in_zonelist = False

        while True:
            line = ""
            log = logtext.readline()
            log = log.rstrip()
            if "[Rift Raid Alert] " in log:
                cut_string = log.split("[Rift Raid Alert] ")
                log = cut_string[0] + cut_string[1]
                line = cut_string[1]
                guioutput(log)
            # log = umlaute(log)
            log = str.lower(log)

            if 'Rift Raid Alert Trigger >' in line:
                if combattrigger == 1:
                    cut_string = line.split('Rift Raid Alert Trigger > ')
                    new_string = cut_string[1]
                    if zone != new_string:
                        trigger.clear()
                        special.clear()
                        language = "all"
                        location = "all"
                        boss = "all"
                        zone = new_string
                        triggerload(new_string)
                        trigger += defaulttrigger + bufftrigger
                        special += defaultspecial
            elif "Combat Begin > " in line:
                combat = True
                bossname = line.split(" > ")
                bossname = bossname[1]
                for item in zonelist:
                    if item == zone:
                        zone_in_zonelist = True
                        break
                if zone_in_zonelist:
                    Thread(target=load_abilies, args=(bossname,)).start()
            elif "Combat End" in line:
                lasttime = -1
                combat = False
                if zone_in_zonelist:
                    save_abilities(bossname)
                zone_in_zonelist = False

            if log:
                if playback:
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
                            # guioutput(str(logtime) + ", " + str(lasttime) + ", " + str(wait))
                            time.sleep(wait)
                        lasttime = logtime

                if 'tank pull >' in log or 'fail pull >' in log:
                    i = 0
                    while i < len(timerreset):
                        if timerreset[i] == "siri start countdown":
                            del timerreset[i]
                            break
                        i += 1
                    guioutput(str(timerreset))
                elif 'rift raid alert trigger < keywords off' in log:
                    zone = ""
                    # guioutput(log) 123
                elif 'rift raid alert trigger > keywords on' in log:
                    trigger.clear()
                    special.clear()
                    triggerload("keywords")
                    trigger += defaulttrigger + bufftrigger
                    special += defaultspecial
                    # guioutput(log) 123
                    zone = ""
                elif 'player >> ' in log:
                    cut_string = log.split('player >> ')
                    playername = cut_string[1]
                    guioutput("Player:" + playername)
                elif output == "wav":
                    if 'raidbuff missing > ' + playername in log:
                        text = "raidbuffs.wav"

                trigger_analysis(log)

                if combat and line and zone_in_zonelist:
                    Thread(target=abilitycheck, args=(line, bossname)).start()

                # Siri
                if siri:
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
                        if output == "tts":
                            text = '''Hi, I am Siri. I support you with Raid announcements.'''
                        else:
                            text = "siri.wav"

                if text:
                    Thread(target=saytext, args=(text,)).start()
                    text = ""
            else:
                time.sleep(0.50)  # waiting for a new line
    except:
        guioutput('An error has occurred in the Log.txt !')
        time.sleep(0.10)
        t = Thread(target=logfile_analysis, args=(logtext,))
        t.start()


def save_abilities(bossname):
    if len(abilities_new) != len(abilities_old):
        mypath = "trigger/abilities/" + zone
        if not os.path.isdir(mypath):
            os.makedirs(mypath)
        f = codecs.open(mypath + "/" + bossname + ".txt", "w", "utf-8")
        for item in abilities_new:
            f.write(str(item) + '\r\n')
        f.close()
        abilities_old.clear()
        abilities_new.clear()


def load_abilies(bossname):
    global abilities_old, abilities_new
    if zone:
        try:
            abilities_old.clear()
            abilities_new.clear()
            mypath = "trigger/abilities/" + zone + "/" + bossname + ".txt"
            abilities_txt = codecs.open(mypath, 'r', "utf-8")
            for item in abilities_txt:
                item = item.rstrip()
                abilities_old += [item]
                abilities_new += [item]
            abilities_txt.close()
        except:
            pass


def abilitycheck(line, bossname):
    global abilities_new
    # print(abilities_new)
    ability_existing = False
    if "pull >> " not in line and "Combat Begin" not in line and "Rift Raid Alert" not in line and "%" not in line \
            and "remove" not in line:
        if " >> " in line:
            line = line.split(" >> ")
            line = line[0]  # + " >> player"
        elif " << " in line:
            line = line.split(" << ")
            line = "player << " + line[1]
        for item in abilities_new:
            if line == item:
                ability_existing = True
        if not ability_existing:
            abilities_new += [line]


def logfilecheck():
    global logfile
    logtext = ""

    try:
        logtext = codecs.open(logfile, 'r', "utf-8")
        guioutput('Log.txt found')
        log_exists = True
    except:
        guioutput('Log.txt not found, checking common locations')
        try:
            logfile = os.path.expanduser('~\Documents\RIFT\Log.txt')
            logtext = codecs.open(logfile, 'r', "utf-8")
            guioutput('Log.txt found')
            log_exists = True
        except:
            try:
                logfile = 'C:\Program Files (x86)\RIFT Game\Log.txt'
                logtext = codecs.open(logfile, 'r', "utf-8")
                guioutput('Log.txt found')
                log_exists = True
            except:
                try:
                    logfile = 'C:\Programs\RIFT~1\Log.txt'
                    logtext = codecs.open(logfile, 'r', "utf-8")
                    guioutput('Log.txt found')
                    log_exists = True
                except:
                    guioutput('Error! could not find the Log File')
                    speak.Speak('Logfile not found!')
                    log_exists = False
    if log_exists:
        if playback:
            logtext.seek(0, 1)  # reading from line 1
        else:
            if error_analysis:
                logtext.seek(0, 1)  # reading from line 1
            else:
                logtext.seek(0, 2)  # jump to the end of the Log.txt
        t = Thread(target=logfile_analysis, args=(logtext,))
        t.start()
    else:
        guioutput('use /log in Rift and edit the path to your Logfile in the RiftRaidAlert.ini !')
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
    # guioutput(timeout_trigger)


def timer(seconds, timer_name, text):
    global timerreset
    guioutput('Start timer with ' + str(seconds) + ' seconds.')
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
            guioutput('Stop timer.')
            return
    Thread(target=saytext, args=(text,)).start()
    i = 0
    while i < len(timerreset):
        if timer_name == timerreset[i]:
            del timerreset[i]
            break
        i += 1
    # guioutput(str(timerreset))


def countdown(count, countdown_name):
    global timerreset
    guioutput('Start countdown with ' + str(count) + ' seconds.')
    timerreset += [countdown_name]
    # guioutput(str(timerreset))
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
                Thread(target=saytext, args=(str(count - i),)).start()
            time.sleep(1)
        else:
            guioutput('Stop countdown.')
            return
    i = 0
    while i < len(timerreset):
        if countdown_name == timerreset[i]:
            del timerreset[i]
            break
        i += 1
    # guioutput(str(timerreset))


def saytext(text):
    global output
    if text:
        guioutput("Siri: " + str(text))
        if ".wav" in text:
            winsound.PlaySound('siri/' + text, winsound.SND_FILENAME)
        else:
            if output == "tts":
                texttospeech(text)
            else:
                playsoundfile(text)


def texttospeech(text):
    global output, volume
    try:
        if volume != volume_bar.get():
            volume = volume_bar.get()
            speak.Volume = volume
        pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
        if not error_analysis:
            speak.Speak(text)
    except:
        output = "wav"
        playsoundfile(text)


def playsoundfile(text):
    global soundfiles, output
    soundfile_found = False
    if output == "wav" or output == "mix":
        if "free" in text:
            text = "free"
        elif "intercept" in text:
            text = "intercept"
        for i in range(0, len(soundfiles)):
            if text == soundfiles[i]:
                if text == "kick" or text == "now":
                    winsound.PlaySound('siri/' + text + ".wav", winsound.SND_NOWAIT)
                else:
                    winsound.PlaySound('siri/' + text + ".wav", winsound.SND_FILENAME)
                soundfile_found = True
                break
    if output == "mix":
        if not soundfile_found:
            texttospeech(text)


def triggerload(file):  # get parametrs from Rift_Raid_Warnings.ini
    global trigger, logfile, volume, special, keywords, buffcheck, output

    try:
        if file == "RiftRaidAlert.ini":
            ini = codecs.open(file, 'r', "utf-8")
            guioutput(file + ' found')
        else:
            ini = codecs.open("trigger/" + file + ".txt", 'r', "utf-8")
            guioutput(file + ' trigger loaded')
        try:
            trigger = []
            special = []
            # stacks = []
            for para_line in ini:
                paraline = str.rstrip(para_line)
                type_end = paraline.find('= ') + 2
                liste = []

                if 0 < type_end < len(paraline):
                    line_type = str.lower(paraline[0:type_end])
                    line_data = str.rstrip(paraline[type_end:])
                    # line_data = umlaute(line_data)
                    line_data = str.lower(line_data)
                    # line_data_lower = str.lower(paraline[type_end:])
                    if '#' not in line_type:
                        if file == "RiftRaidAlert.ini":
                            if 'logfile' in line_type:
                                logfile = line_data
                            if 'volume' in line_type:
                                volume = int(line_data)
                                if volume < 0 or volume > 100:
                                    volume = 100
                            if 'buffcheck' in line_type:
                                buffcheck = int(line_data)
                                if buffcheck < 0 or buffcheck > 1:
                                    buffcheck = 1
                            if 'output' in line_type:
                                output = line_data
                                if output == "wav" or output == "tts" or output == "mix" or output == "off":
                                    pass
                                else:
                                    output = "wav"
                        else:
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
                                    guioutput("Incorrect syntax: " + s)
                            if 'special' in line_type:
                                liste = []
                                s = line_data
                                parameter = s.rsplit("; ")
                                for found in parameter:
                                    liste += [found]
                                special += [liste]
                                del [liste]
                            if 'keywords' in line_type:
                                liste = ["all"] + ["all"] + ["all"] + ["all"]
                                s = line_data
                                parameter = s.rsplit("; ")
                                for found in parameter:
                                    liste += [found]
                                special += [liste]
                                del [liste]
            ini.close()

        except:
            guioutput('Error in reading parameters from ' + file)
    except:
            guioutput('No Triggers found for ' + file)


def soundfiles_list(folder):
    try:
        soundfileslist = os.listdir(folder)
        for i in range(0, len(soundfileslist)):
            soundfileslist[i] = soundfileslist[i].split(".")[0]
        return soundfileslist
    except:
        guioutput("Folder siri is missing")


def guioutput(text):
    T.insert(END, "\n" + text)
    T.yview(END)


def ask_quit():
    file_out = codecs.open("RiftRaidAlert.ini", "w", 'utf-8')
    file_out.write("logfile = " + logfile + '\r\n')
    file_out.write("volume = " + str(volume_bar.get()) + '\r\n')
    file_out.write("buffcheck = " + str(buffcheck) + '\r\n')
    file_out.write("output = " + output + '\r\n')
    file_out.close()
    root.destroy()
    os._exit(1)


def wav():
    global output
    if var_wav.get() == 1:
        if output == "tts":
            output = "mix"
        elif output == "off":
            output = "wav"
        guioutput("Sound: " + output)
    elif var_wav.get() == 0:
        if output == "mix":
            output = "tts"
        elif output == "wav":
            output = "off"
        guioutput("Sound: " + output)


def tts():
    global output
    if var_tts.get() == 1:
        if output == "wav":
            output = "mix"
        elif output == "off":
            output = "tts"
        guioutput("Sound: " + output)
    elif var_tts.get() == 0:
        if output == "mix":
            output = "wav"
        elif output == "tts":
            output = "off"
        guioutput("Sound: " + output)


def buff_check():
    global buffcheck, trigger, bufftrigger, special
    if var_buffcheck.get() == 1:
        guioutput("Buffcheck: on")
        if buffcheck == 0:
            buffcheck = 1
            trigger.clear()
            special.clear()
            if zone:
                triggerload(zone)
            trigger += defaulttrigger + bufftrigger
            special += defaultspecial
    elif var_buffcheck.get() == 0:
        guioutput("Buffcheck: off")
        if buffcheck == 1:
            buffcheck = 0
            trigger.clear()
            special.clear()
            if zone:
                triggerload(zone)
            trigger += defaulttrigger
            special += defaultspecial


def trigger_select(evt):
    try:
        value = str((trigger_listbox.get(trigger_listbox.curselection())))
        trigger_choice(value)
    except:
        pass


def boss_select(evt):
    try:
        final_trigger.clear()
        b3.grid_forget()
        b4.grid_forget()
        value = str((boss_listbox.get(boss_listbox.curselection())))
        e1.delete(0, END)
        e1.insert(0, value)
        trigger_ui(value)
    except:
        pass


def zone_select(evt):
    final_trigger.clear()
    e1.delete(0, END)
    e1.insert(0, "")
    b3.grid_forget()
    b4.grid_forget()
    value = str((zone_listbox.get(zone_listbox.curselection())))
    e0.delete(0, END)
    e0.insert(0, value)
    zone_listbox_value = value
    boss_ui(value)


def save_newtrigger(value):
    global trigger, special
    found = False
    newtrigger = ""
    if value == "special_new" and e0.get() and e1.get() and len(e_special1.get()) > 4 and e_special6.get():
        found = True
        special_keywords = e_special1.get()
        if e_special2.get():
            special_keywords += " || " + e_special2.get()
        if e_special3.get():
            special_keywords += " || " + e_special3.get()
        if e_special4.get():
            special_keywords += " || " + e_special4.get()
        if e_special5.get():
            special_keywords += " || " + e_special5.get()
        special_tts = "; " + e_special6.get()
        if e_special7.get():
            special_tts += "; " + e_special7.get()
        if e_special8.get():
            special_tts += "; " + e_special8.get()
        if e_special9.get():
            special_tts += "; " + e_special9.get()
        if e_special10.get():
            special_tts += "; " + e_special10.get()
        if e_special11.get():
            special_tts += "; " + e_special11.get()
        if e_special12.get():
            special_tts += "; " + e_special12.get()
        if e_special13.get():
            special_tts += "; " + e_special13.get()
        newtrigger = "special = all; " + e0.get() + "; " + e1.get() + "; ability; " + special_keywords + special_tts
    else:
        if e0.get() and e1.get() and len(e2.get()) >= 5 and e4.get().isdigit() and e5.get().isdigit() \
                and e6.get().isdigit() and e8.get().isdigit():
            found = True
            newtrigger = "trigger = all; " + e0.get() + "; " + e1.get() + "; ability; " + e2.get() + "; " + e3.get() + "; " \
                         + e4.get() + "; " + e5.get() + "; " + e6.get() + "; " + e7.get() + "; " + e8.get() + "; " \
                         + var_reset.get()

    if found:
        f = codecs.open("trigger/" + e0.get() + ".txt", "a", "utf-8")
        f.write(newtrigger + '\r\n')
        f.close()
        b3.grid_forget()
        b4.grid_forget()
        boss_ui(e0.get())
        trigger_ui(e1.get())
        zone_list()
        if zone == str.lower(e0.get()):
            trigger.clear()
            special.clear()
            triggerload(zone)
            trigger += defaulttrigger + bufftrigger
            special += defaultspecial
    else:
        if value == "special_new":
            l18.grid(row=18, column=1, padx=190, sticky=W)
        else:
            l18.grid(row=11, column=1, padx=190, sticky=W)


def edit_trigger(value):
    global trigger, special
    final_trigger_tts = ""
    old_trigger = ""
    newtrigger = ""
    found = False
    liste = []
    if value == "delete":
        found = True
        if ' || ' in final_trigger[4]:
            value = "special_delete"
    if value == "special_edit" or value == "special_delete":
        i = 0
        for item in final_trigger:
            if i > 4:
                final_trigger_tts += "; " + item
            i += 1
        old_trigger = "special = " + final_trigger[0] + "; " + final_trigger[1] + "; " + final_trigger[2] + "; " \
                      + final_trigger[3] + "; " + final_trigger[4] + final_trigger_tts
        if value == "special_edit":
            if e0.get() and e1.get() and len(e_special1.get()) > 4:
                found = True
                special_keywords = e_special1.get()
                if e_special2.get():
                    special_keywords += " || " + e_special2.get()
                if e_special3.get():
                    special_keywords += " || " + e_special3.get()
                if e_special4.get():
                    special_keywords += " || " + e_special4.get()
                if e_special5.get():
                    special_keywords += " || " + e_special5.get()
                special_tts = "; " + e_special6.get()
                if e_special7.get():
                    special_tts += "; " + e_special7.get()
                if e_special8.get():
                    special_tts += "; " + e_special8.get()
                if e_special9.get():
                    special_tts += "; " + e_special9.get()
                if e_special10.get():
                    special_tts += "; " + e_special10.get()
                if e_special11.get():
                    special_tts += "; " + e_special11.get()
                if e_special12.get():
                    special_tts += "; " + e_special12.get()
                if e_special13.get():
                    special_tts += "; " + e_special13.get()
                newtrigger = "special = all; " + "all; " + e1.get() + "; ability; " + special_keywords + special_tts

    if value == "edit" or value == "delete":
        old_trigger = "trigger = " + final_trigger[0] + "; " + final_trigger[1] + "; " + final_trigger[2] + "; " \
                      + final_trigger[3] + "; " + final_trigger[4] + "; " + final_trigger[5] + "; " + final_trigger[6] \
                      + "; " + final_trigger[7] + "; " + final_trigger[8] + "; " + final_trigger[9] + "; " \
                      + final_trigger[10] + "; " + final_trigger[11]
        if value == "edit":
            if e0.get() and e1.get() and len(e2.get()) >= 5 and e4.get().isdigit() and e5.get().isdigit() and e6.get().isdigit()\
                    and e8.get().isdigit():
                found = True
                newtrigger = "trigger = all; " + "all; " + e1.get() + "; ability; " + e2.get() + "; " + e3.get() + "; " \
                             + e4.get() + "; " + e5.get() + "; " + e6.get() + "; " + e7.get() + "; " + e8.get() + "; " + var_reset.get()

    if found or value == "delete" or value == "special_delete":
        file = codecs.open("trigger/" + e0.get() + ".txt", "r", 'utf-8')
        for item in file:
            if old_trigger in item:
                if value == "edit" or value == "special_edit":
                    item = newtrigger + '\r\n'
                    liste += [item]
            else:
                liste += [item]
        file.close()
        file_out = codecs.open("trigger/" + e0.get() + ".txt", "w", 'utf-8')
        for item in liste:
            file_out.write(item)
        file_out.close()
        boss_ui(e0.get())
        trigger_ui(e1.get())
        zone_list()
        if zone == str.lower(e0.get()):
            trigger.clear()
            special.clear()
            triggerload(zone)
            trigger += defaulttrigger + bufftrigger
            special += defaultspecial
    else:
        if value == "special_edit":
            l18.grid(row=18, column=1, padx=190, sticky=W)
        else:
            l18.grid(row=11, column=1, padx=190, sticky=W)


def sound_file_select(evt):
    value = str((sound_listbox.get(sound_listbox.curselection())))
    if value != ".. exit":
        e3.delete(0, END)
        e3.insert(0, value)
        Thread(target=saytext, args=(value + ".wav",)).start()
    sound_listbox.grid_forget()
    scrollbar.grid_forget()
    b7.grid(row=4, column=1, padx=330, sticky=W)
    b9.grid(row=3, column=1, padx=330, sticky=W)
    l13.grid(row=5, column=1, padx=90, sticky=W)
    l14.grid(row=6, column=1, padx=90, sticky=W)
    l15.grid(row=7, column=1, padx=90, sticky=W)
    l16.grid(row=8, column=1, padx=90, sticky=W)
    l17.grid(row=9, column=1, padx=90, sticky=W)


def sound_file():
    b7.grid_forget()
    b9.grid_forget()
    l13.grid_forget()
    l14.grid_forget()
    l15.grid_forget()
    l16.grid_forget()
    l17.grid_forget()
    liste = soundfiles_list('siri')
    sound_listbox.delete(0, END)
    sound_listbox.insert(END, ".. exit")
    for item in liste:
        sound_listbox.insert(END, item)
    sound_listbox.grid(row=0, column=2, pady=10, rowspan=12, sticky=N+S+E+W)
    scrollbar.grid(row=0, column=3, pady=10, rowspan=12, sticky=N+S+E+W)
    sound_listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=sound_listbox.yview)


def ability_select(evt):
    value = str((abilities_listbox.get(abilities_listbox.curselection())))
    if value != ".. exit":
        e2.delete(0, END)
        e2.insert(0, value)
    abilities_listbox.grid_forget()
    scrollbar.grid_forget()
    b7.grid(row=4, column=1, padx=330, sticky=W)
    b9.grid(row=3, column=1, padx=330, sticky=W)
    l13.grid(row=5, column=1, padx=90, sticky=W)
    l14.grid(row=6, column=1, padx=90, sticky=W)
    l15.grid(row=7, column=1, padx=90, sticky=W)
    l16.grid(row=8, column=1, padx=90, sticky=W)
    l17.grid(row=9, column=1, padx=90, sticky=W)


def abilities():
    b7.grid_forget()
    b9.grid_forget()
    l13.grid_forget()
    l14.grid_forget()
    l15.grid_forget()
    l16.grid_forget()
    l17.grid_forget()
    abilities_listbox.delete(0, END)
    abilities_listbox.insert(END, ".. exit")
    abilities_listbox.grid(row=0, column=2, pady=10, rowspan=12, sticky=N + S + E + W)
    scrollbar.grid(row=0, column=3, pady=10, rowspan=12, sticky=N + S + E + W)
    abilities_listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=abilities_listbox.yview)
    try:
        file = codecs.open("trigger/abilities/" + e0.get() + "/" + e1.get() + ".txt", "r", 'utf-8')
        for item in file:
            item = item.rstrip()
            abilities_listbox.insert(END, item)

    except:
        pass


def special_trigger(value):
    b2.grid_forget()
    b8.grid_forget()
    b_special_trigger.grid_forget()
    zone_listbox.grid_forget()
    boss_listbox.grid_forget()
    trigger_listbox.grid_forget()
    b3.grid_forget()
    b4.grid_forget()
    root.rowconfigure(0, weight=0)
    root.columnconfigure(0, weight=0)
    root.rowconfigure(1, weight=0)
    root.columnconfigure(1, weight=0)
    l_special0.grid(row=0, column=0, padx=30, sticky=W)
    l_special1.grid(row=0, column=1, sticky=W)
    l2.grid(row=1, padx=30, sticky=W)
    l3.grid(row=2, padx=30, sticky=W)
    e0.grid(row=1, column=1, sticky=W)
    e1.grid(row=2, column=1, sticky=W)
    l_special2.grid(row=3, column=0, padx=30, sticky=W)
    e_special1.grid(row=4, column=1, sticky=W)
    e_special2.grid(row=5, column=1, sticky=W)
    e_special3.grid(row=6, column=1, sticky=W)
    e_special4.grid(row=7, column=1, sticky=W)
    e_special5.grid(row=8, column=1, sticky=W)
    l5.grid(row=9, column=0, padx=30, sticky=W)
    e_special6.grid(row=10, column=1, sticky=W)
    e_special7.grid(row=11, column=1, sticky=W)
    e_special8.grid(row=12, column=1, sticky=W)
    e_special9.grid(row=13, column=1, sticky=W)
    e_special10.grid(row=14, column=1, sticky=W)
    e_special11.grid(row=15, column=1, sticky=W)
    e_special12.grid(row=16, column=1, sticky=W)
    e_special13.grid(row=17, column=1, sticky=W)
    if value == "new":
        b_special_trigger1.grid(row=18, column=1, pady=10, sticky=W)
    else:
        b_special_trigger2.grid(row=18, column=1, pady=10, sticky=W)
        split = final_trigger[4].split("||")
        i = 1
        for item in split:
            item = item.lstrip()
            item = item.rstrip()
            if i == 1:
                e_special1.delete(0, END)
                e_special1.insert(0, item)
            elif i == 2:
                e_special2.delete(0, END)
                e_special2.insert(0, item)
            elif i == 3:
                e_special3.delete(0, END)
                e_special3.insert(0, item)
            elif i == 4:
                e_special4.delete(0, END)
                e_special4.insert(0, item)
            elif i == 5:
                e_special5.delete(0, END)
                e_special5.insert(0, item)
            i += 1
        try:
            e_special6.delete(0, END)
            e_special6.insert(0, final_trigger[5])
            e_special7.delete(0, END)
            e_special7.insert(0, final_trigger[6])
            e_special8.delete(0, END)
            e_special8.insert(0, final_trigger[7])
            e_special9.delete(0, END)
            e_special9.insert(0, final_trigger[8])
            e_special10.delete(0, END)
            e_special10.insert(0, final_trigger[9])
            e_special11.delete(0, END)
            e_special11.insert(0, final_trigger[10])
            e_special12.delete(0, END)
            e_special12.insert(0, final_trigger[11])
            e_special13.delete(0, END)
            e_special13.insert(0, final_trigger[12])
        except:
            pass


def test_trigger():
    global trigger, special, zone, language, location, boss
    if zone != e0.get():
        trigger_analysis("combat end")
    zone = e0.get()
    boss = e1.get()
    trigger.clear()
    special.clear()
    language = "all"
    location = "all"
    boss = "all"
    triggerload(e0.get())
    trigger += defaulttrigger + bufftrigger
    special += defaultspecial
    if len(final_trigger) > 3 and " || " in final_trigger[4]:
        split = final_trigger[4].split(" || ")[0]
        trigger_analysis(str.lower(split))
    else:
        trigger_analysis(str.lower(final_trigger[4]))


def new_trigger(value):
    # print(final_trigger)
    if len(final_trigger) > 3 and " || " in final_trigger[4]:
        if value == "new":
            special_trigger("new")
        else:
            special_trigger("edit")
    else:
        forget()
        root.rowconfigure(0, weight=0)
        root.columnconfigure(0, weight=0)
        root.rowconfigure(1, weight=0)
        root.columnconfigure(1, weight=0)
        if value == "new":
            l1.grid(row=0, column=1, padx=10, pady=10, sticky=W)
        else:
            l19.grid(row=0, column=1, padx=10, pady=10, sticky=W)
        l2.grid(row=1, padx=30, sticky=W)
        l3.grid(row=2, padx=30, sticky=W)
        l4.grid(row=3, padx=30, sticky=W)
        l5.grid(row=4, padx=30, sticky=W)
        l6.grid(row=5, padx=30, sticky=W)
        l7.grid(row=6, padx=30, sticky=W)
        l8.grid(row=7, padx=30, sticky=W)
        l9.grid(row=8, padx=30, sticky=W)
        l10.grid(row=9, padx=30, sticky=W)
        l11.grid(row=10, padx=30, sticky=W)
        b9.grid(row=3, column=1, padx=330, sticky=W)
        l13.grid(row=5, column=1, padx=90, sticky=W)
        l14.grid(row=6, column=1, padx=90, sticky=W)
        l15.grid(row=7, column=1, padx=90, sticky=W)
        l16.grid(row=8, column=1, padx=90, sticky=W)
        l17.grid(row=9, column=1, padx=90, sticky=W)
        e0.grid(row=1, column=1, padx=10, sticky=W)
        e1.grid(row=2, column=1, padx=10, pady=10, sticky=W)
        e2.grid(row=3, column=1, padx=10, sticky=W)
        e3.grid(row=4, column=1, padx=10,  pady=10, sticky=W)
        e4.grid(row=5, column=1, padx=10, sticky=W)
        e5.grid(row=6, column=1, padx=10, pady=10, sticky=W)
        e6.grid(row=7, column=1, padx=10, sticky=W)
        e7.grid(row=8, column=1, padx=10, pady=10, sticky=W)
        e8.grid(row=9, column=1, padx=10, sticky=W)
        c4.grid(row=10, column=1, pady=10, sticky=W)
        if value == "new":
            b5.grid(row=11, column=1, pady=5, sticky=W)
        else:
            b6.grid(row=11, column=1, pady=5, sticky=W)
        b7.grid(row=4, column=1, padx=330, sticky=W)


def trigger_choice(value):
    global final_trigger
    b_special_trigger.grid_forget()
    b2.grid_forget()
    b8.grid(row=1, column=1, pady=20)
    b3.grid(row=2, column=1, pady=20)
    b4.grid(row=3, column=1, pady=20)
    trigger_details = value.split(" | ")
    rownumber = trigger_listbox.curselection()[0]
    final_trigger = trigger_details_list[rownumber]
    e2.delete(0, END)
    e2.insert(0, final_trigger[4])
    e3.delete(0, END)
    e3.insert(0, final_trigger[5])
    e4.delete(0, END)
    e4.insert(0, final_trigger[6])
    e5.delete(0, END)
    e5.insert(0, final_trigger[7])
    e6.delete(0, END)
    e6.insert(0, final_trigger[8])
    e7.delete(0, END)
    e7.insert(0, final_trigger[9])
    e8.delete(0, END)
    e8.insert(0, final_trigger[10])
    if final_trigger[11] == "1":
        c4.select()


def trigger_ui(value):
    global trigger_details_list
    try:
        reset()
        tupel = ()
        trigger_details_list.clear()
        b8.grid_forget()
        b2.grid(row=1, column=1)
        b_special_trigger.grid(row=2, pady=30, column=1)
        # trigger_listbox.grid(row=1, column=0, padx=10, pady=10, rowspan=3, sticky=N+S+E+W)
        trigger_listbox.delete(0, END)
        zone_txt = codecs.open("trigger/" + e0.get() + ".txt", 'r', "utf-8")
        for para_line in zone_txt:
            paraline = str.rstrip(para_line)
            type_end = paraline.find('= ') + 2
            if 0 < type_end < len(paraline):
                line_type = str.lower(paraline[0:type_end])
                line_data = str.rstrip(paraline[type_end:])
                # line_data = umlaute2(line_data)
                if '#' not in line_type:
                    if 'trigger' in line_type or 'special' in line_type:
                        trigger_details = line_data.split("; ")
                        if value == trigger_details[2]:
                            trigger_details_list += [trigger_details]
                            trigger_listbox.insert(END, trigger_details[4] + " | " + trigger_details[5])
        zone_txt.close()
    except:
        guioutput("Folder trigger is missing")


def boss_ui(value):
    try:
        reset()
        tupel = ()
        # boss_listbox.grid(row=0, column=1, padx=10, pady=10, sticky=N+S+E+W)
        b8.grid_forget()
        b2.grid(row=1, column=1)
        b_special_trigger.grid(row=2, pady=30, column=1)
        boss_listbox.delete(0, END)
        trigger_listbox.delete(0, END)
        zone_txt = codecs.open("trigger/" + value + ".txt", 'r', "utf-8")
        for para_line in zone_txt:
            paraline = str.rstrip(para_line)
            type_end = paraline.find('= ') + 2
            if 0 < type_end < len(paraline):
                line_type = str.lower(paraline[0:type_end])
                line_data = str.rstrip(paraline[type_end:])
                # line_data = umlaute2(line_data)
                if 'trigger' in line_type or 'special' in line_type:
                    line_data = line_data.split("; ")
                    if line_data[2] not in tupel:
                        tupel += (line_data[2],)
                        boss_listbox.insert(END, line_data[2])
        zone_txt.close()
    except:
        guioutput("Trigger is missing")


def trigger_dir(folder):
    zonen = []
    triggerdir = os.listdir(folder)
    for item in triggerdir:
        if item != "abilities" and item != "keywords.txt" and item != "default.txt" and item != "Weaponstone Flask and Food.txt":
            zonen += [item.split(".txt")[0]]
    return zonen


def zone_list():
    global zonelist
    forget()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.columnconfigure(1, weight=1)
    zone_listbox.grid(row=0, column=0, padx=10, pady=10, sticky=N+S+E+W)
    boss_listbox.grid(row=0, column=1, padx=10, pady=10, sticky=N + S + E + W)
    trigger_listbox.grid(row=1, column=0, padx=10, pady=10, rowspan=3, sticky=N + S + E + W)
    b8.grid_forget()
    if not final_trigger:
        # print(final_trigger)
        b2.grid(row=1, column=1)
        b_special_trigger.grid(row=2, pady=30, column=1)
    else:
        b8.grid(row=1, column=1, pady=20)
        b3.grid(row=2, column=1, pady=20)
        b4.grid(row=3, column=1, pady=20)
    try:
        zonelist = trigger_dir("trigger")
        # print(zonelist)
        zone_listbox.delete(0, END)
        for items in zonelist:
            zone_listbox.insert(END, items)
    except:
        guioutput("Folder trigger is missing")


def mainmenue():
    forget()
    b2.grid_forget()
    x = 20
    y = 80
    l0.grid(row=0, column=0, padx=x, pady=20, sticky=NW)
    c1.grid(row=0, column=0, padx=x, pady=y, sticky=NW)
    c2.grid(row=0, column=0, padx=x, pady=y+40, sticky=NW)
    c3.grid(row=0, column=0, padx=x, pady=y+80, sticky=NW)
    l20.grid(row=0, column=0, padx=x, pady=80, sticky=S)
    volume_bar.grid(row=0, column=0, padx=x, pady=30, sticky=S)
    if buffcheck == 1:
        c3.select()
    b1.grid(row=1, column=0, pady=20)
    T.grid(row=0, column=1, rowspan=2, sticky=N+S+E+W)
    sb.grid(row=0, column=2, rowspan=2, sticky=N+S+E+W)
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=0)
    root.rowconfigure(1, weight=0)
    root.columnconfigure(1, weight=1)
    zone_listbox.grid_forget()
    boss_listbox.grid_forget()
    trigger_listbox.grid_forget()


def forget():

    b1.grid_forget()
    b2.grid_forget()
    b3.grid_forget()
    b4.grid_forget()
    b5.grid_forget()
    b6.grid_forget()
    b7.grid_forget()
    b8.grid_forget()
    b9.grid_forget()
    b_special_trigger.grid_forget()
    b_special_trigger1.grid_forget()
    b_special_trigger2.grid_forget()

    volume_bar.grid_forget()

    c1.grid_forget()
    c2.grid_forget()
    c3.grid_forget()
    c4.grid_forget()

    e0.grid_forget()
    e1.grid_forget()
    e2.grid_forget()
    e3.grid_forget()
    e4.grid_forget()
    e5.grid_forget()
    e6.grid_forget()
    e7.grid_forget()
    e8.grid_forget()
    e9.grid_forget()
    e_special1.grid_forget()
    e_special2.grid_forget()
    e_special3.grid_forget()
    e_special4.grid_forget()
    e_special5.grid_forget()
    e_special6.grid_forget()
    e_special7.grid_forget()
    e_special8.grid_forget()
    e_special9.grid_forget()
    e_special10.grid_forget()
    e_special11.grid_forget()
    e_special11.grid_forget()
    e_special12.grid_forget()
    e_special13.grid_forget()

    l0.grid_forget()
    l1.grid_forget()
    l2.grid_forget()
    l3.grid_forget()
    l4.grid_forget()
    l5.grid_forget()
    l6.grid_forget()
    l7.grid_forget()
    l8.grid_forget()
    l9.grid_forget()
    l10.grid_forget()
    l11.grid_forget()
    l12.grid_forget()
    l13.grid_forget()
    l14.grid_forget()
    l15.grid_forget()
    l16.grid_forget()
    l17.grid_forget()
    l18.grid_forget()
    l19.grid_forget()
    l20.grid_forget()

    l_special0.grid_forget()
    l_special1.grid_forget()
    l_special2.grid_forget()

    sound_listbox.grid_forget()
    abilities_listbox.grid_forget()
    scrollbar.grid_forget()
    sb.grid_forget()

    zone_listbox.grid_forget()
    boss_listbox.grid_forget()
    trigger_listbox.grid_forget()

    T.grid_forget()


def reset():
    global final_trigger
    # e1.delete(0, END)
    # e1.insert(0, "")
    # final_trigger.clear()
    e2.delete(0, END)
    e2.insert(0, "")
    e3.delete(0, END)
    e3.insert(0, "")
    e4.delete(0, END)
    e4.insert(0, "0")
    e5.delete(0, END)
    e5.insert(0, "0")
    e6.delete(0, END)
    e6.insert(0, "0")
    e7.delete(0, END)
    e7.insert(0, "0")
    e8.delete(0, END)
    e8.insert(0, "0")
    e9.delete(0, END)
    e9.insert(0, "0")
    c4.deselect()

    e_special1.delete(0, END)
    e_special2.delete(0, END)
    e_special3.delete(0, END)
    e_special4.delete(0, END)
    e_special5.delete(0, END)
    e_special6.delete(0, END)
    e_special7.delete(0, END)
    e_special8.delete(0, END)
    e_special9.delete(0, END)
    e_special10.delete(0, END)
    e_special11.delete(0, END)
    e_special12.delete(0, END)
    e_special13.delete(0, END)
    e_special1.insert(0, "")
    e_special2.insert(0, "")
    e_special3.insert(0, "")
    e_special4.insert(0, "")
    e_special5.insert(0, "")
    e_special6.insert(0, "")
    e_special7.insert(0, "")
    e_special8.insert(0, "")
    e_special9.insert(0, "")
    e_special10.insert(0, "")
    e_special11.insert(0, "")
    e_special12.insert(0, "")
    e_special13.insert(0, "")

    # trigger_listbox.delete(0, END)


root = Tk()
root.geometry("800x400")
root.title("Rift Raid Alert")

menubar = Menu(root)
menubar.add_command(label="Main", command=mainmenue)
menubar.add_command(label="Trigger", command=zone_list)
root.config(menu=menubar)

sb = Scrollbar(root)
scrollbar = Scrollbar(root)
T = Text(root, height=20, width=50)
sb.config(command=T.yview)
T.config(yscrollcommand=sb.set)
T.insert(END, "Rift Raid Alert Version 0.5.2\nMake sure you use /log in Rift after each game restart !")

soundfiles = soundfiles_list('siri')
combattrigger = 1
buffcheck = 1
output = "mix"
trigger = []
special = []
keywords = []
stacks = []
bufftrigger = []
abilities_old = []
abilities_new = []
# defaulttrigger = []
zone = ""
zonelist = trigger_dir("trigger")
logfile = ""
volume = 100
triggerload("RiftRaidAlert.ini")
triggerload("default")
defaulttrigger = trigger
defaultspecial = special
if buffcheck == 1:
    triggerload("Weaponstone Flask and Food")
    bufftrigger = trigger
trigger = defaulttrigger + bufftrigger
speak = win32com.client.Dispatch('Sapi.SpVoice')
speak.Volume = volume
timerreset = []
siri = True
location = "all"
playername = "noname"
boss = "all"
language = "all"
specialtrigger = 5
timeout_trigger = []
stacks_trigger = []
depending = 0
counter1 = 0
counter2 = 0
playback = False  # only for Playback a logfile from line 1
error_analysis = False
logfilecheck()

trigger_details_list = []
var_wav = IntVar()
var_tts = IntVar()
var_buffcheck = IntVar()
var_zone = StringVar()
var_reset = StringVar()
var_save = StringVar()
final_trigger = []
# zone_listbox_value = ""

l0 = Label(root, text="Activate the Logfile with /log in Rift !")
l1 = Label(root, text="New Trigger:")
l2 = Label(root, text="Zone:")
l3 = Label(root, text="Boss:")
l4 = Label(root, text="Text to Search:")
l5 = Label(root, text="Text to Speech:")
l6 = Label(root, text="Timer:")
l7 = Label(root, text="Countdown")
l8 = Label(root, text="Timeout:")
l9 = Label(root, text="Number of Events:")
l10 = Label(root, text="Dependent:")
l11 = Label(root, text="Reset:")
l12 = Label(root, text="At least 5 letters")
l13 = Label(root, text="The trigger is only executed after the specified time has elapsed.")
l14 = Label(root, text="Before the end of the time a countdown is announced (3..2..1).")
l15 = Label(root, text="After triggering, the trigger will be ignored for the specified time.")
l16 = Label(root, text="Number of events before the trigger fires e.g. stacks until tank swap.")
l17 = Label(root, text="Is currently not used (only for Lord Arak) but for the future.")
l18 = Label(root, text="Check your entries!", fg="red", font='bold')
l19 = Label(root, text="Edit Trigger:")
l20 = Label(root, text="Text to Speech Volume:")
c1 = Checkbutton(root, text="Soundfiles (*.wav)", variable=var_wav, command=wav)
if output == "mix" or output == "wav":
    c1.select()
c2 = Checkbutton(root, text="Text to Speech", variable=var_tts, command=tts)
if output == "mix" or output == "tts":
    c2.select()
c3 = Checkbutton(root, text="Weaponstone Flask and Food Check", variable=var_buffcheck, command=buff_check)
c4 = Checkbutton(root, text="Stop all running Timer and Countdowns", variable=var_reset)

b1 = Button(root, text="EXIT", width=20, command=ask_quit)
b2 = Button(root, text="New Trigger", width=20, command=lambda: new_trigger("new"))
b3 = Button(root, text="Edit Trigger", width=20, command=lambda: new_trigger("edit"))
b4 = Button(root, text="Delete Trigger", width=20, command=lambda: edit_trigger("delete"))
b5 = Button(root, text="Save", width=20, command=lambda: save_newtrigger("new"))
b6 = Button(root, text="Save", width=20, command=lambda: edit_trigger("edit"))
b7 = Button(root, text="Sound File", width=10, command=sound_file)
b8 = Button(root, text="Test Trigger", width=20, command=test_trigger)
b9 = Button(root, text="Abilities", width=10, command=abilities)
b_special_trigger = Button(root, text="Special Trigger", width=20, command=lambda: special_trigger("new"))
b_special_trigger1 = Button(root, text="Save", width=20, command=lambda: save_newtrigger("special_new"))
b_special_trigger2 = Button(root, text="Save", width=20, command=lambda: edit_trigger("special_edit"))

volume_bar = Scale(root, from_=0, to=100, orient=HORIZONTAL)
volume_bar.set(volume)

e0 = Entry(root, width=50)
e1 = Entry(root, width=50)
e2 = Entry(root, width=50)
e3 = Entry(root, width=50)
e4 = Entry(root, width=10)
e5 = Entry(root, width=10)
e6 = Entry(root, width=10)
e7 = Entry(root, width=10)
e8 = Entry(root, width=10)
e9 = Entry(root, width=10)

l_special0 = Label(root, text="Special Trigger")
l_special1 = Label(root, text="Keywords occurs: output = text to speech 1, Next keyword occurs: output = text to speech 2 ...")
l_special2 = Label(root, text="Keywords:")
e_special1 = Entry(root, width=50)
e_special2 = Entry(root, width=50)
e_special3 = Entry(root, width=50)
e_special4 = Entry(root, width=50)
e_special5 = Entry(root, width=50)
e_special6 = Entry(root, width=50)
e_special7 = Entry(root, width=50)
e_special8 = Entry(root, width=50)
e_special9 = Entry(root, width=50)
e_special10 = Entry(root, width=50)
e_special11 = Entry(root, width=50)
e_special12 = Entry(root, width=50)
e_special13 = Entry(root, width=50)

zone_listbox = Listbox(root, width=60, height=10)
zone_listbox.bind('<<ListboxSelect>>', zone_select)
boss_listbox = Listbox(root, width=60, height=10)
boss_listbox.bind('<<ListboxSelect>>', boss_select)
trigger_listbox = Listbox(root, width=60, height=10)
trigger_listbox.bind('<<ListboxSelect>>', trigger_select)
sound_listbox = Listbox(root, width=47, height=5)
sound_listbox.bind('<<ListboxSelect>>', sound_file_select)
abilities_listbox = Listbox(root, width=47, height=5)
abilities_listbox.bind('<<ListboxSelect>>', ability_select)

mainmenue()
root.protocol("WM_DELETE_WINDOW", ask_quit)
root.mainloop()
