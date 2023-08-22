#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int64,String

class Node():
    def __init__(self):
        rospy.init_node("odd_even_classifier", anonymous=True)
        self.sub = rospy.Subscriber('/integers',Int64,self.callback)
        self.pub = rospy.Publisher('/oddeven',String,queue_size=10)
        self.data = Int64()
        self.data_received = False
    def callback(self,data):
        self.data = data
        self.data_received=True
    def printInfo(self):
        if self.data_received:
            res=String()
            if (self.data.data%2==0):
                res="Even"
            else:
                res="Odd"
            self.pub.publish(res)
            rospy.loginfo("%d %s"%(self.data.data,res))
            self.data_received=False
if __name__=="__main__":
    node = Node()
    while not rospy.is_shutdown():
        node.printInfo()
