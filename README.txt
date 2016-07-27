Rift Raid Alert is an Addon which can be used to create spoken raid warnings for the MMORPG Rift. The current version support announcements for RoF, IGP, MoM and CoA.

Video: https://youtu.be/jGX8BH6vb2w

Features:
- search the chat messages and alert you when certain phrases/keywords appear in the chat channel
- encounter timers and countdowns
- tank swap mechanic
-tracking buffs and debuffs
- monitors waeponstones, flasks and food
- make your own timers, countdowns and alerts without Lua knowledge


Installation Instructions for Python:
I use the Microsoft Speech API (SAPI 5) . Rift has no API to interact with the Microsoft Speech API so I wrote a Python Script that scans the Rift Log.txt file according to predefined parameters and passes it to the SAPI 5 interface. You have to install Python and the Python for Windows Extensions !

- download and install Python 3.5.x or higher https://www.python.org/downloads/
- download and install Python for Windows Extensions https://sourceforge.net/projects/pywin32/files/pywin32/Build%20220/
- Python for Windows Extensions have a 32bit and a 64bit version available - you must download the one which corresponds to the Python you have installed. Even if you have a 64bit computer, if you installed a 32bit version of Python you must install the 32bit version of pywin32.


Installation Instructions for the Addon:
- copy the Rift-Raid-Alert-master folder in your Rift Addon folder
- start Rift
- use /log in the rift chatwindow
- double-click the Python Script start.py in your Rift-Raid-Alert-master folder
- use /rra start (you can use /rra stop for stoping Rift Raid Alert) or /rra keywords if you want only search for key words from the keywords.txt
- write in game "Siri introduce yourself" or "Siri tell me a joke" or "Siri say whatever you want" for a sound check
- edit the RiftRaidAlert.ini - you can change settings (Log.txt path, volume, ...)
- edit the text files in the trigger folder - you can edit/create triggers


Select a Voice:
You can use any voice that was created for the Microsoft Speech API (SAPI 4 or SAPI 5). Windows 7, 8 or 10 has a default text to speech voice mostly installed.

Under http://www.mwsreader.com/en/voices/ you can download other voices (different languages). There are many free voices (often sound robotic) but also very natural sounding voices.

To Select a voice open the Windows Text to Speech Engine. The default folder is: C:\Windows\SysWOW64\Speech\SpeechUX\sapi.cpl


How to use Rift Raid Alerts on TeamSpeak:
- INSTALL VB-CABLE Virtual Audio Device - http://vb-audio.pagesperso-orange.fr/Cable/index.htm
- Right click on the windows speaker icon > choose Recording Devices > double clicking CABLE Output > Listen > Playback through this device: coose Default Playback Device and checking the box
- Open the Windows Text to Speech Engine. Default folder is C:\Windows\SysWOW64\Speech\SpeechUX\sapi.cpl
- Settings for the Text to Speech Engine: Advanced > choose CABLE Input (VB-Audio Virtual Cable)
- Open teamspeak > Option > Capture and Create a new Profil, coose CABLE Output (VB-Audio Virtual Cable) as your Recording Device
- Read how to use multiple Teamspek Clients - http://www.gameplayinside.com/optimize/multiple-teamspeak-3-clients/
- Use one teamspek client with your default profil and the second teamspek client with your new profil for Raid Rift Alerts