#!/usr/bin/env python3


#necessary imports here , follow basic Ros2 node stuff
import rclpy
from rclpy.node import Node

import py_trees as pt #, py_trees_ros as ptr, rospy
from irob_assignment_5.reactive_sequence import RSequence

#import necessary services below
#from somewhere import XX{get goal}, {activtion service}, {deactivtion service}, {Check at Goal service} 
from irob_interfaces.srv import Activate, AtGoal, Deactivate, GetGoal

# IMPORT necessary messages, you need to use cmd_vel and more
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool
from nav_msgs.msg import Odometry
from action_msgs.msg import GoalStatus

# Should we use these?
from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import PoseStamped, Point, PointStamped, PoseWithCovarianceStamped
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient

import tf2_ros
from tf2_ros import TransformException

# import necessary sensory messages if needed:
import math
from math import atan2, sqrt, pow
import time
import numpy as np


class BTStudentsNode(Node):
    def __init__(self):
        super().__init__('BT_students_node')
                
        # Shared State variables for BT
        # The shared memory should contain only information that multiple behaviours need to share
        self.shared_memory = pt.blackboard.Blackboard()
        self.shared_memory.current_goal = None
        self.shared_memory.current_pose = None
        self.shared_memory.localized = False

        self.last_goal = (None, None) # to store the last (i.e., previous) goal point received from the service, to compare with new ones and ignore duplicates
        
        self.current_pose = None
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)

        # Nav2
        # We define the action client here as one client for whole system to use, to avoid multiple clients sending goals and interfering with each other. This way we can centralize goal sending and have better control over navigation state.
        self.navigate_ac = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        # Build BT
        self.tree = self.create_tree()

        # Tick BT
        self.timer = self.create_timer(0.1, self.tick_tree)

        self.get_logger().info("Behavior Tree running.")
        
    def odom_callback(self, msg):
        self.current_pose = msg.pose.pose
        self.shared_memory.current_pose = self.current_pose

    # Behavior Tree
    def create_tree(self):
 
        root = pt.composites.Sequence(name="MainSequence", memory=False)

        activate_robot_selector = pt.composites.Selector("Selector for activating the robot", memory=False)
        check_robot_active = CheckRobotActive(self)
        request_activation = ActivateBehaviour(self)
        activate_robot_selector.add_children([
            check_robot_active, 
            request_activation
        ])

        localization_selector = pt.composites.Selector("Selector for checking localization", memory=False)
        check_localization = CheckLocalization(self)
        initialize_localization = InitializeLocalization(self)
        localization_selector.add_children([
            check_localization,
            initialize_localization            
        ])

        get_goal_selector = pt.composites.Selector("Selector for aquiriing a new goal", memory=False)
        detect_new_goal = DetectNewGoal(self)
        is_goal_available = IsGoalAvailable(self)
        acquire_goal = AcquireGoal(self)
        get_goal_selector.add_children([
            detect_new_goal,
            is_goal_available,
            acquire_goal
        ])
                
        validate_goal = ValidateGoal(self)
        
        navigate_to_goal = NavigateToGoal(self, self.navigate_ac)
        
        precision_align_towards_goal = PrecisionAlign(self)
        
        verify_at_goal = VerifyAtGoal(self)
        
        deactivate_robot = DeactivateBehaviour(self)
        
        root.add_children([
            activate_robot_selector,
            localization_selector,
            get_goal_selector,
            validate_goal,
            navigate_to_goal,
            precision_align_towards_goal,
            verify_at_goal,
            deactivate_robot
        ])

        return pt.trees.BehaviourTree(root)

    def tick_tree(self):
        self.tree.tick()
        
        
def is_same_goal(g1, g2, tol=0.05):
    if g1 is None or g2 is None:
        return False
    if None in g1 or None in g2:
        return False
    return abs(g1[0] - g2[0]) < tol and abs(g1[1] - g2[1]) < tol


