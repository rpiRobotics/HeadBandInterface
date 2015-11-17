import serial
import time
import threading
import RobotRaconteur as RR
import socket
import time
import sys
import signal

RRN = RR.RobotRaconteurNode.s


# catch control c to allow for use of the same port
def signal_handler(signal, frame):
        print('Ctrl+C shutdown!')
        RRN.Shutdown()
        sys.exit(0)

class HeadbandInterface(object):
    def __init__(self):
        self.arduino = serial.Serial('/dev/ttyACM1', 115200, timeout=.001)
        self.output = []

    # used to get an instance of data
    def get_vals(self, vals):
      values = vals.split('|')
      for x in range(0, len(values)):
        if values[x].isdigit():
          values[x] = int(values[x])
      return values

    # run this to start accumulating data
    def runUpdates(self):
      threading.Timer(.01, self.runUpdates).start()
      if self.arduino.readline():
        values = self.get_vals(self.arduino.readline())
        if len(values) > 8:
          DF = values[0]
          DB = values[1]
          TR = values[2]
          TL = values[3]
          AU = values[4]
          AD = values[5]
          AR = values[6]
          AL = values[7]
          self.output = [0.0, DB, TR, TL, AU, AD, AR, AL]
          
    def getData(self):
            print self.output
            return self.output
          
          

def main():

    port = 10002
    
        
    t1 = RR.LocalTransport()
    t1.StartServerAsNodeName("headBandNode")
    RRN.RegisterTransport(t1)

    t2 = RR.TcpTransport()
    t2.EnableNodeAnnounce()
    t2.StartServer(port)
    RRN.RegisterTransport(t2)

    with open('headBandServer.robodef', 'r') as f:
        service_def = f.read()
    
    myHeadBand = HeadbandInterface()
    myHeadBand.runUpdates()

    RRN.RegisterServiceType(service_def)
    RRN.RegisterService("headBandNode", "headBandNode.HeadbandInterface", myHeadBand)
    print "Conect string: tcp://localhost:" + str(port) + "/headBandNode/headBandNode"
    raw_input("Press any key to end")

    RRN.Shutdown()
  


if __name__ == '__main__':
    main()
 
  

