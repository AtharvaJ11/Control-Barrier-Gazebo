#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Point, Twist, PointStamped, Quaternion
from nav_msgs.msg import Odometry


import numpy as np 
import cvxpy as cp
import csv
import pandas as pd
import os
import tf2_ros 
from cbf_simulation.msg import cbf_data
import tf.transformations as tf


class DCBF():


    def __init__(self, swarm_size, id):

        self.alpha_i = 0.2
        self.alpha_j = 0.2
        self.gamma = 1.0
        self.swarm_size = swarm_size
        self.id = self.id


    def calculate_control(self, u_hat:np.ndarray):
        '''
        I have uhat using ux uy. I need to subscribe to other nexus odom for del_pij, del_vij.
        Subscribe to nexus(i)/odom for px, py(transform needed) and vx vy 
        '''

        self.robot_i = "nexus"+str(self.id)
        for k in range(1, self.swarm_size+1):
            if k!=self.id:
                self.robot_j = "nexus"+str(k)



    def get_dcbf(self, u_hat:np.ndarray, del_pij:np.ndarray, alpha_i:float, alpha_j:float, del_vij:np.ndarray, Ds:float, gamma:float):
        control = cp.Variable(2)  

        # dcbf constraint
        A = del_pij.T
        h_ij = np.sqrt(2*(alpha_i+alpha_j)*(np.linalg.norm(del_pij, ord=2)-Ds)) + (del_pij.T)@(del_vij)/np.linalg.norm(del_pij, ord=2)
        b = (alpha_i/(alpha_i+alpha_j))* (gamma* (h_ij**3)*np.linalg.norm(del_pij, ord=2) 
                                        - (del_vij.T@del_pij)/(np.linalg.norm(del_pij, ord=2)**2)
                                        + (alpha_i+alpha_j)*(del_vij.T@del_pij)/np.sqrt(2*(alpha_i+alpha_j)*(np.linalg.norm(del_pij, ord=2)-Ds))
                                        + np.linalg.norm(del_vij, ord=2)
                                        )

        # DCBF constraint
        dcbf_constraint = [ A@control <= b]


        # control limits constraints (infinity norm)
        control_limits_constraint = [control[i] >= -alpha_i for i in range(2)]
        control_limits_constraint += [control[i] <= alpha_i for i in range(2)]

        # Cost function to be minimized
        cost = cp.Minimize(cp.sum_squares(control - u_hat))

        # Optimization problem
        problem = cp.Problem(cost, 
                            dcbf_constraint +
                            control_limits_constraint )

        problem.solve()

        optimal_states = control.value
        print(control.value)

        return control.value




class ControlBot():
    def __init__(self, amin=-0.2, amax=0.2, dt=0.1):
        # Initialize the ROS node
        rospy.init_node('controller', anonymous=True)

        robot_name = rospy.get_param('robot_name', 'default_robot')
        cmd_vel_topic = '/' + robot_name + '/cmd_vel'
        self.pub = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
        self.log_pub = rospy.Publisher(robot_name+'/cbf', cbf_data, queue_size=10)

        self.sub_topic = "/" + robot_name + "/odom"
        self.goal_topic = "/" + robot_name + "/goal"
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)

        self.robot_name = robot_name
        self.robot_id = rospy.get_param('robot_id', 0)
        self.swarm_size = rospy.get_param('swarm_size', 2)

        self.amin = amin
        self.amax = amax
        self.dt = dt

        # Reference States
        self.x_ref = 0
        self.y_ref = 0
        self.vx_ref = 0
        self.vy_ref = 0

        self.kp = rospy.get_param('kp', 0.5)
        self.kv = 4 * np.sqrt(self.kp)

        # Initial variable
        self.x = 0.0
        self.y = 0.0
        self.vx = 0.0
        self.vy = 0.0

        self.odom_frame = self.robot_name + '/odom'

        try: 
            self.odom_to_map_transform  = self.tf_buffer.lookup_transform('map', self.odom_frame, rospy.Time(0), rospy.Duration(1.0))
            self.map_to_odom_transform= self.tf_buffer.lookup_transform(self.odom_frame,'map', rospy.Time(0), rospy.Duration(1.0))

        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            rospy.logwarn("Transform lookup failed: {}".format(e))

        _ = rospy.wait_for_message(self.goal_topic, PointStamped, timeout=10)
        rospy.Subscriber(self.goal_topic, PointStamped, self.goal_cb)
        _ = rospy.wait_for_message(self.sub_topic, Odometry, timeout=10)
        rospy.Subscriber(self.sub_topic, Odometry, self.odom_cb)
        




    def transform_point(self, x, y, transform_stamped):
        # Extract translation and rotation from TransformStamped
        translation = np.array([transform_stamped.transform.translation.x,
                                transform_stamped.transform.translation.y,
                                transform_stamped.transform.translation.z])
        rotation = np.array([transform_stamped.transform.rotation.x,
                            transform_stamped.transform.rotation.y,
                            transform_stamped.transform.rotation.z,
                            transform_stamped.transform.rotation.w])

        # Convert quaternion to rotation matrix
        rotation_matrix = tf.quaternion_matrix([rotation[0], rotation[1], rotation[2], rotation[3]])[:3, :3]

        # Create homogeneous point
        point_homogeneous = np.array([x, y, 0, 1])

        # Apply transformation
        transformed_point = np.dot(rotation_matrix, point_homogeneous[:3]) + translation

        return transformed_point[0], transformed_point[1]
    



    def goal_cb(self, ptstamp):
        self.x_ref, self.y_ref = self.transform_point(ptstamp.point.x, ptstamp.point.y, self.map_to_odom_transform)


    def run_control(self):
        rate = rospy.Rate(10)

        while not rospy.is_shutdown():
            
            rospy.Subscriber(self.sub_topic, Odometry, self.odom_cb)
            rospy.Subscriber(self.goal_topic, PointStamped, self.goal_cb)
            self.control_algo()
            self.log_cbf_data()
            rate.sleep()

    def control_algo(self):
        
        # PD control
        self.ux = self.kp * (self.x_ref - self.x) + self.kv * (self.vx_ref - self.vx)
        self.uy = self.kp * (self.y_ref - self.y) + self.kv * (self.vy_ref - self.vy)

        # Double Integrator Model
        self.ux = np.clip(self.ux, a_min=self.amin, a_max=self.amax)
        self.uy = np.clip(self.uy, a_min=self.amin, a_max=self.amax)



        self.cmd_x = self.vx + self.dt * self.ux
        self.cmd_y = self.vy + self.dt * self.uy

        cmd_vel = Twist()
        cmd_vel.linear.x = self.cmd_x
        cmd_vel.linear.y = self.cmd_y

        self.pub.publish(cmd_vel)

    def odom_cb(self, odom_msg):
        self.x = odom_msg.pose.pose.position.x
        self.y = odom_msg.pose.pose.position.y
        self.vx = odom_msg.twist.twist.linear.x
        self.vy = odom_msg.twist.twist.linear.y

        self.control_algo()
        

    def log_cbf_data(self):

        cbfd = cbf_data()
        cbfd.stamp = rospy.Time.now()
        cbfd.px, cbfd.py = self.transform_point(self.x, self.y, self.odom_to_map_transform)
        cbfd.vx = self.vx
        cbfd.vy = self.vy
        cbfd.ux = self.ux
        cbfd.uy = self.uy
        self.log_pub.publish(cbfd)





if __name__ == '__main__':
    try:
        cb = ControlBot()
        cb.run_control()
    except rospy.ROSInterruptException:
        pass




