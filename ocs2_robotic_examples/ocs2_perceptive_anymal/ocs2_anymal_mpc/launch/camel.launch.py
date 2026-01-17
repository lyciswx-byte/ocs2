import os
import sys

import launch
import launch_ros.actions
from ament_index_python.packages import get_package_share_directory

def load_file_content(file_path):  
    with open(file_path, 'r') as file:  
        return file.read()  

def generate_launch_description():
    target_command = get_package_share_directory('ocs2_anymal_mpc') + "/config/anymal_c/targetCommand.info"
    description_name = get_package_share_directory('ocs2_robotic_assets') + "/resources/anymal_c/urdf/anymal_c.urdf"
    ld = launch.LaunchDescription([
        launch.actions.IncludeLaunchDescription(
            launch.launch_description_sources.PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory(
                    'ocs2_anymal_mpc'), 'launch/mpc.launch.py')
            ),
            launch_arguments={
                'robot_name': 'camel',
                'config_name': 'anymal_c',
                'description_name': description_name,
                'urdf_model_path': description_name,
                'target_command': target_command
            }.items()
        )
    ])
    return ld


if __name__ == '__main__':
    generate_launch_description()
