# Control Barrier Functions for Multirobot Collision Avoidance

The project is an implementation of the following research paper. Li Wang, A. D. Ames, and M. Egerstedt, "Safety Barrier Certificates for Collisions-Free Multirobot Systems," IEEE Transactions on Robotics, vol. 33, no. 3, pp. 661-674, June 2017.

The project is written for ROS Noetic and works on the Gazebo Simulator. The project uses the nexus robot package developed by Robin Baran: https://github.com/RBinsonB/nexus_4wd_mecanum_simulator.git 

## Instructions for setting up the environment:

Before launching the simulation, make sure to execute the following command in all terminals to set up the environment:

```bash
$ mkdir catkin_ws && cd catkin_ws
$ git clone https://github.com/AtharvaJ11/Control-Barrier-Gazebo.git
$ catkin_make
```

```bash
$ source devel/setup.bash
```

Follow Simulation launch steps for Gazebo Simulation.


## Simulation Launch

In Terminal:
```bash
$ source devel/setup.bash
$ roslaunch cbf_simulation nexus_{swarm_size}.launch #Replace swarm_size with single, double or triple.
```

The nexus_multi.launch can be edited to create an environment with a swarm size greater than 3 by copying the code snippet mentioned in the launch file.
