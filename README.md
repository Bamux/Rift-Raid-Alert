## Rift Raid Alert v0.2.9
Rift Raid Alert is a program (written in Python) which can be used to create spoken raid warnings for the MMORPG Rift.
The current version support announcements for RoF, IGP, MoM and CoA. You can use Rift Raid Alert with Team Speak so the whole Raid can benefit from.

Video: https://youtu.be/jGX8BH6vb2w

Features:
- search the chat messages and alert you when certain phrases/keywords appear in the chat channel
- encounter timers and countdowns
- tank swap mechanic
- tracking buffs and debuffs
- monitors waeponstones, flasks and food
- pull countdown and alert you if the tank has aggro or who has fail pulled
- make your own timers, countdowns and alerts without Lua knowledge

## Installation Instructions:

1.  Download and unzip the Rift-Raid-Alert-master.zip - https://github.com/Bamux/Rift-Raid-Alert/archive/master.zip
2.  Copy the Rift-Raid-Alert-master folder in your Rift Addon folder
3.  Start Rift
4.  use /log in the rift chatwindow
5.  Start the RiftRaidAlert.exe
6.  use /rra start (you can use /rra stop for stoping Rift Raid Alert) or /rra keywords if you want only search for key words from the keywords.txt
7.  Write in game "Siri introduce yourself" or "Siri tell me a joke" or "Siri say whatever you want" for a sound check
8.  Edit the RiftRaidAlert.ini - you can change settings (Log.txt path, volume, ...)
9.  Edit the text files in the trigger folder - you can edit/create triggers

Ingame Commands:
- /rra start - start Raid announcements for RoF, IGP, MoM and CoA
- /rra stop - stop Rift Raid Alert
- /rra check - checks waeponstones, flasks and food of all players in the raid
- /rra keywords - search the chat for keywords from your keywords.txt (in your trigger folder). As an example, you are looking for a Raid for CoA. If both words (CoA and lfm) appear in the chat channel you'll be informed. The advantage is you can running Rift in the background watch a movie, surf the web etc. while waiting that someone is looking for players.

## Select a Voice
Open the Windows Text to Speech Engine and select your voice. The default folder is:
- C:\Windows\SysWOW64\Speech\SpeechUX\sapi.cpl

I use the Microsoft Speech API (SAPI 5) . The Python program that I wrote scans the Rift Log.txt file according to predefined parameters and passes it to the SAPI 5 interface. You can use any voice that was created for the SAPI 4 or SAPI 5 interface. There are many free voices (often sound robotic) but also very natural sounding voices. 

Under http://www.mwsreader.com/en/voices/ you can download other voices (different languages). 



## How to use Rift Raid Alerts on TeamSpeak:

1. INSTALL VB-CABLE Virtual Audio Device - http://vb-audio.pagesperso-orange.fr/Cable/index.htm
2. Right click on the windows speaker icon > choose Recording Devices > double clicking CABLE Output > Listen > Playback through this device: coose Default Playback Device and checking the box
3. Open the Windows Text to Speech Engine. Default folder is C:\Windows\SysWOW64\Speech\SpeechUX\sapi.cpl
   Advanced > choose CABLE Input (VB-Audio Virtual Cable)
3. Open teamspeak > Option > Capture and Create a new Profil, coose CABLE Output (VB-Audio Virtual Cable) as your Recording Device
4. Read how to use multiple Teamspek Clients - http://www.gameplayinside.com/optimize/multiple-teamspeak-3-clients/ 
5. Use one teamspek client with your default profil and the second teamspek client with your new profil for Raid Rift Alerts

![Recording Devices](https://raw.githubusercontent.com/Bamux/Rift-Raid-Alert/images/Recording%20Devices.png)
