#!/usr/bin/python
import rospy

from baxter_pykdl import baxter_kinematics
import baxter_interface
import time
import numpy as np

import RobotRaconteur as RR
RRN = RR.RobotRaconteurNode.s



def main():
    t1 = RR.LocalTransport()
    RRN.RegisterTransport(t1)
    
    
    t2 = RR.TcpTransport()
    RRN.RegisterTransport(t2)
    
    myHeadBand = RRN.ConnectService('tcp://localhost:10002/headBandNode/headBandNode')
    
    rospy.init_node('baxter_kinematics')
    print '*** Baxter PyKDL Kinematics ***\n'
    kin = baxter_kinematics('right')

    # build jacobian
    jacobian=kin.jacobian()
    
    # create limb interface
    limb = baxter_interface.Limb('right')
    angles = limb.joint_angles()
    angles['right_s0']=0.0
    angles['right_s1']=0.0
    angles['right_e0']=0.0
    angles['right_e1']=0.0
    angles['right_w0']=0.0
    angles['right_w1']=0.0
    angles['right_w2']=0.0
    
    #angles are initialized
    start= time.time()
    # run for 2 seconds
    while time.time()-start < 5:
        jacobianInv=kin.jacobian_pseudo_inverse()
        
        
        # grab data from the head band
        data = myHeadBand.getData()
        upAngle = data[4]
        downAngle = data[5]
        
        upVelocity = (upAngle*1.0 - downAngle*1.0)/ 100.0
        
        # includes angular and linear velocities
        # desriedEndEffectorVelocities = np.array([Vx,Vy,Vz,Wx,Wy,Wz])
        desiredEndEffectorVelocities = np.array([[0],[0],[upVelocity],[0],[0],[0]])
        
        # q' = J(q)^-1*[Vx;Wx]
        jointVelocities = jacobianInv*desiredEndEffectorVelocities


        
        
        angles['right_s0']=jointVelocities[0]
        angles['right_s1']=jointVelocities[1]
        angles['right_e0']=jointVelocities[2]
        angles['right_e1']=jointVelocities[3]
        angles['right_w0']=jointVelocities[4]
        angles['right_w1']=jointVelocities[5]
        angles['right_w2']=jointVelocities[6]



        #print jointVelocities
        print jointVelocities
        limb.set_joint_velocities(angles)
        time.sleep(.1)



if __name__ == "__main__":
    main()