class CheckRobotActive(pt.behaviour.Behaviour):
    def __init__(self, node):
        super().__init__("Is robot active?")
        self.node = node
        self.robot_active = None

        self.node.create_subscription(Bool, '/robot_active', self.robot_active_callback, 10)

    def robot_active_callback(self, msg):
        self.robot_active = msg.data

    def update(self):
        if self.robot_active is None:
            self.node.get_logger().info("Waiting for robot active state from topic...")
            return pt.common.Status.RUNNING
        
        return pt.common.Status.SUCCESS if self.robot_active else pt.common.Status.FAILURE
 

class ActivateBehaviour(pt.behaviour.Behaviour):
    def __init__(self, node):
        super().__init__("Activate Robot")
        self.node = node
        self.activate_sent = False
        self.isRobotActive = False
        self.activate_client = self.node.create_client(Activate, '/activate')
        self.shared_memory = self.node.shared_memory
        
    def initialise(self):
        # self.activate_sent = False # We want to keep this True to keep the robot active, and only set it to False when we receive a deactivation request.
                                     # Basically, we don't need to resend the activation request multiple times, we just want to keep the robot active until we receive a deactivation request.
        self.isRobotActive = False

    def activate_response_callback(self, future):
        res = future.result()
        if res.success:
            self.node.get_logger().info("Robot activated successfully.")
            self.isRobotActive = True
            self.shared_memory.active = True # this variable is not used anywhere currently
        else:
            self.node.get_logger().warn("Failed to activate robot.")

    def update(self):
        if not self.activate_sent:
            self.node.get_logger().info("Activating robot...")
            req = Activate.Request()
            self.activate_client.wait_for_service()
            future = self.activate_client.call_async(req)
            future.add_done_callback(self.activate_response_callback)
            self.activate_sent = True

        if self.isRobotActive:
            self.node.get_logger().info("Robot activated")
            return pt.common.Status.SUCCESS
        else:
            return pt.common.Status.RUNNING


class CheckLocalization(pt.behaviour.Behaviour):
    def __init__(self, node):
        super().__init__("Check If Robot is Localized")
        self.node = node        
        self.covariance = None
        self.node.create_subscription(PoseWithCovarianceStamped, '/amcl_pose', self.localization_callback, 10)
        self.shared_memory = self.node.shared_memory

    def localization_callback(self, msg):
        # Check the covariance to determine if we are localized
        self.node.get_logger().info(f"Received AMCL pose with covariance")
        self.covariance = msg.pose.covariance

    def update(self):
        if self.shared_memory.localized:
            self.node.get_logger().info("Robot is already localized → returning success")
            return pt.common.Status.SUCCESS

        if self.covariance is None:
            self.node.get_logger().info("Waiting for AMCL pose message from /amcl_pose topic...")
            return pt.common.Status.RUNNING
        
        cov_norm = np.linalg.norm(np.array(self.covariance))  # L2 euclidian norm
        if cov_norm < 0.065: # Check if the overall covariance is low enough to consider the robot localized
            self.node.get_logger().info("Covariance is low enough, robot is localized.")
            self.node.get_logger().info(f"Covariance value: {cov_norm}")
            self.shared_memory.localized = True
            return pt.common.Status.SUCCESS
        else:
            self.node.get_logger().warn("Covariance is too high, robot is NOT localized!")
            self.node.get_logger().warn(f"Covariance value: {cov_norm}")
            self.shared_memory.localized = False
            return pt.common.Status.FAILURE 


