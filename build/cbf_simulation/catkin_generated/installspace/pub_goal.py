#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Point, PointStamped

def point_publisher():
    rospy.init_node('pub_goal', anonymous=True)
    robot_name = rospy.get_param('robot_name', 'default_robot')
    x = rospy.get_param('x', 0.0)
    y = rospy.get_param('y', 0.0)

    topic_name = '/' + robot_name + '/goal'
    pub = rospy.Publisher(topic_name, PointStamped, queue_size=10)

    point_msg = Point()
    point_msg.x = int(x)
    point_msg.y = int(y)
    point_msg.z = 0.0

    point_stamp = PointStamped()
    point_stamp.header.frame_id = 'map'

    rate = rospy.Rate(10)  # 10 Hz

    while not rospy.is_shutdown():
        point_stamp.header.stamp = rospy.Time.now()
        point_stamp.point = point_msg
        pub.publish(point_stamp)
        rospy.loginfo("Published goal point for {}: ({}, {})".format(robot_name, point_msg.x, point_msg.y))
        rate.sleep()

if __name__ == '__main__':
    try:
        point_publisher()
    except rospy.ROSInterruptException:
        pass
