#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import argparse
import numpy as np
from cybermans_psu.srv import PositionWant
from cybermans_psu.srv import PositionWhere, PositionWhereResponse
from cybermans_psu.srv import PositionAround

x, y = 0, 0


def handle_where(req):
    return PositionWhereResponse(x, y)


def change_rnd_pos(pos_want, pos_around):
    around = pos_around(x, y)
    if around.w != 0 and around.a != 0 and around.s != 0 and around.d != 0:
        return x, y
    else:
        flag = True
        xx, yy = x, y
        while flag:
            way = np.random.choice(['w', 'a', 's', 'd'])
            if way == 'w' and around.w == 0:
                xx = x - 1
                flag = False
            elif way == 'a' and around.a == 0:
                yy = y - 1
                flag = False
            elif way == 's' and around.s == 0:
                xx = x + 1
                flag = False
            elif way == 'd' and around.d == 0:
                yy = y + 1
                flag = False
        # print(xx, yy)

        if pos_want(x, y, xx, yy).res:
            return xx, yy
        else:
            return x, y


def server(server_name):
    rospy.init_node(server_name)
    rospy.loginfo("Start '" + server_name + "' node")
    r = rospy.Rate(10)

    flag = True
    s = None
    while flag:
        try:
            rospy.loginfo("Wait server 'labirint_rnd_pos'")
            rospy.wait_for_service('labirint_rnd_pos')
            get_rnd_pos = rospy.ServiceProxy('labirint_rnd_pos', PositionWhere)
            global x, y
            rnd_pos = get_rnd_pos()
            x = rnd_pos.x
            y = rnd_pos.y

            rospy.loginfo("Wait server 'labirint'")
            rospy.wait_for_service('labirint')
            pos_want = rospy.ServiceProxy('labirint', PositionWant)

            rospy.loginfo("Wait server 'labirint_around'")
            rospy.wait_for_service('labirint_around')
            pos_around = rospy.ServiceProxy('labirint_around', PositionAround)

            if s is None:
                s = rospy.Service(server_name, PositionWhere, handle_where)
                rospy.loginfo("Start server '" + server_name + "'")

            while not rospy.is_shutdown():
                x, y = change_rnd_pos(pos_want, pos_around)
                rospy.loginfo("%s x=%s,y=%s", server_name, x, y)
                r.sleep()
            flag = False
        except rospy.ServiceException as e:
            rospy.loginfo("Service call failed: %s" % e)
            # s.shutdown('shutdown ' + server_name)
            rospy.sleep(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='server')
    parser.add_argument('server_name', type=str, help="Name of server")
    args = parser.parse_args()
    server(args.server_name)
