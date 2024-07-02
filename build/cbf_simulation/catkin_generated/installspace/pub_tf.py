#!/usr/bin/env python3

import rospy
import tf



def handle_pose(robot_name, x, y, yaw):
    br = tf.TransformBroadcaster()
    odom_frame = robot_name+"/odom"
    br.sendTransform((x, y, 0),
                     tf.transformations.quaternion_from_euler(0, 0, yaw),
                     rospy.Time.now(),
                     odom_frame,
                     "map")





if __name__ == '__main__':
    rospy.init_node('map_tf_broadcaster')
    robot_name = rospy.get_param('robot_name', 'default_robot')
    pose_x = rospy.get_param('pose_x', 0.0)  
    pose_y = rospy.get_param('pose_y', 0.0)  
    pose_yaw = rospy.get_param('pose_yaw', 0.0)  
    rate = rospy.Rate(20)  # Reduced publishing rate to 10 Hz for demonstration
    while not rospy.is_shutdown():
        handle_pose(robot_name, pose_x, pose_y, pose_yaw)
        rate.sleep()
