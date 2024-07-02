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
from cbf_simulation.msg import cbf_data, state_msg
import tf.transformations as tf

import numpy as np
import matplotlib.pyplot as plt
import time


class DCBF():


    def __init__(self):

        self.alpha_i = 0.2
        self.alpha_j = 0.2
        self.gamma = 1.0


    def get_dcbf(self, u_hat:np.ndarray, Alist, blist, alpha_i:float):
        control = cp.Variable(2)  

        dcbf_constraint =[]

        # DCBF constraint
        for i in range(len(Alist)):
            rospy.loginfo(f"DCBF: {Alist[i]}, {blist[i]}")
            dcbf_constraint += [ Alist[i]@control <= blist[i]]


        rospy.loginfo(dcbf_constraint)
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
        # Check for NaN values and replace with zeros
        # if np.isnan(optimal_states).any():
        #     optimal_states = np.zeros_like(optimal_states)

        # print(optimal_states)

        return optimal_states


    def get_Ab(self, del_pij:np.ndarray, alpha_i:float, alpha_j:float, del_vij:np.ndarray, Ds:float, gamma:float):

        # dcbf constraint

        rel_vij = (del_pij.T@del_vij)

        if rel_vij>0:
            return np.array([0.0,0.0]), 0.0

        A = -del_pij.T
        
        h_ij = np.sqrt(2*(alpha_i+alpha_j)*(np.linalg.norm(del_pij, ord=2)-Ds)) + (del_pij.T@del_vij)/np.linalg.norm(del_pij, ord=2)
        rospy.loginfo(h_ij)
        b = (alpha_i/(alpha_i+alpha_j)) * (gamma* (h_ij**3)*np.linalg.norm(del_pij, ord=2) 
                                        - (del_vij.T@del_pij)**2/(np.linalg.norm(del_pij, ord=2)**2)
                                        + (alpha_i+alpha_j)*(del_vij.T@del_pij)/np.sqrt(2*(alpha_i+alpha_j)*(np.linalg.norm(del_pij, ord=2)-Ds))
                                        + np.linalg.norm(del_vij, ord=2)**2
                                        )
        return A, b



    def plot_cvx_polytope(self, Alist, blist, unom, usafe, window_name="CVX Polytope"):
        # Start measuring execution time
        start_time = time.time()

        # Create a new figure with the specified window name
        plt.figure(window_name)

        d = np.linspace(-2, 2, 500)
        x, y = np.meshgrid(d, d)
        
        # Precompute mask
        mask = (y >= -0.2) & (y <= 0.2) & (x >= -0.2) & (x <= 0.2)

        for A, b in zip(Alist, blist):
            A = A.T
            eqn = (A[0] * x + A[1] * y <= b)
            mask &= eqn

        plt.clf()  # Clear the previous plot
        plt.imshow(mask.astype(int), extent=(x.min(), x.max(), y.min(), y.max()), origin="lower", cmap="Greys", alpha=0.3)
        plt.plot(unom[0], unom[1], marker='o', color="red")
        plt.plot(usafe[0], usafe[1], marker='o', color="green")
        plt.xlim(-0.2, 0.2)
        plt.ylim(-0.2, 0.2)
        plt.axhline(y=0, color='k')
        plt.axvline(x=0, color='k')
        plt.xlabel(r'$x$')
        plt.ylabel(r'$y$')

        # Pause to update the plot window
        plt.pause(0.2)

        # Calculate execution time
        end_time = time.time()
        execution_time = end_time - start_time
        rospy.loginfo(f"Execution time: {execution_time} seconds")

        # Return execution time
        return execution_time



# class FeasibleDCBF(DCBF):


#     def get_Ab(self, del_pij:np.ndarray, alpha_i:float, alpha_j:float, vi:np.ndarray,vj:np.ndarray, Ds:float, gamma:float):

        
#         if np.linalg.norm(vi ,ord=2)==0:
#             A=0
#         elif np.linalg.norm(vj, ord=2)==0:
#             A= -(del_pij.T@vj)*vj/(2*alpha_j* np.linalg.norm(vj, ord=2))-(np.linalg.norm(vj, ord=2))*(-del_pij)/(2*alpha_j* np.linalg.norm(vj, ord=2))

#         A = -del_pij.T
        
#         h_ij = np.sqrt(2*(alpha_i+alpha_j)*(np.linalg.norm(del_pij, ord=2)-Ds)) + (del_pij.T@del_vij)/np.linalg.norm(del_pij, ord=2)
#         rospy.loginfo(h_ij)
#         b = (alpha_i/(alpha_i+alpha_j)) * (gamma* (h_ij**3)*np.linalg.norm(del_pij, ord=2) 
#                                         - (del_vij.T@del_pij)**2/(np.linalg.norm(del_pij, ord=2)**2)
#                                         + (alpha_i+alpha_j)*(del_vij.T@del_pij)/np.sqrt(2*(alpha_i+alpha_j)*(np.linalg.norm(del_pij, ord=2)-Ds))
#                                         + np.linalg.norm(del_vij, ord=2)**2
#                                         )
#         return A, b

