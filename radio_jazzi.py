from datetime              import datetime
from subprocess            import *
from time                  import sleep, strftime
from Queue                 import Queue
from threading             import Thread
import os
from nanpy import Arduino, Lcd
 
Arduino.pinMode(14, input)
 
lcd = Lcd([8,9,4,5,6,7],[16,2])            # Setup the LCD pins for the Sainsmart Shield
lcd.printString("Jess's Web Radio",0,0)
lcd.printString("Loading" + "."*3,0,1)
sleep(5)
max_trax = 74
x = 1
loop_menu = 1
loop_radio = 1
 
def display_ipaddr():
   show_wlan0 = "ip addr show wlan0 | cut -d/ -f1 | awk '/inet/ {printf \"w%15.15s\", $2}'"
   show_eth0  = "ip addr show eth0  | cut -d/ -f1 | awk '/inet/ {printf \"e%15.15s\", $2}'"
   ipaddr = run_cmd(show_eth0)
   if ipaddr == "":
      ipaddr = run_cmd(show_wlan0)
   lcd.printString('IP Address:',0,0)
   lcd.printString(ipaddr,0,1)
   sleep(2)
 
def displaymenu():    
    if x==1:
        lcd.printString("1. Display      ",0,0)
        lcd.printString("   IP Address   ",0,1)
    elif x==2:
        lcd.printString("2. Audio Output ",0,0)
        lcd.printString("   to hdmi Port ",0,1)
    elif x==3:
        lcd.printString("3. Audio Output ",0,0)
        lcd.printString("  to Analog port",0,1)
    elif x==4:
        lcd.printString("4. Audio Output ",0,0)
        lcd.printString("  Auto Sel. Port",0,1)
    elif x==5:
        lcd.printString("5. Reload the   ",0,0)
        lcd.printString("   Playlist     ",0,1)
    elif x==6:
        lcd.printString("6. ShutDown     ",0,0)
        lcd.printString("   the System   ",0,1)
    else:
        lcd.printString("7. Exit to      ",0,0)
        lcd.printString("   Main Menu    ",0,1)
 
def load_playlist():
   output = run_cmd("mpc clear")
   output = run_cmd("/home/pi/radio_playlist.sh")
                             
def run_cmd(cmd):
   p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
   output = p.communicate()[0]
   return output
 
def getKey():                            
   val = Arduino.analogRead(14)
   if val == 1023:
      return "NONE"
   elif val < 100:
      return "RIGHT"
   elif val < 150:
      return "UP"
   elif val < 330:
      return "DOWN"
   elif val < 510:
      return "LEFT"
   elif val < 750:
      return "SEL"
   else:
      return "KBD_FAULT"
 
load_playlist()
def getTrack():
   #L= [S.strip('\n') for S in os.popen('mpc').readlines()]        # Get the Track info from the stdout of the mpc command
   output = run_cmd("mpc current")
   station = output [0:16]                                           # Pick out the Station and Track info
   track =  output [-17:-1]
   lcd.printString(station + " "*(16 - len(station)), 0, 0)
   lcd.printString(track + " "*(16 - len(track)), 0, 1)
 
track_num = 1                                                     # Start off on Track number 1
os.system("mpc play "+str(track_num))                             # Tell the OS to Play it
 
while loop_radio == 1:
   getTrack()
   loop_menu = 1
   x = 1
   key = getKey()
   if key == "UP":
      track_num += 1
      if track_num > max_trax:
         track_num = max_trax
      os.system("mpc play " + str(track_num))
      getTrack()
   elif key == "DOWN":
      track_num -= 1
      if track_num < 1:
         track_num = 1
      os.system("mpc play " + str(track_num))
      getTrack()
   elif key == "SEL":
      while loop_menu == 1:
           displaymenu()
           key = getKey()
           if key == "RIGHT":
                  os.system("mpc volume +2")
                  lcd.printString(16*" ", 0, 0)
                  lcd.printString(16*" ", 0, 1)
                  output = run_cmd("mpc volume")
                  lcd.printString("VOLUME UP:", 0, 0)
                  lcd.printString(output, 5, 1)
                  sleep(.25)
                  lcd.printString(16*" ",0,0)
                  lcd.printString(16*" ",0,1)
           elif key == "LEFT":
                  os.system("mpc volume -2")
                  lcd.printString(16*" ",0,0)
                  lcd.printString(16*" ", 0,1)
                  output = run_cmd("mpc volume")
                  lcd.printString("VOLUME DOWN:", 0, 0)
                  lcd.printString(output, 5, 1)
                  sleep(.25)
                  lcd.printString(16*" ",0,0)
                  lcd.printString(16*" ",0,1)
           elif key == "UP":
                 if x <= 1:
                     x = 7
                 else:
                    x = x - 1
           elif key == "DOWN":
                 if x >= 7:
                      x = 1
                 else:
                     x = x + 1      
           elif key == "SEL":
                 if x == 1:
                    display_ipaddr()
                    sleep(1)
                 elif x == 2:
                    output = run_cmd("amixer -q cset numid=3 2")
                    lcd.printString("Audio OUT-->HDMI", 0, 0)
                    lcd.printString("output ", 0, 1)
                    sleep(.5)
                 elif x == 3:
                    output = run_cmd("amixer -q cset numid=3 1")
                    lcd.printString("Audio OUT->Analog", 0, 0)
                    lcd.printString("output ", 0, 1)
                    sleep(.5)
                 elif x == 4:
                    output = run_cmd("amixer -q cset numid=3 0")
                    lcd.printString("Audio OUT->  Auto", 0, 0)
                    lcd.printString("output ", 0, 1)
                    sleep(.5)
                 elif x == 5:
                    load_playlist()      
                    os.system('mpc play 1')
                 elif x == 6:
                    lcd.printString("Good Bye         ", 0, 0)
                    lcd.printString("Have a Nice Day  ", 0, 1)
                    output = run_cmd("mpc clear")
                    output = run_cmd("sudo shutdown now")
                 elif x == 7:
                     loop_menu = 0
                     getTrack()
                 break
           elif key == "RIGHT":
                  os.system("mpc volume +2")
                  lcd.printString(16*" ",0,0)
                  lcd.printString(16*" ", 0,1)
                  output = run_cmd("mpc volume")
                  lcd.printString("VOLUME UP:", 0, 0)
                  lcd.printString(output, 5, 1)
                  sleep(.25)
                  lcd.printString(16*" ",0,0)
                  lcd.printString(16*" ",0,1)
           elif key == "LEFT":
                  os.system("mpc volume -2")
                  lcd.printString(16*" ", 0, 0)
                  lcd.printString(16*" ", 0, 1)
                  output = run_cmd("mpc volume")
                  lcd.printString("VOLUME DOWN:", 0, 0)
                  lcd.printString(output, 5, 1)
                  sleep(.25)
                  lcd.printString(16*" ",0,0)
                  lcd.printString(16*" ",0,1)
