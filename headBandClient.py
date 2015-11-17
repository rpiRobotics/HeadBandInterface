import RobotRaconteur as RR
import time
RRN = RR.RobotRaconteurNode.s

def main():
    t1 = RR.LocalTransport()
    RRN.RegisterTransport(t1)
    

    t2 = RR.TcpTransport()
    RRN.RegisterTransport(t2)

    myHeadBand = RRN.ConnectService('tcp://localhost:10002/headBandNode/headBandNode')
    
    while 1==1:
        time.sleep(.05)
        print myHeadBand.getData()

    
    RRN.Shutdown()
  

if __name__ == '__main__':
    main()
