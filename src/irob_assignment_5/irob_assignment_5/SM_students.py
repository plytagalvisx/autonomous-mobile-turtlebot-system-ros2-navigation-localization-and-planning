#!/usr/bin/env python3


#necessary imports here , follow basic Ros2 node stuff
import rclpy
from rclpy.node import Node

#import necessary services below
#from Somewhere import XX{get goal}, {activtion service}, {deactivtion service}, {Check at Goal service} 
from irob_interfaces.srv import Activate, AtGoal, Deactivate, GetGoal

# IMPORT necessary messages, you need to use cmd_vel and more
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool
from nav_msgs.msg import Odometry

# Should we use these?
from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient

# import necessary sensory messages if needed:
import math
from math import atan2, sqrt, pow
import time
import numpy as np

# Task E: Activate&GetGoals&ReachGoals without sensory input

# - Activate Robot. 
# - Demand goal and goto goal. 
# - Check if at goal, If goal is in obstacle or not reachable, demand new goal. 
# - Repeat 2, 3 till goal reached. 
# - Deactivate Robot.

# You can use the sensors/NAV2 for this level as well.
# They are referring to the robot’s perception inputs, i.e. topics like:
# /scan     --> LiDAR (laser scan)  Gives distances to obstacles.
# /odom     --> odometry (pose estimate)
# /imu      --> orientation
# /map      --> occupancy grid (from SLAM)
# /tf       --> transforms
# Nav2      --> Nav2 internally uses costmaps (from /map + /scan), planners, and controllers to navigate to a goal pose. 

# We can either:
# - manually use sensors (scan, odom, map)
# OR
# - let Nav2 use them for us

