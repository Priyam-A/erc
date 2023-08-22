#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist

class Node():
    def __init__(self):
        rospy.init_node("go_straight", anonymous=True)
        self.pub = rospy.Publisher('/cmd_vel',Twist,queue_size=10)
        self.r = rospy.Rate(15)
    def send(self):
        vel = Twist()
        vel.linear.x=0.2
        self.pub.publish(vel)
        self.r.sleep()
if __name__=="__main__":
    node=Node()
    while (not rospy.is_shutdown()):
        node.send()