# Rift Raid Warnings
# Spoken raid warnings for the MMORPG Rift
# Version 0.3 
# Author: Bamux@Typhiria
# Note: This code is based on the RiftSay Project http://www.mspeedie.com/RiftSay.html

from threading import Thread
import os, time
import string, sys, re, pythoncom
import win32com.client # the Python for Windows extensions (win32com.client) should be installed https://sourceforge.net/projects/pywin32/files/pywin32/
import win32pipe, win32file, win32com.shell

# !!! use /log and /combatlog in Rift to create the logfiles each time you restart Rift!!!
# Edit the Path to your Log.txt and CombatLog.txt
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
                
                #where = combatlogtext.tell()
                #combatlog = combatlogtext.readline()
                #st_results = os.stat(combatlogfile)
                #st_size = st_results[6]
                #combatlogtext.seek(st_size)

                combatlog = combatlogtext.readline()
                log = logtext.readline()

                if combatlog:

                # MoM Pagura
                        
                        if MoM_Pagura == True and MoM == True:


                                #r = re.compile('Pagura begins casting Curse of Five')

                                #if r.search(combatlog):
                                        #print ('yes')
                                
                                        
                                if 'Pagura begins casting Curse of' in combatlog:
                                        
                                    if timerreset == True:  
                                        timerreset = False
                                        team = 1
                                        text = 'Team 1'
                                        Thread(target=SayText,args=(text,)).start()
                                        #print ("läuft")
                                        
                                    elif team == 1:
                                        team = 2
                                        text = 'Team 2'
                                        Thread(target=SayText,args=(text,)).start()
                                        
                                    else:
                                        team = 1
                                        text = 'Team 1'
                                        Thread(target=SayText,args=(text,)).start()

                                elif 'Pagura begins casting Leaping Contagion' in combatlog:
                                        text = 'spread out'
                                        Thread(target=SayText,args=(text,)).start()
                                        
                                elif 'Pagura begins casting Shattering Roar' in combatlog:      
                                        timerreset = False
                                        t = Thread(target=countdown, args=(17,))
                                        t.start()                
                                        t = Thread(target=timer, args=(icesouls,))
                                        t.start()
                                        text = 'Ice Soul'
                                        Thread(target=SayText,args=(text,)).start()
                                        
                                elif 'Raaaarrrrhhh' in log:
                                        timerreset = True
                                        icesoul = icesoulp3 #Time from first Curse of Five until Ice Soul
                                        text = 'Phase 2 go to left Golem'
                                        Thread(target=SayText,args=(text,)).start()
                                        
                                elif 'Pagura begins casting Leaping Contagion' in combatlog:      
                                        text = 'spread out'
                                        Thread(target=SayText,args=(text,)).start()
                                        
                                elif 'begins casting Pain Bringer' in combatlog:      
                                        shell = win32com.client.Dispatch('WScript.Shell') 
                                        shell.SendKeys("{F3}", 0) 
                                        
                                elif '[Bamux]: run out' in log:
                                        cut_string = log.split('run out ')
                                        new_string = cut_string[1]
                                        cut_string = new_string.split('@')
                                        new_string = cut_string[0]
                                        speak.Speak(new_string + ' run out')
                                        print(new_string)
                            
                                elif 'Combat End' in combatlog:
                                        print('Combat End')
                                        timerreset = True 
                                        
                else:
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
                #print (count-i)
                if (timerreset == False):
                        if count-i < 4:
                                Thread(target=SayText,args=(count-i,)).start()
                                #print (count-i)
                        time.sleep(1)
                else:
                        print('Stop countdown. ')
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


def SayText(text):

	# this is to allow the speech engine to run in a thread
	try:
		pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
	except pythoncom.com_error:
	# already initialized.
		pass
	# connect to the speech engine
	speak.Speak(text)



print ('Make sure you use /combatlog and /log in Rift after each game restart !!!')
speak = win32com.client.Dispatch('Sapi.SpVoice')
text = 'Rift raid Warnings active! Make sure you use /combatlog and /log in Rift !'
Thread(target=SayText,args=(text,)).start()
timerreset = True
logfilecheck(combatlogfile,logfile)



