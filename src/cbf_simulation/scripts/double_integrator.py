# Class definition for converting the cmd_vel input to double Integrator model

import rospy
from cbf_simulation.msg import state_msg
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import numpy as np


class DoubleIntegrator():

    def __init__(self, amin, amax, dt):
        self.amin= amin
        self.amax = amax
        self.dt = dt
        self.prev_state = state_msg()

    def pose_to_state(self):
        state = state_msg()
        self.prev_state=state
        return state
    
    def cmd_vel_update(self, ax, ay):
        cmd_vel = Twist()
        cmd_vel.x = self.prev_state.vx + self.dt*np.clip(ax, a_min=self.amin, a_max= self.amax)
        cmd_vel.y = self.prev_state.vy + self.dt*np.clip(ay, a_min=self.amin, a_max= self.amax)
        self.prev_cmd = cmd_vel
