import serial
import time
import threading

arduino = serial.Serial('COM4', 115200, timeout=.001)
output = []

def get_vals(vals):
  values = vals.split('|')
  for x in range(0, len(values)):
    if values[x].isdigit():
      values[x] = int(values[x])
  return values

def request():
  threading.Timer(.01, request).start()
  if arduino.readline():
    values = get_vals(arduino.readline())
    if len(values) > 8:
      DF = values[0]
      DB = values[1]
      TR = values[2]
      TL = values[3]
      AU = values[4]
      AD = values[5]
      AR = values[6]
      AL = values[7]
      output = [DF, DB, TR, TL, AU, AD, AR, AL]
      print output
request()

 
  

