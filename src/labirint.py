#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import numpy as np
import random as rnd
from cybermans_psu.srv import Position2, Position2Response

def handle(req):
    # req.xx, req.yy, req.x, req.y
    res = check_rnd_pos(labirint, req.x, req.y)
    if res:
        labirint[ req.xx,  req.yy] = 0
        labirint[ req.x,  req.y] = 2
        print(labirint)
    return Position2Response(res)

def check_rnd_pos(arr, x, y):
    #print(x, y)
    if x>=0 and x<17 and y>=0 and y<17 and arr[x, y]==0:
        return True
    else:
        return False

def server(server_name):
    rospy.init_node(server_name)
    rospy.loginfo("Start "+server_name)
    global labirint 
    # labirint = np.random.randint(0, 2, (17, 17))
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
    print(labirint)
    s = rospy.Service(server_name, Position2, handle)
    rospy.spin()

if __name__ == "__main__":
    server('labirint')
