#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import numpy as np
import random as rnd
import argparse
from cybermans_psu.srv import PositionWant, PositionWantResponse
from cybermans_psu.srv import PositionWhere, PositionWhereResponse
from cybermans_psu.srv import PositionAround, PositionAroundResponse

robots = ['alpha', 'beta']  # имена нодов роботов
visual = None

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
    res = check_rnd_pos(labirint, req.i_new, req.j_new)
    # print(res)
    if res:
        labirint[req.i_old, req.j_old] = 0
        labirint[req.i_new, req.j_new] = 2
        if visual:
            print(labirint)
    return PositionWantResponse(res)


def handle_around(req):
    w = get_pos(req.i - 1, req.j)
    a = get_pos(req.i, req.j - 1)
    s = get_pos(req.i + 1, req.j)
    d = get_pos(req.i, req.j + 1)
    # print(w, a, s, d)
    return PositionAroundResponse(w, a, s, d)


def handle_get_rnd_pos(req):
    flag = True
    i, j = 0, 0
    while flag:
        i, j = rnd.randint(0, 16), rnd.randint(0, 16)
        if check_rnd_pos(labirint, i, j):
            flag = False
        labirint[i, j] = 2
        if visual:
            print(labirint)
    return PositionWhereResponse(i, j)


def check_pos(i, j):
    return 0 <= i < 17 and 0 <= j < 17


def get_pos(i, j):
    if check_pos(i, j):
        return labirint[i, j]
    else:
        return -1


def check_rnd_pos(arr, i, j):
    return check_pos(i, j) and arr[i, j] == 0


def init_servers():
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
        if visual:
            # print(labirint)
            pass
        else:
            for pos in ser_list:
                try:
                    resp = pos[0]()
                    rospy.loginfo("%s telemetry x=%s,y=%s", pos[1], resp.j, resp.i)
                except rospy.ServiceException as e:
                    rospy.loginfo("Service call failed: %s" % e)
                    rospy.sleep(1)
        r.sleep()


def omega():
    rospy.init_node('omega')
    rospy.loginfo("Start 'omega' node")
    print(labirint)
    rospy.sleep(1)
    init_servers()
    get_robot_position()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='station server')
    parser.add_argument('-v',  type=bool,  default=False,
                        help='V = True => massive output')
    args = parser.parse_args()
    visual = args.v
    omega()
