# Rift Raid Warnings
# Spoken raid warnings for the MMORPG Rift
# Version 0.3 
# Author: Bamux@Typhiria

from threading import Thread
import os, time
import string, sys, re, pythoncom
import win32com.client # the Python for Windows extensions (win32com.client) should be installed https://sourceforge.net/projects/pywin32/files/pywin32/


def combatlogfileanalysis(combatlogtext):

        #Timer
        MOM_Pagura_Icesoul = 52 # Time from first Curse of Four until Ice Soul
        MOM_Pagura_Icesouls = 70 # Time between Ice Souls
        MOM_Pagura_Icesoul_P3 = 47 # Time from first Curse of Five until Ice Soul
        
        global timerreset
        text = ""
        IGP = True
        MoM = True

        while True:
                combatlog = combatlogtext.readline()

                if combatlog:
                
                # MoM Pagura
                
                        if MoM_Pagura == True and MoM == True:
                          
                                if 'Pagura begins casting Curse of Four' in combatlog:
                                    IGP = False    
                                    if timerreset == True:  
                                        timerreset = False
                                        t = Thread(target=timer, args=(MOM_Pagura_Icesoul,))
                                        t.start()
                                        team = 1
                                        text = 'Team 1'
                                        
                                    elif team == 1:
                                        team = 2
                                        text = 'Team 2'
                                        
                                    else:
                                        team = 1
                                        text = 'Team 1'

                                elif 'Pagura begins casting Curse of Five' in combatlog:
                                        
                                    if timerreset == True:  
                                        timerreset = False
                                        t = Thread(target=timer, args=(MOM_Pagura_Icesoul_P3,))
                                        t.start()
                                        team = 1
                                        text = 'Team 1'
                                        
                                    elif team == 1:
                                        team = 2
                                        text = 'Team 2'
                                        
                                    else:
                                        team = 1
                                        text = 'Team 1'
                                        
                                elif 'Pagura begins casting Leaping Contagion' in combatlog:
                                        text = 'spread out'
                                        
                                elif 'Pagura begins casting Shattering Roar' in combatlog:      
                                        timerreset = False
                                        t = Thread(target=countdown, args=(17,))
                                        t.start()                
                                        t = Thread(target=timer, args=(MOM_Pagura_Icesouls,))
                                        t.start()
                                        text = 'Ice Soul'
                                        
                                elif 'begins casting Pain Bringer' in combatlog:      
                                        shell = win32com.client.Dispatch('WScript.Shell') 
                                        shell.SendKeys("{F3}", 0) 
                            
                        if 'Combat End' in combatlog:
                                print('Combat End')
                                timerreset = True
                                IGP = True
                                MoM = True

                #IGP Anrak
                                        
                        if IGP_Anrak == True and IGP == True:
                                
                                if 'Anrak the Foul begins casting Spines of Earth.' in combatlog:
                                        text = 'spread out'
                                        MoM = False

                                elif 'Anrak the Foul begins casting Swarm of Anrak.' in combatlog:
                                        text = 'prepare for adds'
                #IGP Guurloth
                                        
                        if IGP_Guurloth == True and IGP == True:
                                
                                if 'Guurloth begins casting Boulder of Destruction.' in combatlog:
                                        text = 'Tank damage, stun the add.'

                                elif 'Guurloth begins casting Dance with Death.' in combatlog:
                                        text = 'dance'
                                        
                                elif 'Guurloth begins casting Earthen Toil.' in combatlog:
                                        text = 'run Forrest run'

                                elif 'Guurloth begins casting Guurloth' in combatlog:
                                        text = 'add'
                                        
                                elif 'Guurloth begins casting Orb of Searing Power.' in combatlog:
                                        text = 'turn'

                                elif 'Guurloth begins casting Rumbling Earth.' in combatlog:
                                        text = 'jump'
                                        MoM = False
                                        
                                elif 'Guurloth begins casting The Point.' in combatlog:
                                        text = 'point'

                #IGP Thalguur
                                        
                        if IGP_Thalguur == True and IGP == True:
                                
                                if ''"is afflicted by Thalguur's Curse of Greed."'' in combatlog:
                                        cut_string = combatlog.split('Curse of Greed , 0 ) ')
                                        new_string = cut_string[1]
                                        cut_string = new_string.split(''" is afflicted by Thalguur's Curse of Greed."'')
                                        new_string = cut_string[0]
                                        cut_string = new_string.split('@')
                                        new_string = cut_string[0]
                                        text = (new_string + ' run out')
                                        MoM = False
                #IGP Uruluuk
                                        
                        if IGP_Uruluuk == True and IGP == True:
                                
                                if 'Uruluuk begins casting Crashing Boulders.' in combatlog:
                                        text = 'Boulders'
                                        MoM = False

                                elif 'Uruluuk begins casting Fist of Laethys.' in combatlog:
                                        text = 'Fist'
                                                                             
                        if text:
                                #print (text)
                                Thread(target=SayText,args=(text,)).start()
                                text = ""
                                
                else:
                        time.sleep(0.50) # waiting for a new line

                                  
