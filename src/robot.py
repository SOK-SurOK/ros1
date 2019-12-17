#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import argparse
import numpy as np
import random as rnd
from cybermans_psu.srv import Position2, Position, PositionResponse

x, y = 0, 0
pos = None


def handle(req):
    return PositionResponse(x, y)


def get_rnd_pos():
    flag = True
    xx, yy = 0, 0
    while flag:
        xx, yy = rnd.randint(0, 16), rnd.randint(0, 16)
        if pos(xx, yy, xx, yy).res:
            flag = False
    return xx, yy


def change_rnd_pos():
    way = np.random.choice(['a', 'w', 's', 'd'])
    xx, yy = x, y
    if way == 'a':
        xx = x - 1
    elif way == 'w':
        yy = y - 1
    elif way == 's':
        yy = y + 1
    elif way == 'd':
        xx = x + 1

    if pos(x, y, xx, yy).res:
        return xx, yy
    else:
        return x, y


def server(server_name):
    rospy.init_node(server_name)
    rospy.loginfo("Start " + server_name)

    try:
        global pos
        pos = rospy.ServiceProxy('labirint', Position2)
        global x, y
        x, y = get_rnd_pos()

        r = rospy.Rate(10)

        s = rospy.Service(server_name, Position, handle)
        while not rospy.is_shutdown():
            x, y = change_rnd_pos()
            rospy.loginfo("%s x=%s,y=%s", server_name, x, y)
            r.sleep()
    except rospy.ServiceException, e:
        rospy.loginfo("Service call failed: %s" % e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='server')
    parser.add_argument('server_name', type=str, help="Name of server")
    args = parser.parse_args()
    server(args.server_name)
