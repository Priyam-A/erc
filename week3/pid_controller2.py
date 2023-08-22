#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from math import atan2, sqrt
from tf.transformations import euler_from_quaternion

class TurtlebotPIDController:
    def __init__(self, goal_x, goal_y):
        rospy.init_node('turtlebot_pid_controller')
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.kp = 1  # Proportional constant
        self.ki = 0.0 # Integral constant
        self.kd = 0.5  # Derivative constant
        
        self.curr_x  = 0
        self.curr_y = 0

        self.data=Odometry()
        self.data_orient = self.data.pose.pose.orientation
        self.data_list = [self.data_orient.x,self.data_orient.y,self.data_orient.z,self.data_orient.w]
        self.received=False

        self.prev_error = 0.0
        self.integral = 0.0
        
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.odom_sub = rospy.Subscriber('/odom', Odometry, self.odom_callback)
        
    def odom_callback(self, msg):
        self.curr_x = msg.pose.pose.position.x
        self.curr_y = msg.pose.pose.position.y
        
        distance_to_goal = sqrt((self.goal_x - self.curr_x)**2 + (self.goal_y - self.curr_y)**2)
        curr_angle = euler_from_quaternion(self.data_list)[2] 
        angle_to_goal = atan2(self.goal_y - self.curr_y, self.goal_x - self.curr_x)

        self.data=msg
        self.data_orient = self.data.pose.pose.orientation
        self.data_list = [self.data_orient.x,self.data_orient.y,self.data_orient.z,self.data_orient.w]
        
        error = angle_to_goal-curr_angle
        self.integral += error
        derivative = error - self.prev_error
        
        control_signal = self.kp * error + self.ki * self.integral + self.kd * derivative
        
        self.prev_error = error
        
        twist_msg = Twist()
        twist_msg.linear.x = 0.2
        twist_msg.angular.z = control_signal
        
        self.cmd_vel_pub.publish(twist_msg)
        
        if distance_to_goal < 0.1:
            twist_msg.linear.x = 0.0
            twist_msg.angular.z = 0.0
            self.cmd_vel_pub.publish(twist_msg)
            rospy.loginfo("Goal reached!")
            rospy.signal_shutdown("Goal reached")

if __name__ == '__main__':
    goal_x = float(input("Enter the goal x-coordinate: "))
    goal_y = float(input("Enter the goal y-coordinate: "))
    
    controller = TurtlebotPIDController(goal_x, goal_y)
    rospy.spin()
