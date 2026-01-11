import os
import sys

import launch
import launch_ros.actions
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    rviz_config_file = get_package_share_directory('ocs2_legged_robot_ros') + "/rviz/legged_robot.rviz"
    ld = launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(
            name='rviz',
            default_value='true'
        ),
        launch.actions.DeclareLaunchArgument(
            name='description_name',
            default_value='legged_robot_description'
        ),
        launch.actions.DeclareLaunchArgument(
            name='multiplot',
            default_value='false'
        ),
        launch.actions.DeclareLaunchArgument(
            name='terminal_prefix',
            default_value=''
        ),
        launch.actions.DeclareLaunchArgument(
            name='robot_name',
            default_value='anymal_c',
            description='Robot name: anymal_c, b2, etc.'
        ),
        launch.actions.DeclareLaunchArgument(
            name='taskFile',
            default_value=PathJoinSubstitution([
                FindPackageShare('ocs2_robotic_assets'),
                'resources',
                LaunchConfiguration('robot_name'),
                'mpc',
                'task.info'
            ])
        ),
        launch.actions.DeclareLaunchArgument(
            name='referenceFile',
            default_value=PathJoinSubstitution([
                FindPackageShare('ocs2_robotic_assets'),
                'resources',
                LaunchConfiguration('robot_name'),
                'mpc',
                'reference.info'
            ])
        ),
        launch.actions.DeclareLaunchArgument(
            name='urdfFile',
            default_value=PathJoinSubstitution([
                FindPackageShare('ocs2_robotic_assets'),
                'resources',
                LaunchConfiguration('robot_name'),
                'urdf',
                [LaunchConfiguration('robot_name'), '.urdf']
            ])
        ),
        launch.actions.DeclareLaunchArgument(
            name='gaitCommandFile',
            default_value=PathJoinSubstitution([
                FindPackageShare('ocs2_robotic_assets'),
                'resources',
                LaunchConfiguration('robot_name'),
                'mpc',
                'gait.info'
            ])
        ),
        launch.actions.DeclareLaunchArgument(
            name='resourcePath',
            default_value=PathJoinSubstitution([
                FindPackageShare('ocs2_robotic_assets'),
                'resources',
                LaunchConfiguration('robot_name'),
                'meshes'
            ])
        ),
        launch_ros.actions.Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            output="screen",
            arguments=[launch.substitutions.LaunchConfiguration("urdfFile")],
        ),
        launch_ros.actions.Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=["-d", rviz_config_file],
            condition=launch.conditions.IfCondition(
                launch.substitutions.LaunchConfiguration('rviz'))
        ),
        launch_ros.actions.Node(
            package='ocs2_legged_robot_ros',
            executable='legged_robot_ipm_mpc',
            name='legged_robot_ipm_mpc',
            output='screen',
            prefix= "",
            parameters=[
                {
                    'multiplot': launch.substitutions.LaunchConfiguration('multiplot')
                },
                {
                    'taskFile': launch.substitutions.LaunchConfiguration('taskFile')
                },
                {
                    'referenceFile': launch.substitutions.LaunchConfiguration('referenceFile')
                },
                {
                    'urdfFile': launch.substitutions.LaunchConfiguration('urdfFile')
                }
            ]
        ),
        launch_ros.actions.Node(
            package='ocs2_legged_robot_ros',
            executable='legged_robot_dummy',
            name='legged_robot_dummy',
            output='screen',
            prefix=launch.substitutions.LaunchConfiguration('terminal_prefix'),
            parameters=[
                {
                    'taskFile': launch.substitutions.LaunchConfiguration('taskFile')
                },
                {
                    'referenceFile': launch.substitutions.LaunchConfiguration('referenceFile')
                },
                {
                    'urdfFile': launch.substitutions.LaunchConfiguration('urdfFile')
                }
            ]
        ),
        launch_ros.actions.Node(
            package='ocs2_legged_robot_ros',
            executable='legged_robot_target',
            name='legged_robot_target',
            output='screen',
            prefix=launch.substitutions.LaunchConfiguration('terminal_prefix'),
            parameters=[
                {
                    'referenceFile': launch.substitutions.LaunchConfiguration('referenceFile')
                }
            ]
        ),
        launch_ros.actions.Node(
            package='ocs2_legged_robot_ros',
            executable='legged_robot_gait_command',
            name='legged_robot_gait_command',
            output='screen',
            prefix=launch.substitutions.LaunchConfiguration('terminal_prefix'),
            parameters=[
                {
                    'gaitCommandFile': launch.substitutions.LaunchConfiguration('gaitCommandFile')
                }
            ]
        )
    ])
    return ld


if __name__ == '__main__':
    generate_launch_description()