class InitializeLocalization(pt.behaviour.Behaviour):
    def __init__(self, node):
        super().__init__("Initialize Localization")
        self.node = node
        self.cmd_publisher = self.node.create_publisher(Twist, '/cmd_vel', 10)
        self.init_sent = False
        self.shared_memory = self.node.shared_memory

    def stop_robot(self):
        msg = Twist()
        self.cmd_publisher.publish(msg)

    def rotate_robot(self):
        msg = Twist()
        msg.angular.z = 0.4
        self.cmd_publisher.publish(msg)

    def update(self):
        if self.shared_memory.localized:
            self.node.get_logger().info("Robot is already localized → no need to initialize, stopping robot and returning success")
            self.stop_robot()
            return pt.common.Status.SUCCESS
                    
        self.node.get_logger().info("Waiting for localization to complete...")
        self.rotate_robot()
        return pt.common.Status.RUNNING


class DetectNewGoal(pt.behaviour.Behaviour): # detect for new external goal received from topic
    def __init__(self, node):
        super().__init__("Detecting New Goal Point From Topic")
        self.node = node
        self.shared_memory = self.node.shared_memory # we store the current goal on the blackboard (shared memory), so that it can be accessed by other behaviours without needing to subscribe to the topic multiple times
        self.new_goal = None

        self.node.create_subscription(PointStamped, '/goal_point', self.last_goal_callback, 10)
  
    def last_goal_callback(self, msg):
        self.node.get_logger().warn(f"Detecting new goal point from TOPIC: ({msg.point.x}, {msg.point.y})")
        self.new_goal = (msg.point.x, msg.point.y)

    def update(self):
        self.node.get_logger().info("Checking for detected new goal point from TOPIC...")
        
        if self.new_goal is None and self.shared_memory.current_goal is not None:
            self.node.get_logger().warn("No new goal detected from TOPIC, but we have a currently existing goal → do nothing")
            return pt.common.Status.RUNNING
        
        if self.new_goal is None and self.shared_memory.current_goal is None:
            self.node.get_logger().info("No new or currently existing goal detected yet.")
            return pt.common.Status.FAILURE

        if self.shared_memory.current_goal is None:
            self.node.get_logger().info("We don't have a currently existing goal from service yet.")
            return pt.common.Status.FAILURE

        if not is_same_goal(self.new_goal, self.shared_memory.current_goal):
            self.node.get_logger().info("HOORAY! New goal from TOPIC detected → updating shared memory")
            self.shared_memory.current_goal = self.new_goal
            return pt.common.Status.SUCCESS
        else:
            self.node.get_logger().info("New goal from TOPIC detected, but it's the same as currently existing one → ignoring")
            return pt.common.Status.FAILURE
        

class IsGoalAvailable(pt.behaviour.Behaviour):
    def __init__(self, node):
        super().__init__("Is Goal Available?")
        self.node = node
        self.shared_memory = self.node.shared_memory
        
    def update(self):        
        if self.shared_memory.current_goal is not None:
            self.node.get_logger().info(f"The current goal exists (on shared memory): {self.shared_memory.current_goal}")
            return pt.common.Status.SUCCESS 
        else:
            self.node.get_logger().info("No current goal exists (on shared memory) yet")
            return pt.common.Status.FAILURE
    
    