def logfileanalysis(logtext):      
        global timerreset
        text = ""
        
        while True:
                
                log = logtext.readline()

                if log:

                # MoM Pagura
                       
                        if MoM_Pagura == True and MoM == True:
                                
                                if 'Raaaarrrrhhh' in log:
                                        timerreset = True
                                        text = 'Phase 2 go to left Golem'
                                        IGP = False

                                elif '[Bamux]: run out' in log:
                                        cut_string = log.split('run out ')
                                        new_string = cut_string[1]
                                        cut_string = new_string.split('@')
                                        new_string = cut_string[0]
                                        text = (new_string + ' run out')
                                        
                #IGP Guurloth

                        if IGP_Guurloth == True and IGP == True:
                                
                                if 'will do nothing or you all suffer!' in log:
                                        cut_string = log.split('Guurloth screams, "')
                                        new_string = cut_string[1]
                                        cut_string = new_string.split(' will do nothing or you all suffer!')
                                        new_string = cut_string[0]
                                        cut_string = new_string.split('@')
                                        new_string = cut_string[0]
                                        text = (new_string + ' stop')
                                        MoM = False
                #IGP Uruluuk

                        if IGP_Uruluuk == True and IGP == True:
                                
                                if 'Uruluuk points at' in log:
                                        cut_string = log.split('Uruluuk points at ')
                                        new_string = cut_string[1]
                                        cut_string = new_string.split('!')
                                        new_string = cut_string[0]
                                        cut_string = new_string.split('@')
                                        new_string = cut_string[0]
                                        text = (new_string + ' run out')
                                        MoM = False
                        if text:
                                print (text)
                                Thread(target=SayText,args=(text,)).start()
                                text = ""
                else:
                        time.sleep(0.50) # waiting for a new line

      
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
                                t = Thread(target=combatlogfileanalysis, args=(combatlogtext,))
                                t.start()
                                t = Thread(target=logfileanalysis, args=(logtext,))
                                t.start()                                
                                #logtext.close()
                                #combatlogtext.close()
        else:
                print ('use /combatlog and /log in Rift and edit the path to your Logfiles in the Rift_Raid_Warnings.ini !')
                time.sleep(20)
                logfilecheck(combatlogfile,logfile)


def timer(seconds):
        print('Start timer with ' + str(seconds) + ' seconds. ')
        for i in range(0,seconds-warningtime):
                if (timerreset == False):
                        time.sleep(1)
                else:
                        print('Stop timer.')
                        return
                
        t = Thread(target=countdown, args=(warningtime,))
        t.start()         
        speak.Speak(str(warningtime) + ' seconds left')    


def countdown(count):
        print('Start countdown with ' + str(count) + ' seconds.')
        for i in range(0,count):
                #print (count-i)
                if (timerreset == False):
                        if count-i < 4:
                                Thread(target=SayText,args=(count-i,)).start()
                                #print (count-i)
                        time.sleep(1)
                else:
                        print('Stop countdown.')
                        return  

def SayText(text):
	# this is to allow the speech engine to run in a thread
	try:
		pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
	except pythoncom.com_error:
	# already initialized.
		pass
	# connect to the speech engine
	speak.Speak(text)


#get parametrs from Rift_Raid_Warnings.ini
	
try:      
        ini = open('RiftRaidWarnings.ini','r')
        try:
                for para_line in ini:
                        paraline = str.rstrip(para_line)
                        type_end = paraline.find('= ')+2
                        
                        if type_end > 0 and type_end < len(paraline):
                                line_type = str.lower(paraline[0:type_end])
                                line_data = str.rstrip(paraline[type_end:])
                                line_data_lower = str.lower(paraline[type_end:])
                                
                                if 'logfile' in line_type:
                                        logfile = line_data
                                        #print (logfile)
                                        
                                if 'combatfile' in line_type:
                                        combatlogfile = line_data
                                        #print (combatlogfile)

                                if 'warningtime' in line_type:
                                        warningtime = int(line_data)
                                        #print (warningtime)

                                if 'anrak' in line_type:
                                        IGP_Anrak = line_data
                                        if 't' == line_data_lower[0] or 'y' == line_data_lower[0]:
                                                IGP_Anrak = True
                                        else: 
                                                IGP_Anrak = False                                         
                                                
                                if 'guurloth' in line_type:
                                        IGP_Guurloth = line_data
                                        if 't' == line_data_lower[0] or 'y' == line_data_lower[0]:
                                                IGP_Anrak = True
                                        else: 
                                                IGP_Anrak = False
                                        
                                if 'thalguur' in line_type:
                                        IGP_Thalguur = line_data
                                        if 't' == line_data_lower[0] or 'y' == line_data_lower[0]:
                                                IGP_Thalguur = True
                                        else: 
                                                IGP_Thalguur = False
                                        
                                if 'uruluuk' in line_type:
                                        IGP_Uruluuk = line_data
                                        if 't' == line_data_lower[0] or 'y' == line_data_lower[0]:
                                                IGP_Uruluuk = True
                                        else: 
                                                IGP_Uruluuk = False
                                        
                                if 'pagura' in line_type:
                                        MoM_Pagura = line_data
                                        if 't' == line_data_lower[0] or 'y' == line_data_lower[0]:
                                                MoM_Pagura = True
                                        else: 
                                                MoM_Pagura = False 
                                        
                ini.close         
        except:
                print ('Error in reading parameters')

except:
        print ('Cannot find Parameter file RiftRaidWarnings.ini')
        time.sleep(20)
        sys.exit('RiftRaidWarnings.ini not found')

      
print ('Make sure you use /combatlog and /log in Rift after each game restart !!!')
speak = win32com.client.Dispatch('Sapi.SpVoice')
text = 'Rift raid Warnings active! Make sure you use /combatlog and /log in Rift !'
#Thread(target=SayText,args=(text,)).start()
timerreset = True
logfilecheck(combatlogfile,logfile)

