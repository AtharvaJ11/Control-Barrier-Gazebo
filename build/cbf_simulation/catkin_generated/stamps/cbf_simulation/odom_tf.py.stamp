#!/usr/bin/env python3

import rospy
import tf
from nav_msgs.msg import Odometry

def handle_odom(msg, robot_name):
    br = tf.TransformBroadcaster()
    pose = msg.pose.pose
    odom_frame = robot_name + "/odom"
    baselink_frame = robot_name + "/base_footprint"
    br.sendTransform((pose.position.x, pose.position.y, 0),  # Fixed typo in position tuple
                     (pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w),
                     rospy.Time.now(),
                     baselink_frame,  # Changed the order of frames (from odom_frame to baselink_frame)
                     odom_frame)

if __name__ == '__main__':
    rospy.init_node('turtle_tf_broadcaster')
    robot_name = rospy.get_param('robot_name', 'default_robot')  # Access the parameter with the "~" prefix
    rospy.Subscriber('/%s/odom' % robot_name,
                     Odometry,
                     handle_odom,
                     robot_name)
    rospy.spin()