class AcquireGoal(pt.behaviour.Behaviour):
    def __init__(self, node):
        super().__init__("Requesting New Goal Point from Service")
        self.node = node
        self.goal_req_sent = False
        self.goal_point = None
        self.last_goal_point = None
        self.shared_memory = self.node.shared_memory
        self.get_goal_client = self.node.create_client(GetGoal, '/get_goal')
        
    def initialise(self):
        self.goal_req_sent = False
        self.last_goal_point = (self.node.last_goal[0], self.node.last_goal[1]) 

    def goal_response_callback(self, future):
        res = future.result()
        if res is not None:
            self.node.get_logger().info(f"Receiving a new goal point from service: ({res.goal_x}, {res.goal_y})")
            self.goal_point = (res.goal_x, res.goal_y)
        else:
            self.node.get_logger().warn("Failed to get a new goal point from service.")

    def update(self):
        self.node.get_logger().info("Checking for new goal point from service...")
        
        if not self.goal_req_sent:
            self.node.get_logger().info("Requesting a new goal point from service...")
            req = GetGoal.Request()
            self.get_goal_client.wait_for_service()
            future = self.get_goal_client.call_async(req)
            future.add_done_callback(self.goal_response_callback)
            self.goal_req_sent = True
            
        if self.goal_point is None:
            self.node.get_logger().info("Waiting for new goal point from service...")
            return pt.common.Status.RUNNING # Here the goal_selector stops ticking further children (if any). It runs again from FIRST child (DetectNewGoal)
                                            # Even though AcquireGoal was RUNNING:
                                            # On next tick, the goal Selector does NOT resume it directly
                                            # It starts again from the top of the tree

        if self.last_goal_point is not None and is_same_goal(self.goal_point, self.last_goal_point):
            self.node.get_logger().info("The received new goal from service is the same as the last/previous one → ignoring")
            return pt.common.Status.FAILURE
        else:
            self.node.get_logger().info("HOORAY! Received new goal from service → updating shared memory")
            self.shared_memory.current_goal = (self.goal_point[0], self.goal_point[1])
            self.node.last_goal = (self.goal_point[0], self.goal_point[1])
            return pt.common.Status.SUCCESS


class ValidateGoal(pt.behaviour.Behaviour): # Confirm/Validate if the goal is in an obstacle or not, by checking the map data. 
    def __init__(self, node):
        super().__init__("Validate Goal Point")
        self.node = node
        self.node.create_subscription(OccupancyGrid, '/map', self.map_callback, 10)
        self.shared_memory = self.node.shared_memory
        self.map_data = None
    
    def map_callback(self, msg):
        self.node.get_logger().info(f"Receiving a new map from topic.")
        self.map_data = msg
        
    def is_goal_in_obstacle(self, goal_x, goal_y, radius_cells=1):
        """
        Returns True if the goal is:
        - outside map bounds
        - in an occupied cell
        - in an unknown cell
        - too close to occupied/unknown cells in a small neighborhood
        """
        resolution = self.map_data.info.resolution
        origin_x = self.map_data.info.origin.position.x
        origin_y = self.map_data.info.origin.position.y
        width = self.map_data.info.width
        height = self.map_data.info.height

        col = int((goal_x - origin_x) / resolution)
        row = int((goal_y - origin_y) / resolution)

        if row < 0 or row >= height or col < 0 or col >= width:
            self.node.get_logger().warn("The current goal is outside map bounds.")
            return True

        map_array = np.array(self.map_data.data).reshape((height, width))
        
        for r in range(row - radius_cells, row + radius_cells + 1):
            for c in range(col - radius_cells, col + radius_cells + 1):
                cell_value = map_array[r, c]
                if cell_value == 100 or cell_value == -1: # unknown or occupied
                    self.node.get_logger().warn(f"The current goal is invalid: blocked/unknown near row={r}, col={c}, value={cell_value}")
                    return True

        return False

    def update(self):
        self.node.get_logger().info("Checking if current goal in shared memory is in obstacle...")
        
        if self.shared_memory.current_goal is None:
            self.node.get_logger().info("No current goal is stored in shared memory.")
            return pt.common.Status.FAILURE
                
        if self.map_data is None:
            self.node.get_logger().info("Waiting for map data from topic...")
            return pt.common.Status.RUNNING
        
        self.node.get_logger().info(f"The current goal to validate: {self.shared_memory.current_goal}")
        
        if self.is_goal_in_obstacle(self.shared_memory.current_goal[0], self.shared_memory.current_goal[1]):
            self.node.get_logger().warn(f"The current goal is in an obstacle → removing it from shared memory")
            self.shared_memory.current_goal = None
            return pt.common.Status.FAILURE
        else:
            self.node.get_logger().info(f"The current goal is free.")
            return pt.common.Status.SUCCESS


