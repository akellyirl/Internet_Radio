import os
from nanpy import Arduino, Lcd

Arduino.pinMode(14, input)

lcd = Lcd([8,9,4,5,6,7],[16,2])

max_trax = 6

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


def getTrack():
   L= [S.strip('\n') for S in os.popen('mpc').readlines()]
   station = L[0][0:15]
   track = L[0][-16:-1]
   lcd.printString(16*" ", 0, 0)
   lcd.printString(station, 0, 0)
   lcd.printString(16*" ", 0, 1)
   lcd.printString(track, 0, 1)
   print L
   print station
   print track

track_num = 1
os.system("mpc play "+str(track_num))
getTrack()

while True:
   key = getKey()
   if key == "RIGHT":
      track_num += 1
      if track_num > max_trax:
         track_num = max_trax
      os.system("mpc play " + str(track_num))
      getTrack()
   elif key == "LEFT":
      track_num -= 1
      if track_num < 1:
         track_num = 1
      os.system("mpc play " + str(track_num))
      getTrack()
   elif key == "SEL":
      os.system("mpc toggle")
      getTrack()
