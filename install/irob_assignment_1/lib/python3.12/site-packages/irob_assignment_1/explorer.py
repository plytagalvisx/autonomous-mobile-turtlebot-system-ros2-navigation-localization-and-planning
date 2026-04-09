#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient
import numpy as np
import tf2_ros
from tf2_ros import TransformException


class ExplorerNode(Node):
    def __init__(self):
        # TODO: Initialize the node with name 'explorer'.
        super().__init__('explorer')
        
        # Create TF buffer
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)    
        
        # TODO: Create a subscription to the occupancy grid map topic (e.g., '/map'),
        #       with queue size 10, and register self.map_callback.
        self.map_subscriber = self.create_subscription(OccupancyGrid, "/map", self.map_callback, 10)
        
        # TODO: Create an ActionClient for Nav2's NavigateToPose on 'navigate_to_pose'.
        self.navigate_ac = ActionClient(self, NavigateToPose, "navigate_to_pose")
        
        # TODO: Create a set to store visited frontier cells (row, col).
        self.visited_frontiers = set()
        
        # TODO: Initialize storage for the latest map (self.map_data = None).
        self.map_data = None
        
        # TODO: Initialize the robot's grid position (self.robot_position), to be
        #       updated by localization (placeholder values are fine for now).
        self.robot_position = (0, 0)
        self.robot_world_position = None
        
        # TODO: Create a periodic timer (e.g., every 5.0 seconds) that calls self.explore().
        self.navigation_in_progress = False # flag to track if a navigation goal is currently active (do not send a new goal while one is in progress)
        self.create_timer(5.0, self.explore)

    def map_callback(self, msg):
        """
        TODO: Store the latest occupancy grid message in self.map_data.
              Optionally log that a new map was received.
        """
        self.map_data = msg
        self.get_logger().info("Received new map data")

    def navigate_to(self, x, y):
        """
        TODO: Construct a PoseStamped goal in the 'map' frame at coordinates (x, y).
              - Set header.stamp using the node clock.
              - Set orientation (e.g., w = 1.0).
        TODO: Wrap that in a NavigateToPose.Goal and send it with the ActionClient.
        TODO: Wait for the action server to be available.
        TODO: Attach self.goal_response_callback to the future returned by send_goal_async().
        """
        if self.navigation_in_progress:
            self.get_logger().info("Navigation already in progress, skipping new goal")
            return
            
        goal_msg = PoseStamped()
        goal_msg.header.frame_id = "map"
        goal_msg.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.position.x = x
        goal_msg.pose.position.y = y
        goal_msg.pose.orientation.w = 1.0
        
        navigate_goal = NavigateToPose.Goal()
        navigate_goal.pose = goal_msg
        
        self.navigation_in_progress = True
        self.get_logger().info(f"Sending navigation goal to ({x:.2f}, {y:.2f})")
        
        self.navigate_ac.wait_for_server()
        send_goal_future = self.navigate_ac.send_goal_async(navigate_goal)
        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        """
        TODO: Check whether the goal was accepted or rejected.
        TODO: If accepted, request the result and attach self.navigation_complete_callback
              to the result future (goal_handle.get_result_async()).
        """
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.navigation_in_progress = False
            self.get_logger().info("Navigation goal rejected")
            return
        
        self.get_logger().info("Navigation goal accepted, waiting for result...")
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.navigation_complete_callback)

    def navigation_complete_callback(self, future):
        """
        TODO: Handle completion of the navigation action.
              - If successful, log/record the result.
              - On failure, log the exception or error.
        """
        # try:
        #     result = future.result().result
        #     self.get_logger().info("Navigation completed successfully")
        #     self.get_logger().info(f"Final pose: ({result.final_pose.pose.position.x:.2f}, {result.final_pose.pose.position.y:.2f})")
        # except Exception as e:
        #     self.get_logger().error(f"Navigation failed: {e}")
        
        try:
            goal_result = future.result()
            status = goal_result.status
            result = goal_result.result

            if status == 4:
                self.get_logger().info("Navigation succeeded")
            else:
                self.get_logger().warn(f"Navigation finished with status code: {status}")

            self.get_logger().info(f"Result: {result}")
        except Exception as e:
            self.get_logger().error(f"Navigation failed: {e}")
        finally:
            self.navigation_in_progress = False

    def find_frontiers(self, map_array):
        """
        TODO: Detect frontier cells in the occupancy grid.
              Definition: a frontier is a FREE cell (value == 0)
              that has at least one UNKNOWN neighbor (value == -1)
              in its 8-neighborhood.

              Steps:
              - Iterate over interior cells (avoid the outermost border).
              - For each free cell, check the 3x3 neighborhood.
              - If any neighbor is unknown, add (row, col) to a list of frontiers.
              - Return the list of (row, col) frontier cells.
        """
        frontiers = []
        height, width = map_array.shape
        
        for row in range(1, height - 1):
            for col in range(1, width - 1):
                if map_array[row, col] == 0:  # Free cell
                    neighborhood = map_array[row-1:row+2, col-1:col+2]
                    if np.any(neighborhood == -1):  # At least one unknown neighbor
                        frontiers.append((row, col))
        
        return frontiers

    def choose_frontier(self, frontiers):
        """
        TODO: Choose the closest frontier to the robot's current grid position.
              - Skip frontiers already present in self.visited_frontiers.
              - Compute Euclidean distance in grid coordinates.
              - Keep the minimum; return (row, col) or None if none available.
              - Add the chosen frontier to self.visited_frontiers.
        """
        if not frontiers:
            return None
        
        closest_frontier = None
        min_distance = float('inf')
        
        for frontier in frontiers:
            if frontier in self.visited_frontiers:
                continue
            
            distance = np.sqrt((frontier[0] - self.robot_position[0])**2 + 
                               (frontier[1] - self.robot_position[1])**2)
            
            if distance < min_distance:
                min_distance = distance
                closest_frontier = frontier
        
        if closest_frontier is not None:
            self.mark_frontier_region_visited(closest_frontier) # here we mark a whole region around the chosen frontier as visited to prevent the robot from trying to navigate to very close frontiers in the future.
            # self.visited_frontiers.add(closest_frontier)
        
        return closest_frontier

    # More advanced frontier selection with clustering and centroid computation
    def choose_frontier_cluster_centroid(self, frontiers):
        """
        Cluster frontier cells, then choose the closest cluster centroid
        to the robot's current grid position.
        Skip centroids already visited.
        """
        if not frontiers:
            return None

        clusters = self.cluster_frontiers(frontiers)

        best_centroid = None
        best_cluster = None
        min_distance = float('inf')

        for cluster in clusters:
            centroid = self.compute_cluster_centroid(cluster)

            if centroid in self.visited_frontiers:
                continue

            distance = np.sqrt(
                (centroid[0] - self.robot_position[0]) ** 2 +
                (centroid[1] - self.robot_position[1]) ** 2
            )

            if distance < min_distance:
                min_distance = distance
                best_centroid = centroid
                best_cluster = cluster

        # if best_centroid is not None:
        #     self.mark_frontier_region_visited(best_centroid, radius=5)

        if best_cluster is not None:
            for cell in best_cluster:
                self.visited_frontiers.add(cell)

        return best_centroid

    def filter_frontiers_by_distance(self, frontiers, min_distance_m=0.4):
        if self.map_data is None or self.robot_world_position is None:
            return frontiers

        resolution = self.map_data.info.resolution
        origin_x = self.map_data.info.origin.position.x
        origin_y = self.map_data.info.origin.position.y
        robot_x, robot_y = self.robot_world_position

        filtered = []
        for row, col in frontiers:
            x = (col + 0.5) * resolution + origin_x
            y = (row + 0.5) * resolution + origin_y

            distance_m = np.sqrt((x - robot_x)**2 + (y - robot_y)**2)
            if distance_m >= min_distance_m:
                filtered.append((row, col))

        return filtered

    def update_robot_position(self):
        if self.map_data is None:
            return

        try:
            # Get the latest transform from "map" to "base_link" to find the robot's current position in the map frame
            transform = self.tf_buffer.lookup_transform(
                "map", # self.map_data.header.frame_id,  # target frame (e.g., "map")
                "base_link",                    # source frame (robot's base frame)
                rclpy.time.Time()
            )

            # Robot position in the map frame
            x = transform.transform.translation.x
            y = transform.transform.translation.y

            resolution = self.map_data.info.resolution
            origin_x = self.map_data.info.origin.position.x
            origin_y = self.map_data.info.origin.position.y

            # Robot position in grid coordinates (row, col)
            col = int((x - origin_x) / resolution)
            row = int((y - origin_y) / resolution)

            self.robot_world_position = (x, y) 
            self.robot_position = (row, col)
            return True

        except TransformException as ex:
            self.get_logger().warn(f'Could not transform map to base_link: {ex}')
            return False

    def mark_nearby_frontiers_visited(self, frontiers, radius_cells=2):
        for frontier in frontiers:
            self.mark_frontier_region_visited(frontier, radius=radius_cells)

    def mark_frontier_region_visited(self, frontier, radius=5):
        r0, c0 = frontier
        for r in range(r0 - radius, r0 + radius + 1):
            for c in range(c0 - radius, c0 + radius + 1):
                self.visited_frontiers.add((r, c))

    def cluster_frontiers(self, frontiers):
        """
        Group frontier cells into 8-connected clusters.
        Returns a list of clusters, where each cluster is a list of (row, col) cells.
        """
        frontier_set = set(frontiers)
        visited = set()
        clusters = []

        for cell in frontier_set:
            if cell in visited:
                continue

            cluster = []
            stack = [cell]
            visited.add(cell)

            while stack:
                current = stack.pop()
                cluster.append(current)
                r, c = current

                # 8-connected neighbors
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue

                        neighbor = (r + dr, c + dc)
                        if neighbor in frontier_set and neighbor not in visited:
                            visited.add(neighbor)
                            stack.append(neighbor)

            clusters.append(cluster)

        return clusters

    def compute_cluster_centroid(self, cluster):
        """
        Compute centroid of a cluster in grid coordinates.
        Returns (row, col) as integers.
        """
        rows = [cell[0] for cell in cluster]
        cols = [cell[1] for cell in cluster]

        row_centroid = int(np.mean(rows))
        col_centroid = int(np.mean(cols))

        return (row_centroid, col_centroid)

    def explore(self):
        """
        TODO: Main exploration routine:
              - If no map yet, return early.
              - Convert the flat map data to a 2D numpy array with shape
                (height, width).
              - Call find_frontiers(map_array) to get candidates.
              - If none, optionally log "exploration complete" and return.
              - Call choose_frontier(frontiers); if None, return.
              - Convert the chosen (row, col) to world (x, y) using:
                    x = col * resolution + origin.position.x
                    y = row * resolution + origin.position.y
              - Call navigate_to(x, y).
        """
        if self.map_data is None:
            self.get_logger().info("No map data yet, cannot explore.")
            return
        
        if not self.navigate_ac.server_is_ready():
            self.get_logger().info("NavigateToPose server not ready yet.")
            return
        
        # self.update_robot_position()
        if not self.update_robot_position():
            return

        # Convert flat map data to 2D array
        width = self.map_data.info.width
        height = self.map_data.info.height
        map_array = np.array(self.map_data.data).reshape((height, width))
        
        frontiers = self.find_frontiers(map_array)
        if not frontiers:
            self.get_logger().info("No frontiers found. Exploration complete!")
            return
        
        filtered_frontiers = self.filter_frontiers_by_distance(frontiers, min_distance_m=0.4)
        if not filtered_frontiers:
            self.get_logger().info("All detected frontiers are too close to the robot. Marking local frontier patch as visited.")
            # self.mark_nearby_frontiers_visited(frontiers, radius_cells=2)
            return
        
        # chosen_frontier = self.choose_frontier(filtered_frontiers)
        chosen_frontier = self.choose_frontier_cluster_centroid(filtered_frontiers) # more advanced frontier selection with clustering and centroid computation
        if chosen_frontier is None:
            self.get_logger().info("No (closest) unvisited frontiers available.")
            return
        
        row, col = chosen_frontier
        resolution = self.map_data.info.resolution
        origin_x = self.map_data.info.origin.position.x
        origin_y = self.map_data.info.origin.position.y
        
        x = col * resolution + origin_x
        y = row * resolution + origin_y
        
        # robot_x, robot_y = self.robot_world_position
        # distance_m = np.sqrt((x - robot_x)**2 + (y - robot_y)**2)
        # if distance_m < 0.4:
        #     self.visited_frontiers.add(chosen_frontier) # this prevents the same frontier from being chosen again in the future, even if we skip it now due to being too close
        #     self.get_logger().info("Chosen frontier too close to robot, skipping")
        #     return
        
        self.navigate_to(x, y)

def main(args=None):
    # TODO: Standard ROS 2 boilerplate:
    # - Initialize rclpy
    rclpy.init(args=args)
    # - Create the ExplorerNode
    node = ExplorerNode()
    # - Spin
    rclpy.spin(node)
    # - On shutdown, destroy node and call rclpy.shutdown()
    node.destroy_node()
    rclpy.shutdown()