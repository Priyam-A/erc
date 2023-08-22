#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist

class Node():
    def __init__(self):
        rospy.init_node("go_straight", anonymous=True)
        self.pub = rospy.Publisher('/cmd_vel',Twist,queue_size=10)
        self.rate=15
        self.r = rospy.Rate(self.rate)
        self.destination=1
        self.velx=0.2
    def stop(self):
        vel=Twist()
        self.pub.publish(vel)
    def move(self):
        vel = Twist()
        vel.linear.x=self.velx
        self.pub.publish(vel)
        self.r.sleep()
    def send(self):
        while not rospy.is_shutdown():
            for i in range(self.rate* int(self.destination/self.velx)):
                self.move() 
            else:
                self.stop()
                break
if __name__=="__main__":
    node=Node()
    node.send()