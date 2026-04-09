
# import os

# from ament_index_python.packages import get_package_share_directory
# from launch import LaunchDescription
# from launch.actions import IncludeLaunchDescription
# from launch.launch_description_sources import PythonLaunchDescriptionSource
# from launch.substitutions import LaunchConfiguration
# from launch_ros.actions import Node

# TURTLEBOT3_MODEL = os.environ['TURTLEBOT3_MODEL']


# def generate_launch_description():
#     use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    
#     world_file_name = 'turtlebot3_worlds/' + TURTLEBOT3_MODEL + '.model'
#     world = os.path.join(get_package_share_directory('turtlebot3_gazebo'), 'worlds', world_file_name)
#     launch_file_dir = os.path.join(get_package_share_directory('turtlebot3_gazebo'), 'launch')
#     pkg_gazebo_ros = get_package_share_directory('gazebo_ros')

#     pkg_irob_assignment_1 = "/Users/milenavilcinskaite/Downloads/ros2_nav2_burger_ws/src/irob_assignment_1"
#     pkg_slamtoolbox_ros = get_package_share_directory('slam_toolbox')
    
#     # Add joint state publisher node for Gazebo simulation:
#     joint_state_publisher = Node(
#         package='joint_state_publisher',
#         executable='joint_state_publisher',
#         name='joint_state_publisher',
#         parameters=[{'use_sim_time': use_sim_time}],
#         output='screen'
#     )

#     # --- RViz Launch ---
#     rviz = Node(
#         package='rviz2',
#         executable='rviz2',
#         name='rviz2',
#         arguments=[
#             '-d', os.path.join(pkg_irob_assignment_1, 'rviz', 'view.rviz'),
#             # '-s', os.path.join(pkg_irob_assignment_1, 'rviz', 'splash_screen.png')
#         ],
#         parameters=[{'use_sim_time': True}],
#         output='screen'
#     )

#     return LaunchDescription([
#         IncludeLaunchDescription(
#             PythonLaunchDescriptionSource(
#                 os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
#             ),
#             launch_arguments={'world': world}.items(),
#         ),

#         IncludeLaunchDescription(
#             PythonLaunchDescriptionSource(
#                 os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
#             ),
#         ),

#         IncludeLaunchDescription(
#             PythonLaunchDescriptionSource([launch_file_dir, '/robot_state_publisher.launch.py']),
#             launch_arguments={'use_sim_time': use_sim_time}.items(),
#         ),
        
#         joint_state_publisher,
        
#         rviz,
        
#         IncludeLaunchDescription(      
#             PythonLaunchDescriptionSource(
#                     os.path.join(pkg_slamtoolbox_ros, 'launch', 'online_async_launch.py')
#                 ),
#                 launch_arguments={'use_sim_time': use_sim_time}.items(),
#         ),
#     ])

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

TURTLEBOT3_MODEL = os.environ['TURTLEBOT3_MODEL']


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    pkg_turtlebot3_gazebo = get_package_share_directory('turtlebot3_gazebo')
    pkg_slamtoolbox_ros = get_package_share_directory('slam_toolbox')
    pkg_irob_assignment_1 = "/Users/milenavilcinskaite/Downloads/ros2_nav2_burger_ws/src/irob_assignment_1"

    # Add joint state publisher node for Gazebo simulation:
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=[
            '-d', os.path.join(pkg_irob_assignment_1, 'rviz', 'view.rviz'),
        ],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_turtlebot3_gazebo, 'launch', 'turtlebot3_world.launch.py')
            ),
            launch_arguments={'use_sim_time': use_sim_time}.items(),
        ),

        joint_state_publisher,  

        rviz,

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_slamtoolbox_ros, 'launch', 'online_async_launch.py')
            ),
            launch_arguments={'use_sim_time': use_sim_time}.items(),
        ),
    ])
    
# Why are we using this version of code?:

# You should not be building your own Gazebo bringup from gzserver.launch.py + gzclient.launch.py + robot_state_publisher.launch.py alone.

# Instead, use the full TurtleBot3 launch that already handles the proper simulation setup:
#     turtlebot3_world.launch.py
    
# That launch is the one most likely to:
#     start Gazebo
#     spawn the robot
#     load the right plugins
#     publish /odom
#     provide the odom TF Nav2 needs
    
# What to do:
#     Replace your current manual Gazebo setup in simulator.launch.py with an include of: