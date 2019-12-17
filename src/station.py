#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import numpy as np
import random as rnd
from cybermans_psu.srv import PositionWant, PositionWantResponse
from cybermans_psu.srv import PositionWhere, PositionWhereResponse
from cybermans_psu.srv import PositionAround, PositionAroundResponse

robots = ['alpha', 'beta']  # имена нодов роботов

labirint = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
                     [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                     [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1],
                     [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
                     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
                     [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
                     [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
                     [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1],
                     [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
                     [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                     [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
                     [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])


def handle_want(req):
    res = check_rnd_pos(labirint, req.x_new, req.y_new)
    # print(res)
    if res:
        labirint[req.x_old, req.y_old] = 0
        labirint[req.x_new, req.y_new] = 2
        # print(labirint)
    return PositionWantResponse(res)


def handle_around(req):
    w = get_pos(req.x - 1, req.y)
    a = get_pos(req.x, req.y - 1)
    s = get_pos(req.x + 1, req.y)
    d = get_pos(req.x, req.y + 1)
    # print(w, a, s, d)
    return PositionAroundResponse(w, a, s, d)


def handle_get_rnd_pos(req):
    flag = True
    x, y = 0, 0
    while flag:
        x, y = rnd.randint(0, 16), rnd.randint(0, 16)
        if check_rnd_pos(labirint, x, y):
            flag = False
    return PositionWhereResponse(x, y)


def check_pos(x, y):
    return 0 <= x < 17 and 0 <= y < 17


def get_pos(x, y):
    if check_pos(x, y):
        return labirint[x, y]
    else:
        return -1


def check_rnd_pos(arr, x, y):
    return check_pos(x, y) and arr[x, y] == 0


def init_servers():
    print(labirint)

    s = rospy.Service('labirint', PositionWant, handle_want)
    rospy.loginfo("Start  server 'labirint'")

    s2 = rospy.Service('labirint_rnd_pos', PositionWhere, handle_get_rnd_pos)
    rospy.loginfo("Start  server 'labirint__rnd_pos'")

    s3 = rospy.Service('labirint_around', PositionAround, handle_around)
    rospy.loginfo("Start  server 'labirint_around'")


def get_robot_position():
    r = rospy.Rate(10)
    ser_list = []
    for robot in robots:
        ser_list.append([rospy.ServiceProxy(robot, PositionWhere), robot])
    while not rospy.is_shutdown():
        for pos in ser_list:
            try:
                resp = pos[0]()
                rospy.loginfo("%s telemetry x=%s,y=%s", pos[1], resp.x, resp.y)
            except rospy.ServiceException as e:
                rospy.loginfo("Service call failed: %s" % e)
                rospy.sleep(1)
        r.sleep()


def omega():
    rospy.init_node('omega')
    rospy.loginfo("Start 'omega' node")
    init_servers()
    get_robot_position()


if __name__ == "__main__":
    omega()