class SMStudentsNode(Node):
    def __init__(self):
        super().__init__('SM_students_node')

        #add important initializations here
        self.robot_active = False
        self.current_goal = None
        self.goal_reached = False
        self.current_pose = None
        self.map_data = None

        self.activate_future = None
        self.deactivate_future = None
        self.get_goal_future = None
        self.at_goal_future = None
        
        self.precision_done = False
        self.precision_tolerance = 0.05  # 5 cm tolerance for precision alignment
        
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.robot_active_sub = self.create_subscription(Bool, '/robot_active', self.robot_active_callback, 10)
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10) # Integrated robot sensor. To get current robot pose for validation and precision alignment
        # Could also integrate laser scan subscription here if we want to do our own obstacle avoidance or frontier detection, but not necessary for this assignment
        self.map_sub = self.create_subscription(OccupancyGrid, '/map', self.map_callback, 10)
        
        # activate robot service server
        # self.activate_service = self.create_service(Activate, 'activate', self.handle_activate_robot)
        # # self.deactivate_service = self.create_service(Deactivate, 'deactivate', self.handle_deactivate_robot)
        # # self.at_goal_service = self.create_service(AtGoal, 'at_goal', self.handle_at_goal)
        # self.get_goal_client = self.create_client(GetGoal, '/get_goal')
        
        self.navigate_ac = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self.nav_send_future = None
        self.nav_result_future = None
        self.nav_goal_handle = None
        self.navigation_in_progress = False
        self.navigation_done = False
        self.navigation_succeeded = False
        
        self.activate_client = self.create_client(Activate, '/activate')
        self.deactivate_client = self.create_client(Deactivate, '/deactivate')
        self.at_goal_client = self.create_client(AtGoal, '/at_goal')
        self.get_goal_client = self.create_client(GetGoal, '/get_goal')

        self.get_logger().info("Waiting for required services...")
        self.activate_client.wait_for_service()
        self.deactivate_client.wait_for_service()
        self.at_goal_client.wait_for_service()
        self.get_goal_client.wait_for_service()
        
        self.get_logger().info("Waiting for Nav2 action server...")
        self.navigate_ac.wait_for_server()

        self.get_logger().info("All systems ready.")
        self.get_logger().info("SM_students_node ready. Robot is inactive until activated.")
        
        # Init state machine:
            # 0 Activate
            # 1 Request goal
            # 2 Validate goal
            # 3 Send Nav2 goal
            # 4 Wait Nav2
            # 5 Precision alignment
            # 6 Check at goal
            # 7 Deactivate
            # 99 Done       
        self.state = 0  
        self.timer = self.create_timer(0.2, self.check_states)
        
    def robot_active_callback(self, msg):
        self.robot_active = msg.data

    def odom_callback(self, msg):
        self.current_pose = msg.pose.pose

    def map_callback(self, msg):
        self.map_data = msg

    def stop_robot(self):
        msg = Twist()
        self.cmd_vel_pub.publish(msg)
        
    # def handle_activate_robot(self):
    #     req = Activate.Request() # It's enough to send an empty request since we don't have any request fields in the Activate.srv
    #     future = self.activate_client.call_async(req)
    #     rclpy.spin_until_future_complete(self, future)

    #     if future.result() is not None:
    #         self.get_logger().info("Activate service called successfully.")
    #         return True
    #     else:
    #         self.get_logger().error("Failed to call activate service.")
    #         return False

    # def handle_deactivate_robot(self):
    #     req = Deactivate.Request() # It's enough to send an empty request since we don't have any request fields in the Deactivate service
    #     future = self.deactivate_client.call_async(req)
    #     rclpy.spin_until_future_complete(self, future)

    #     if future.result() is not None:
    #         self.get_logger().info("Deactivate service called successfully.")
    #         return True
    #     else:
    #         self.get_logger().error("Failed to call deactivate service.")
    #         return False

    # def request_goal(self):
    #     req = GetGoal.Request() # Here we have request/response fields such as goal_x and goal_y that we send to the get_goal service
    #     future = self.get_goal_client.call_async(req)
    #     rclpy.spin_until_future_complete(self, future)

    #     if future.result() is not None:
    #         response = future.result()
    #         self.current_goal = (response.goal_x, response.goal_y)
    #         self.get_logger().info(
    #             f"Received goal: x={response.goal_x:.2f}, y={response.goal_y:.2f}"
    #         )
    #         return True
    #     else:
    #         self.get_logger().error("Failed to call get_goal service.")
    #         return False

    # def check_at_goal(self):
    #     req = AtGoal.Request() # Here we have request/response fields such as success and message that we send to the at_goal service
    #     future = self.at_goal_client.call_async(req)
    #     rclpy.spin_until_future_complete(self, future)

    #     if future.result() is not None:
    #         response = future.result()

    #         self.goal_reached = response.success

    #         self.get_logger().info(f"At goal? {response.success} | {response.message}")
    #         return self.goal_reached
    #     else:
    #         self.get_logger().error("Failed to call at_goal service.")
    #         return False
    
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
        
    def is_goal_in_obstacle(self, goal_x, goal_y, radius_cells=1):
        """
        Returns True if the goal is:
        - outside map bounds
        - in an occupied cell
        - in an unknown cell
        - too close to occupied/unknown cells in a small neighborhood
        """
        if self.map_data is None:
            self.get_logger().warn("No map received yet, cannot validate goal.")
            return None # False

        resolution = self.map_data.info.resolution
        origin_x = self.map_data.info.origin.position.x
        origin_y = self.map_data.info.origin.position.y
        width = self.map_data.info.width
        height = self.map_data.info.height

        col = int((goal_x - origin_x) / resolution)
        row = int((goal_y - origin_y) / resolution)

        if row < 0 or row >= height or col < 0 or col >= width:
            self.get_logger().warn("Goal is outside map bounds.")
            return True

        map_array = np.array(self.map_data.data).reshape((height, width))

        for r in range(row - radius_cells, row + radius_cells + 1):
            for c in range(col - radius_cells, col + radius_cells + 1):
                if r < 0 or r >= height or c < 0 or c >= width:
                    return True

                cell_value = map_array[r, c]

                # unknown or occupied
                if cell_value == 100 or cell_value == -1:
                    self.get_logger().warn(f"Goal invalid: blocked/unknown near row={r}, col={c}, value={cell_value}")
                    return True

        return False
    
    # low-level control with /cmd_vel
    # def move_to_goal(self):
    #     if not self.robot_active:
    #         self.stop_robot()
    #         return

    #     if self.current_goal is None or self.current_pose is None:
    #         self.stop_robot()
    #         return

    #     goal_x, goal_y = self.current_goal
    #     x = self.current_pose.position.x
    #     y = self.current_pose.position.y

    #     # you also need yaw from odom, if your explorer used that
    #     yaw = self.get_yaw(self.current_pose.orientation)

    #     dx = goal_x - x
    #     dy = goal_y - y
    #     target_angle = math.atan2(dy, dx)
    #     angle_error = self.wrap_to_pi(target_angle - yaw)
    #     distance = math.sqrt(dx**2 + dy**2)

    #     cmd = Twist()

    #     if abs(angle_error) > 0.2:
    #         cmd.angular.z = 0.5 * angle_error
    #         cmd.linear.x = 0.0
    #     else:
    #         cmd.linear.x = min(0.15, 0.5 * distance)
    #         cmd.angular.z = 0.5 * angle_error

    #     self.cmd_vel_pub.publish(cmd)    
            
    # high-level navigation through Nav2
    def send_nav_goal(self, x, y):
        goal_msg = PoseStamped()
        goal_msg.header.frame_id = "map"
        goal_msg.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.position.x = x
        goal_msg.pose.position.y = y
        goal_msg.pose.orientation.w = 1.0

        navigate_goal = NavigateToPose.Goal()
        navigate_goal.pose = goal_msg

        self.navigation_in_progress = True
        self.navigation_done = False
        self.navigation_succeeded = False

        self.nav_send_future = self.navigate_ac.send_goal_async(navigate_goal)
        self.nav_send_future.add_done_callback(self.goal_response_callback)
        
    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.navigation_done = True
            self.navigation_succeeded = False
            self.navigation_in_progress = False
            self.get_logger().warn("Navigation goal rejected")
            return

        self.get_logger().info("Navigation goal accepted")
        self.nav_goal_handle = goal_handle
        self.nav_result_future = goal_handle.get_result_async()
        self.nav_result_future.add_done_callback(self.navigation_complete_callback)

    def navigation_complete_callback(self, future):
        # try:
        goal_result = future.result()
        status = goal_result.status

        self.navigation_done = True
        self.navigation_in_progress = False

        if status == 4:
            self.navigation_succeeded = True
            self.get_logger().info("Navigation succeeded.")
        else:
            self.navigation_succeeded = False
            self.get_logger().warn(f"Navigation finished with status code: {status}")
        # except Exception as e:
        #     self.navigation_done = True
        #     self.navigation_in_progress = False
        #     self.navigation_succeeded = False
        #     self.get_logger().error(f"Navigation failed: {e}")
        
    # integration of precision controller after Nav2 reports success, to drive the robot to exact center of goal pose
    def precision_align(self):
        """
        Drives robot slowly to exact goal center using cmd_vel.
        Returns True when centered.
        """

        if self.current_goal is None or self.current_pose is None:
            return False

        goal_x, goal_y = self.current_goal

        x = self.current_pose.position.x
        y = self.current_pose.position.y
        yaw = self.get_yaw(self.current_pose.orientation)

        dx = goal_x - x
        dy = goal_y - y

        distance = math.sqrt(dx**2 + dy**2)

        cmd = Twist()

        # stop condition (CENTERED)
        if distance < self.precision_tolerance:
            self.stop_robot()
            self.get_logger().info("Precision alignment complete.")
            return True

        # rotate toward goal first
        target_angle = math.atan2(dy, dx)
        angle_error = self.wrap_to_pi(target_angle - yaw)

        if abs(angle_error) > 0.1:
            cmd.angular.z = 0.8 * angle_error
        else:
            cmd.linear.x = min(0.05, 0.5 * distance)

        self.cmd_vel_pub.publish(cmd)
        return False
        
    # high-level logic (FSM):
    def check_states(self):
        if self.state == 0:
            self.get_logger().info("State 0: Activate robot")

            if self.activate_future is None:
                req = Activate.Request()
                self.activate_future = self.activate_client.call_async(req)
                return

            if self.activate_future.done():
                # try:
                    # _ = self.activate_future.result()
                self.get_logger().info("Activate service called successfully.")
                self.activate_future = None
                self.state = 1
                # except Exception as e:
                #     self.get_logger().error(f"Activate service failed: {e}")
                #     self.activate_future = None
                            
        elif self.state == 1:
            self.get_logger().info("State 1: Request goal")

            if self.get_goal_future is None:
                req = GetGoal.Request()
                self.get_goal_future = self.get_goal_client.call_async(req)
                return

            if self.get_goal_future.done():
                # try:
                response = self.get_goal_future.result()
                self.current_goal = (response.goal_x, response.goal_y)
                self.get_logger().info(f"Received goal: x={response.goal_x:.2f}, y={response.goal_y:.2f}")
                self.get_goal_future = None
                self.state = 2
                # except Exception as e:
                #     self.get_logger().error(f"GetGoal service failed: {e}")
                #     self.get_goal_future = None
                      
        elif self.state == 2:
            self.get_logger().info("State 2: Validate goal")

            if self.map_data is None:
                self.get_logger().warn("No map received yet. Waiting before validating goal.")
                return

            if self.current_goal is None:
                self.get_logger().warn("No goal to validate.")
                self.state = 1
                return
            
            goal_x, goal_y = self.current_goal
            result = self.is_goal_in_obstacle(goal_x, goal_y)

            if result is None:
                self.get_logger().warn("Still waiting for map before goal validation.")
                return
            
            if result:
                self.get_logger().warn("Goal is in obstacle/unknown region. Requesting a new goal.") # Goal invalid --> requesting new one
                self.current_goal = None
                self.state = 1
            else:
                self.get_logger().info("Goal is valid and appears free.")
                self.state = 3
                                
        # elif self.state == 3:
        #     self.get_logger().info("State 3: Move to goal")

        #     if self.current_goal is None:
        #         self.get_logger().warn("No current goal yet.")
        #         self.state = 1
        #         return

        #     if self.current_pose is None:
        #         self.get_logger().warn("No odometry/current pose yet.")
        #         return

        #     self.move_to_goal()
        #     self.state = 4
                                    
        elif self.state == 3:
            self.get_logger().info("State 3: Send Nav2 goal")

            if not self.robot_active:
                self.get_logger().warn("Robot is not active, cannot navigate.")
                self.state = 0
                return

            if self.current_goal is None:
                self.get_logger().warn("No current goal yet.")
                self.state = 1
                return

            # if self.current_pose is None:
            #     self.get_logger().warn("No odometry/current pose yet.")
            #     self.state = 0
            #     return

            gx, gy = self.current_goal
            self.send_nav_goal(gx, gy)
            # self.move_to_goal()
            self.state = 4

        elif self.state == 4:
            self.get_logger().info("Wait for Nav2")

            if self.navigation_in_progress:
                self.get_logger().info("Navigation in progress...")
                return

            if self.navigation_done:
                if self.navigation_succeeded:
                    # self.get_logger().info("Navigation succeeded, checking at goal...")
                    self.get_logger().info("Nav2 finished. Starting precision alignment.")
                    self.precision_done = False
                    self.state = 5
                else:
                    self.get_logger().warn("Unreachable --> get new goal")
                    self.state = 1

        elif self.state == 5:
            self.get_logger().info("State 5: Precision alignment")

            self.precision_done = self.precision_align()

            if self.precision_done:
                self.get_logger().info("Precision alignment complete. Checking if at goal...")
                self.state = 6

        elif self.state == 6:
            self.get_logger().info("State 6: Check at goal")

            if self.at_goal_future is None:
                req = AtGoal.Request()
                self.at_goal_future = self.at_goal_client.call_async(req)
                return

            if self.at_goal_future.done():
                # try:
                response = self.at_goal_future.result()
                self.goal_reached = response.success
                self.get_logger().info(f"At goal? {response.success} | {response.message}")
                self.at_goal_future = None

                if self.goal_reached:
                    # self.stop_robot()
                    self.get_logger().info("Goal reached successfully!")
                    self.state = 7
                else:
                    self.get_logger().warn("Not at goal after navigation. Demanding new goal.") # Navigating again to same goal.")
                    self.state = 1 # or 3?
                # except Exception as e:
                #     self.get_logger().error(f"AtGoal service failed: {e}")
                #     self.at_goal_future = None     
                                                   
        elif self.state == 7:
            self.get_logger().info("State 7: Deactivate robot")

            if self.deactivate_future is None:
                req = Deactivate.Request()
                self.deactivate_future = self.deactivate_client.call_async(req)
                return

            if self.deactivate_future.done():
                # try:
                # _ = self.deactivate_future.result()
                self.get_logger().info("Deactivate service called successfully.")
                # self.stop_robot()
                # self.deactivate_future = None
                self.state = 99
                # except Exception as e:
                #     self.get_logger().error(f"Deactivate service failed: {e}")
                #     self.deactivate_future = None
                    
                        
        elif self.state == 99:
            self.get_logger().info("Done. State machine finished.")
            # self.stop_robot()
            self.timer.cancel()
            
        # self.rate.sleep()  # Sleep to maintain loop rate and prevent spamming
        # time.sleep(1)  # Sleep a bit to prevent spamming
        
                
def main(args=None):
    # what to do here?
    # - Initialize rclpy
    # - Create the SMStudentsNode
    # - Spin
    # - On shutdown, destroy node and call rclpy.shutdown()
    rclpy.init(args=args)
    node = SMStudentsNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
