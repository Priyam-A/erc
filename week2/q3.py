#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class Node():
    def __init__(self):
        rospy.init_node("go_straight", anonymous=True)
        self.sub=rospy.Subscriber('/scan',LaserScan,self.callback)
        self.pub = rospy.Publisher('/cmd_vel',Twist,queue_size=10)
        self.rate=15
        self.r = rospy.Rate(self.rate)
        self.data=LaserScan()
        self.data_received=False
        self.velx=0.05
        self.reached_dest=False
    def callback(self,data):
        self.data=data
        self.data_received=True
    def stop(self):
        vel=Twist()
        self.pub.publish(vel)
    def move(self):
        vel = Twist()
        vel.linear.x=self.velx
        self.pub.publish(vel)
        self.r.sleep()
    def send(self):
        if self.data_received:
            if (self.data.ranges[0]>0.5):
                self.move() 
            else:
                self.stop()
                self.reached_dest=True
            self.data_received=False
            
            
if __name__=="__main__":
    node=Node()
    while rospy.is_shutdown:
        node.send()
        if node.reached_dest:
            break