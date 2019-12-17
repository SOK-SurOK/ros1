#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from cybermans_psu.srv import Position

robots = ['alpha', 'beta']

def get_server_position():
    #rospy.wait_for_service('ser1')
    try:
        r = rospy.Rate(10)
        ser_list = []
        for robot in robots:
            ser_list.append([rospy.ServiceProxy(robot, Position), robot])
        while not rospy.is_shutdown():
            for pos in ser_list:
                resp = pos[0]()
                rospy.loginfo("%s telemetry x=%s,y=%s", pos[1], resp.x, resp.y)
            r.sleep()   
    except rospy.ServiceException, e:
        rospy.loginfo("Service call failed: %s"%e)

def client():
    rospy.init_node('client')
    rospy.loginfo("Start omega") 
    get_server_position()

if __name__ == "__main__":
    client()