class NavigateToGoal(pt.behaviour.Behaviour):
    def __init__(self, node, navigate_ac):
        super().__init__("Navigate To Goal")
        self.node = node
        self.navigate_ac = navigate_ac
        self.shared_memory = self.node.shared_memory
        self.nav_goal_sent = False
        self.nav_result_received = False
                
    def send_nav_goal(self, x, y):
        goal_msg = PoseStamped()
        goal_msg.header.frame_id = "map"
        goal_msg.header.stamp = self.node.get_clock().now().to_msg()
        goal_msg.pose.position.x = x
        goal_msg.pose.position.y = y
        goal_msg.pose.orientation.w = 1.0

        navigate_goal = NavigateToPose.Goal()
        navigate_goal.pose = goal_msg

        self.navigate_ac.wait_for_server()
        self.node.get_logger().info(f"Sending goal to navigate to: ({x}, {y})")
        nav_send_future = self.navigate_ac.send_goal_async(navigate_goal)
        nav_send_future.add_done_callback(self.goal_response_callback)
        
        self.nav_goal_sent = True

    def goal_response_callback(self, future):
        nav_goal_handle = future.result()
        
        if not nav_goal_handle.accepted:
            self.node.get_logger().warn("Navigation goal was rejected by the action server.")
            self.nav_goal_sent = False
            return
        
        self.node.get_logger().info("Navigation goal accepted by the action server.")
        nav_result_future = nav_goal_handle.get_result_async()
        nav_result_future.add_done_callback(self.navigation_complete_callback)

    def navigation_complete_callback(self, future):
        goal_result = future.result()
        status = goal_result.status

        self.node.get_logger().info(f"Received navigation result with STATUS: {status}")

        if status == GoalStatus.STATUS_SUCCEEDED: # == 4: means succeeded
            self.node.get_logger().info("NAVIGATION SUCCESS.")
            self.nav_result_received = True
        else: # status 6 means aborted, 5 means rejected
            self.node.get_logger().warn(f"NAVIGATION FAILED.")
            self.nav_goal_sent = False # Allow sending a new goal on next tick
    
    def update(self):               
        # send navigation goal if we haven't sent it yet
        if not self.nav_goal_sent:
            self.node.get_logger().info("Sending navigation-to-goal request now...")
            self.send_nav_goal(self.shared_memory.current_goal[0], self.shared_memory.current_goal[1])
            return pt.common.Status.RUNNING
        
        # wait for navigation to finish
        if not self.nav_result_received:
            self.node.get_logger().info("Navigation-to-goal in progress...")
            return pt.common.Status.RUNNING
        
        self.node.get_logger().info("Navigation-to-goal is complete → success")
        return pt.common.Status.SUCCESS


class PrecisionAlign(pt.behaviour.Behaviour):
    def __init__(self, node):
        super().__init__("PrecisionAlign")
        self.node = node
        self.shared_memory = self.node.shared_memory
        self.cmd_vel_pub = self.node.create_publisher(Twist, '/cmd_vel', 10)
        self.tolerance = 0.05
        
    def stop_robot(self):
        msg = Twist()
        self.cmd_vel_pub.publish(msg)

    def get_yaw(self, q):
        """Returns the Euler yaw from a quaternion.
        :type q: Quaternion
        """
        return atan2(2 * (q.w * q.z + q.x * q.y), 1 - 2 * (q.y * q.y + q.z * q.z))
    
    def wrap_to_pi(self, angle): # aka normalize angle, make sure the angle is between -pi and pi
        """Wraps an angle in radians to [-pi, pi].
        :type angle: float
        """
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        return angle

    # Integration of precision controller after Nav2 reports success, to drive the robot to exact center of goal pose
    def update(self):
        self.node.get_logger().info("Running precision alignment behaviour...")

        goal = self.shared_memory.current_goal
        pose = self.shared_memory.current_pose

        if goal is None or pose is None:
            self.node.get_logger().warn("Cannot do precision alignment → missing goal or pose")
            return pt.common.Status.FAILURE
        
        goal_x, goal_y = goal

        x = pose.position.x
        y = pose.position.y
        yaw = self.get_yaw(pose.orientation)

        dx = goal_x - x
        dy = goal_y - y

        distance = math.sqrt(dx**2 + dy**2)
        
        self.node.get_logger().info(f"Distance to goal: {distance:.4f}")

        # stop condition (CENTERED)
        if distance < self.tolerance:
            self.stop_robot()
            self.node.get_logger().info("HOORAY! Stopping robot, precision alignment complete!")
            return pt.common.Status.SUCCESS

        cmd = Twist()

        # rotate toward goal first
        target_angle = math.atan2(dy, dx)
        angle_error = self.wrap_to_pi(target_angle - yaw)

        if abs(angle_error) > 0.1:
            cmd.angular.z = 0.8 * angle_error
        else:
            cmd.linear.x = min(0.05, 0.5 * distance)

        self.cmd_vel_pub.publish(cmd)
        return pt.common.Status.RUNNING        


