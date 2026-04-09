
#Add necessary imports

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


#USE:
# use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    
#pkg_irob_assignment_5 = "/home/parag/ros_as1_test/src/irob_assignment_5"
# pkg_irob_assignment_5 = get_package_share_directory('irob_assignment_5') # better way to do above!

# Launch node/executable goal_server , add parameter goal_params_SM.yaml or goal_params_BT.yaml as needed 
# Launch node/executable activation_server
# Launch node/executable at_goal_server 


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # pkg_irob_assignment_5 = "/home/parag/ros_as1_test/src/irob_assignment_5"
    # better way:
    pkg_irob_assignment_5 = get_package_share_directory('irob_assignment_5')

    # choose one of these as needed
    goal_params = os.path.join(
        pkg_irob_assignment_5,
        'config',
        'goal_params_BT_level_A.yaml'   # TODO: change to goal_params_BT.yaml or goal_params_SM.yaml when needed
    )

    goal_server_node = Node(
        package='irob_assignment_5',
        executable='goal_server',
        name='goal_server',
        output='screen',
        parameters=[
            goal_params,
            {'use_sim_time': use_sim_time}
        ]
    )

    activation_server_node = Node(
        package='irob_assignment_5',
        executable='activation_server',
        name='activation_server',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}]
    )

    at_goal_server_node = Node(
        package='irob_assignment_5',
        executable='at_goal_server',
        name='at_goal_service_node',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}]
    )


    map_path = os.path.join(pkg_irob_assignment_5, 'maps', 'world.yaml')
    params_path = os.path.join(pkg_irob_assignment_5, 'config', 'navigation.yaml')

    nav2_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('nav2_bringup'),
                'launch',
                'bringup_launch.py'
            )
        ),
        launch_arguments={
            'map': map_path,
            'use_sim_time': use_sim_time,
            'params_file': params_path
        }.items()
    )
    
    # amcl = Node(
    #     package='nav2_amcl',
    #     executable='amcl',
    #     name='amcl',
    #     output='screen',
    #     parameters=[params_path],
    # )
    
    # lifecycle_manager = Node(
    #     package='nav2_lifecycle_manager',
    #     executable='lifecycle_manager',
    #     name='lifecycle_manager_localization',
    #     output='screen',
    #     parameters=[{
    #         'use_sim_time': use_sim_time,
    #         'autostart': True,
    #         'node_names': [
    #             'map_server',
    #             'amcl'
    #         ]
    #     }]
    # )

    return LaunchDescription([
        # amcl,
        # lifecycle_manager,
        nav2_bringup,
        goal_server_node,
        activation_server_node,
        at_goal_server_node
    ])