#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int64
import random

class Node():
    def __init__(self):
        rospy.init_node("integer_generator", anonymous=True)
        self.pub = rospy.Publisher('/integers',Int64,queue_size=10)
        self.r = rospy.Rate(15)
    def send(self):
        num = random.randint(1,100)
        self.pub.publish(num)
        self.r.sleep()
if __name__=="__main__":
    node=Node()
    while (not rospy.is_shutdown()):
        node.send()