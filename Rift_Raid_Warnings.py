# Rift Raid Warnings
# Spoken raid warnings for the MMORPG Rift
# Version 0.3 
# Author: Bamux@Typhiria

from threading import Thread
import os, time
import win32com.client # the Python for Windows extensions (win32com.client) should be installed https://sourceforge.net/projects/pywin32/files/pywin32/


# !!! use /log and /combatlog in Rift to create the logfiles each time you restart Rift!!!
# Edit the Path to your Log.txt and CombLog.txt
logfile = "C:/Users/Enermax/Documents/RIFT/Log.txt"
combatlogfile = "C:/Users/Enermax/Documents/RIFT/CombatLog.txt"

warningtime = 5  # how many seconds before an event occurs a warning

def logfileanalysis(combatlogtext,logtext):

        IGP = True # True or False if you want or dont want Raid Warnings for IGP
        IGP_Anrak = True 
        IGP_Guurloth = True
        IGP_Thalguur = True
        IGP_Uruluuk = True
        
        MoM = True # True or False if you want or dont want raid warnings for MoM
        MoM_Pagura = True 
        
        icesoul = 52 # Time from first Curse of Four until Ice Soul
        icesouls = 70 # Time between Ice Souls
        icesoulp3 = 47 # Time from first Curse of Five until Ice Soul
        
        global timerreset
        
        while True:
                combatlog = combatlogtext.readline()
                log = logtext.readline()

        # MoM Pagura
                
                if MoM_Pagura == True and MoM == True:                 
                                
                        if 'Pagura begins casting Curse of' in combatlog:
                                
                            if timerreset == True:  
                                timerreset = False
                                team = 2
                                t = Thread(target=timer, args=(icesoul,))
                                t.start()
                                speak.Speak('Team 1')
                                
                            elif team == 1:
                                team = 2
                                speak.Speak('Team 1')
                                
                            else:
                                team = 1                  
                                speak.Speak('Team 2')

                        elif 'Pagura begins casting Leaping Contagion' in combatlog:      
                                speak.Speak('spread out')
                                
                        elif 'Pagura begins casting Shattering Roar' in combatlog:      
                                timerreset = False
                                t = Thread(target=countdown, args=(17,))
                                t.start()                
                                t = Thread(target=timer, args=(icesouls,))
                                t.start()
                                speak.Speak('Ice Soul')
                                
                        elif 'Raaaarrrrhhh' in log:
                                timerreset = True
                                icesoul = icesoulp3 #Time from first Curse of Five until Ice Soul
                                speak.Speak('Phase 2 go to left Golem')
                                
                        elif 'Pagura begins casting Leaping Contagion' in combatlog:      
                                speak.Speak('spread out')
                                
                        elif 'begins casting Pain Bringer' in combatlog:      
                                shell = win32com.client.Dispatch('WScript.Shell') 
                                shell.SendKeys("{F4}", 0) 
                                
                        elif '[Bamux]: run out' in log:
                                cut_string = log.split('run out ')
                                new_string = cut_string[1]
                                cut_string = new_string.split('@')
                                new_string = cut_string[0]
                                speak.Speak(new_string + ' run out')
                                print(new_string)
                    
                        elif 'begins casting Call of the Ascended' in combatlog or 'Combat End' in combatlog:
                                print('Combat End')
                                speak.Speak('End')
                                #team = 0
                                timerreset = True 
                                
                time.sleep(0.10) # waiting for a new line


def timer(seconds):
        print('Start timer with ' + str(seconds) + ' seconds. ')
        for i in range(0,seconds-warningtime):
                if (timerreset == False):
                        time.sleep(1)
                else:
                        print('Stop timer. ')
                        return
                
        t = Thread(target=countdown, args=(warningtime,))
        t.start()         
        speak.Speak(str(warningtime) + ' seconds left')    
 

def countdown(count):
        print('Start countdown with ' + str(count) + ' seconds. ')
        for i in range(0,count):
                if (timerreset == False):
                        if count-i < 4:
                                t = Thread(target=speak.Speak, args=(count-i,))
                                t.start()
                        time.sleep(1)
                else:
                        print('Stopped countdown. ')
                        return        

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
                                combatlogtext.seek(0, 2)
                                logtext.seek(0, 2)
                                logfileanalysis(combatlogtext,logtext)
                                logtext.close()
                                combatlogtext.close()
        else:
                print ('!!! use /combatlog and /log in Rift !!!')
                time.sleep(20)
                logfilecheck(combatlogfile,logfile)



print ('Make sure you use /combatlog and /log in Rift after each game restart !!!')
speak = win32com.client.Dispatch('Sapi.SpVoice') # connect to the speech engine
#speak.Speak('Rift raid Warnings active! Make sure you use /combatlog and /log in Rift !')
timerreset = True
logfilecheck(combatlogfile,logfile)



