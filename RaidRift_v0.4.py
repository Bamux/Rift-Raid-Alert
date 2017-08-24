import os
import time
import winsound
import codecs
from threading import Thread


def logfile_check():  # checks if a Log.txt is present
    try:
        logtext = codecs.open("Log.txt", 'r', "utf-8")
    except:
        try:
            logfile = os.path.expanduser('~\Documents\RIFT\Log.txt')
            logtext = codecs.open(logfile, 'r', "utf-8")
        except:
            try:
                logfile = 'C:\Program Files (x86)\RIFT Game\Log.txt'
                logtext = codecs.open(logfile, 'r', "utf-8")
            except:
                try:
                    logfile = 'C:\Programs\RIFT~1\Log.txt'
                    logtext = codecs.open(logfile, 'r', "utf-8")
                except:
                    print('Error! could not find the Log File')
                    print('use /log in Rift')
                    print('Restart RaidRift.py')
    if logtext:
        logfile_analysis(logtext)


def logfile_analysis(logtext):  # analyzes each new line in the Log.txt
    logtext.seek(0, 2)  # jumps to the end of the Log.txt
    keywords = []
    keywords += ['rr']
    keywords += ['Lure: The Iron Legion']
    keywords += ['Lure: Decay of Ahnket']
    keywords += ['Lure: Egg of Destruction']
    keywords += ['Köder: Ahnkets Fäulnis']
    keywords += ['Köder: Die Eisenlegion']
    keywords += ['Köder: Ei der Zerstörung']
    while True:
        line = ""
        log = ""
        line = logtext.readline()  # read new line
        if line:
            if "]: " in line:
                log = line.split("]: ")[1]
                log = str.lower(log)  # lower case
                if "lfm" in log:  # Checks if lfm and keyword exists in the new line
                    for keyword in keywords:
                        if str.lower(keyword) in log:
                            Thread(target=play_sound, args=("RaidRift.wav",)).start()  # plays the Soundfile RaidRift.wav
                            try:
                                playername = line.split("]: ")[0]
                                playername = playername.split("][")[1]
                                text = "/tell " + playername + " + "
                                add_to_clipboard(text)
                                print(time.strftime("%H:%M:%S") + " - " + playername)
                                print(line)
                            except:
                                pass
            elif "entered a raid group" in line or "einem Schlachtzug beigetreten" in line:
                logtext.close()
                os._exit(1)

        else:
            time.sleep(0.50)  # waiting for a new input


def add_to_clipboard(text):  # add to windows clipboard
    command = 'echo | set /p dummyVar="' + text + '" | clip'
    os.system(command)


def play_sound(file):
    winsound.PlaySound(file, winsound.SND_FILENAME)


print("RaidRift_v0.4")
logfile_check()