class ControlBot():
    def __init__(self, amax=0.2, dt=0.1):
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
        self.robot_id = rospy.get_param('robot_id', 1)
        self.swarm_size = rospy.get_param('swarm_size', 2)

        # State (p, v)
        self.state_pub = rospy.Publisher('/state', state_msg, queue_size=10)
        self.state = state_msg()
        self.state.id = self.robot_id
        self.swarm_state = {}

        # Control Limits
        self.amin = -amax
        self.amax = amax
        self.rate = 5
        self.dt = 0.2

        # Reference States
        self.x_ref = 0
        self.y_ref = 0
        self.vx_ref = 0
        self.vy_ref = 0

        self.kp = rospy.get_param('kp', 0.5)
        self.kv = 3 * np.sqrt(self.kp)

        # Initial variable
        self.x = 0.0
        self.y = 0.0
        self.vx = 0.0
        self.vy = 0.0

        self.xmap = 0.0
        self.ymap = 0.0
        self.vxmap = 0.0
        self.vymap = 0.0

        self.odom_frame = self.robot_name + '/odom'
        self.base_frame = self.robot_name + '/base_footprint'

        # DCBF Params
        self.dcbf = DCBF()
        self.alpha_i = self.amax
        self.alpha_j = self.amax
        self.gamma = 0.1
        self.Ds = 1.0


        try: 
            self.odom_to_map_transform = self.tf_buffer.lookup_transform('map', self.odom_frame, rospy.Time(0), rospy.Duration(1.0))
            self.map_to_odom_transform = self.tf_buffer.lookup_transform(self.odom_frame, 'map', rospy.Time(0), rospy.Duration(1.0))
            self.base_to_map_transform = self.tf_buffer.lookup_transform('map', self.base_frame, rospy.Time(0), rospy.Duration(1.0))
            self.map_to_base_transform = self.tf_buffer.lookup_transform(self.base_frame, 'map', rospy.Time(0), rospy.Duration(1.0))

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
    

    def transform_velocity(self, x, y, transform_stamped):
        # Extract rotation from TransformStamped
        rotation = np.array([transform_stamped.transform.rotation.x,
                            transform_stamped.transform.rotation.y,
                            transform_stamped.transform.rotation.z,
                            transform_stamped.transform.rotation.w])

        # Convert quaternion to rotation matrix
        rotation_matrix = tf.quaternion_matrix([rotation[0], rotation[1], rotation[2], rotation[3]])[:3, :3]

        # Create homogeneous point
        point_homogeneous = np.array([x, y, 0, 1])

        # Apply transformation
        transformed_point = np.dot(rotation_matrix, point_homogeneous[:3])

        return transformed_point[0], transformed_point[1]
    


    def goal_cb(self, ptstamp):
        # self.x_ref, self.y_ref = self.transform_point(ptstamp.point.x, ptstamp.point.y, self.map_to_odom_transform)
        self.x_ref = ptstamp.point.x
        self.y_ref = ptstamp.point.y


    def state_cb(self, state_msg):
        self.swarm_state[state_msg.id]=[state_msg.x, state_msg.y, state_msg.vx, state_msg.vy]


    def run_control(self):
        rate = rospy.Rate(self.rate)

        while not rospy.is_shutdown():
            try: 
                self.base_to_map_transform = self.tf_buffer.lookup_transform('map', self.base_frame, rospy.Time(0), rospy.Duration(1.0))
                self.map_to_base_transform = self.tf_buffer.lookup_transform(self.base_frame, 'map', rospy.Time(0), rospy.Duration(1.0))

            except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
                rospy.logwarn("Transform lookup failed: {}".format(e))

            rospy.Subscriber(self.sub_topic, Odometry, self.odom_cb)
            rospy.Subscriber(self.goal_topic, PointStamped, self.goal_cb)
            rospy.Subscriber("/state", state_msg, self.state_cb)

            # vector1 =np.array([self.xmap, self.ymap, self.vxmap, self.vymap])
            # vector2 =np.array([self.x_ref, self.y_ref, self.vx_ref, self.vy_ref])
            # rospy.loginfo(vector1)
            # rospy.loginfo(vector2)
            # goal_dist = np.linalg.norm(vector1 - vector2, ord=2)
            # rospy.loginfo(f"GOal Dist {goal_dist}")
            # if goal_dist<=0.02:
            #     cmd_vel = Twist()
            #     self.pub.publish(cmd_vel)
            #     break

            self.control_algo()
            # self.log_cbf_data()
            rate.sleep()


    def calc_dcbf(self, uhat):
        AList = []
        bList = []
        rospy.loginfo(len(self.swarm_state))
        for id, state in self.swarm_state.items():
            if id!=self.robot_id:
                xj, yj, vxj, vyj = state
                del_pij = np.array([self.xmap-xj, self.ymap-yj])
                del_vij = np.array([self.vxmap-vxj, self.vymap-vyj])
                Aj, bj = self.dcbf.get_Ab(del_pij=del_pij, del_vij=del_vij, alpha_i=self.alpha_i, alpha_j=self.alpha_j, gamma=self.gamma, Ds=self.Ds)
                AList.append(Aj)
                bList.append(bj)
        
        rospy.loginfo(f"{self.robot_id} Alist: {AList}")
        rospy.loginfo(f"{self.robot_id} blist: {bList}")
        u_safe = self.dcbf.get_dcbf(u_hat=uhat, Alist=AList, blist=bList, alpha_i=self.alpha_i)
        # if np.linalg.norm(u_safe, ord=2)<=0.01:
        self.dcbf.plot_cvx_polytope(AList, bList, uhat, u_safe, f"{self.robot_name}")   
        

        return u_safe[0], u_safe[1]



    def control_algo(self):
        # PD control
        # The controls are in Map frame (Which makes zero sense btw)
        # rospy.loginfo(f"Goal: [{self.x_ref:.2f}, {self.y_ref:.2f}], Pos: [{self.x:.2f}, {self.y:.2f}], Velocity: [{self.vx:.2f}, {self.vy:.2f}]")
        self.ux = self.kp * (self.x_ref - self.xmap) + self.kv * (self.vx_ref - self.vxmap)
        self.uy = self.kp * (self.y_ref - self.ymap) + self.kv * (self.vy_ref - self.vymap)


        '''
        Removing this part to clip the control.
        '''
        # Double Integrator Model
        # self.ux = np.clip(self.ux, a_min=self.amin, a_max=self.amax)
        # self.uy = np.clip(self.uy, a_min=self.amin, a_max=self.amax)

        # rospy.loginfo(f"Map frame Control: [{self.ux:.2f}, {self.uy:.2f}]")

        # Transform controls (analogous to velocity) from map frame to robot frame (base footprint)
        u_hat = np.array([self.ux, self.uy])
        # rospy.loginfo(f"Nominal Control: {u_hat}")

        # Calculate DCBF control
        self.ux_nom = self.ux.copy()
        self.uy_nom = self.uy.copy()
        self.ux_nom, self.uy_nom = self.transform_velocity(self.ux_nom, self.uy_nom, self.map_to_base_transform)
        self.ux, self.uy = self.calc_dcbf(u_hat)


        rospy.loginfo(f"Nominal Control: {u_hat}, Safe Control: {self.ux, self.uy}")
        self.ux, self.uy = self.transform_velocity(self.ux, self.uy, self.map_to_base_transform)

        self.vx_bot, self.vy_bot = self.transform_velocity(self.vx, self.vy, self.map_to_base_transform)
        # rospy.loginfo(f"Bot vel: {self.vx_bot:.2f}, {self.vy_bot:.2f}")
        # rospy.loginfo(f"State:{self.swarm_state}")

        self.cmd_x = self.vx_bot + self.dt * self.ux
        self.cmd_y = self.vy_bot + self.dt * self.uy

        cmd_vel = Twist()
        cmd_vel.linear.x = self.cmd_x
        cmd_vel.linear.y = self.cmd_y
        rospy.loginfo(f"Cmd vel: {self.cmd_x:.2f}, {self.cmd_y:.2f}")

        self.pub.publish(cmd_vel)





    def odom_cb(self, odom_msg):
        # rospy.loginfo(odom_msg.header.seq)
        self.x = odom_msg.pose.pose.position.x
        self.y = odom_msg.pose.pose.position.y
        self.vx = odom_msg.twist.twist.linear.x
        self.vy = odom_msg.twist.twist.linear.y
        # convert from odom frame to map frame
        self.xmap, self.ymap = self.transform_point(self.x, self.y, self.odom_to_map_transform)
        self.vxmap, self.vymap = self.transform_velocity(self.vx, self.vy, self.odom_to_map_transform)

        # State update
        self.state.x = self.xmap
        self.state.y = self.ymap
        self.state.vx = self.vxmap
        self.state.vy = self.vymap
        self.state_pub.publish(self.state)
        

    def log_cbf_data(self):
        self.cbf_msg = cbf_data()
        self.cbf_msg.stamp = rospy.Time.now()
        self.cbf_msg.px = self.xmap
        self.cbf_msg.py = self.ymap
        self.cbf_msg.vx = self.vxmap
        self.cbf_msg.vy = self.vymap
        self.cbf_msg.ux_nom = self.ux_nom
        self.cbf_msg.uy_nom = self.uy_nom
        self.cbf_msg.ux_safe = self.ux
        self.cbf_msg.uy_safe = self.uy
        self.log_pub.publish(self.cbf_msg)


if __name__ == '__main__':
    try:
        cb = ControlBot()
        cb.run_control()
    except rospy.ROSInterruptException:
        pass