class VerifyAtGoal(pt.behaviour.Behaviour):
    def __init__(self, node):
        super().__init__("Verify At Goal")
        self.node = node
        self.shared_memory = self.node.shared_memory

        self.at_goal_client = self.node.create_client(AtGoal, '/at_goal')
        self.at_goal_req_sent = False
        self.at_goal_verified = False

    def initialise(self):
        self.at_goal_req_sent = False
        self.at_goal_verified = False

    def at_goal_callback(self, future):
        res = future.result()

        if res.success:
            self.node.get_logger().info("Robot is at goal. Response message: " + res.message)
            self.at_goal_verified = True
        else:
            self.node.get_logger().warn("Robot is NOT at goal yet.")
            self.at_goal_req_sent = False  # retry

    def update(self):
        # verify with AtGoal service
        if not self.at_goal_req_sent:
            self.node.get_logger().info("Verifying goal with AtGoal service...")
            req = AtGoal.Request()
            self.at_goal_client.wait_for_service()
            future = self.at_goal_client.call_async(req)
            future.add_done_callback(self.at_goal_callback)
            self.at_goal_req_sent = True
            return pt.common.Status.RUNNING
        
        if not self.at_goal_verified:
            self.node.get_logger().info("Waiting for AtGoal verification...") 
            return pt.common.Status.RUNNING

        self.node.get_logger().info("AtGoal service verified that we are at the goal → success")
        return pt.common.Status.SUCCESS


class DeactivateBehaviour(pt.behaviour.Behaviour):
    def __init__(self, node):
        super().__init__("Deactivate")
        self.node = node
        self.deactivate_sent = False
        self.isRobotDeactivated = False
        self.deactivate_client = self.node.create_client(Deactivate, '/deactivate')
        self.shared_memory = self.node.shared_memory
        
    def initialise(self):
        self.deactivate_sent = False

    def deactivate_response_callback(self, future):
        res = future.result()
        if res.success:
            self.node.get_logger().info("Robot deactivated successfully.")
            self.isRobotDeactivated = True
            self.shared_memory.active = False
        else:
            self.node.get_logger().warn("Failed to deactivate robot.")

    def update(self):
        if not self.deactivate_sent:
            self.node.get_logger().info("Deactivating robot...")
            req = Deactivate.Request()
            self.deactivate_client.wait_for_service()
            future = self.deactivate_client.call_async(req)
            future.add_done_callback(self.deactivate_response_callback)
            self.deactivate_sent = True

        if self.isRobotDeactivated:
            self.node.get_logger().info("Robot deactivated")
            return pt.common.Status.SUCCESS
        else:
            return pt.common.Status.RUNNING 
        
        
def main(args=None):
    rclpy.init(args=args)
    node = BTStudentsNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
