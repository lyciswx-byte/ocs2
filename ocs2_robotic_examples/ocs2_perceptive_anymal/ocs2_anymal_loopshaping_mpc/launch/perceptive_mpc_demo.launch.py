import os
import sys

import launch
import launch_ros.actions
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration


import os
import sys

import launch
import launch_ros.actions
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration
from launch.actions import OpaqueFunction


def launch_setup(context, *args, **kwargs):
    robot_name = LaunchConfiguration('robot_name').perform(context)
    
    if robot_name == 'b2':
        urdf_model_path = get_package_share_directory('ocs2_robotic_assets') + "/resources/b2/urdf/b2.urdf"
    else:
        urdf_model_path = get_package_share_directory('ocs2_robotic_assets') + "/resources/anymal_c/urdf/anymal_c.urdf"

    rviz_config_file = get_package_share_directory('ocs2_anymal_loopshaping_mpc') + "/config/rviz/demo_config.rviz"

    return [
        launch_ros.actions.Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            name='robot_state_publisher',
            output='screen',
            arguments=[urdf_model_path],
        ),
        launch_ros.actions.Node(
            package='rviz2',
            executable='rviz2',
            name='rviz_ocs2',
            output='screen',
            arguments=["-d", rviz_config_file]
        ),
        launch_ros.actions.Node(
            package='ocs2_anymal_loopshaping_mpc',
            executable='ocs2_anymal_loopshaping_mpc_perceptive_demo',
            name='ocs2_anymal_loopshaping_mpc_perceptive_demo',
            output='screen',
            parameters=[
                {
                    'config_name': launch.substitutions.LaunchConfiguration('config_name')
                },
                {
                    'forward_velocity': launch.substitutions.LaunchConfiguration('forward_velocity')
                },
                {
                    'forward_distance': launch.substitutions.LaunchConfiguration('forward_distance')
                },
                {
                    'terrain_name': launch.substitutions.LaunchConfiguration('terrain_name')
                },
                {
                    'ocs2_anymal_description': urdf_model_path
                },
                {
                    'terrain_scale': launch.substitutions.LaunchConfiguration('terrain_scale')
                },
                {
                    'adaptReferenceToTerrain': True
                },
                launch.substitutions.LaunchConfiguration(
                    'perception_parameter_file')
            ]
        ),
    ]


def generate_launch_description():
    ld = launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(
            name='robot_name',
            default_value='anymal_c'
        ),
        launch.actions.DeclareLaunchArgument(
            name='config_name',
            default_value='anymal_c'
        ),
        launch.actions.DeclareLaunchArgument(
            name='description_name',
            default_value='ocs2_anymal_description'
        ),
        launch.actions.DeclareLaunchArgument(
            name='perception_parameter_file',
            default_value=get_package_share_directory(
                'convex_plane_decomposition_ros') + '/config/parameters.yaml'
        ),
        launch.actions.DeclareLaunchArgument(
            name='terrain_name',
            default_value='step.png'
        ),
        launch.actions.DeclareLaunchArgument(
            name='terrain_scale',
            default_value='0.35'
        ),
        launch.actions.DeclareLaunchArgument(
            name='forward_velocity',
            default_value='0.5'
        ),
        launch.actions.DeclareLaunchArgument(
            name='forward_distance',
            default_value='3.0'
        ),
        OpaqueFunction(function=launch_setup)
    ])
    return ld


if __name__ == '__main__':
    generate_launch_description()
