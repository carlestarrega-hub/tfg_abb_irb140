import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
from launch.conditions import IfCondition, UnlessCondition

def generate_launch_description():
    # --- ARGUMENTOS ---
    use_fake = DeclareLaunchArgument('use_fake_hardware', default_value='true')
    ip_robot = DeclareLaunchArgument('robot_ip', default_value='192.168.125.1')

    # --- PAQUETES ---
    # Ahora esto SÍ funcionará porque hemos copiado la carpeta
    pkg_moveit = FindPackageShare('abb_irb140_moveit_config')

    # --- 1. MODO SIMULACIÓN ---
    simulacion = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([pkg_moveit, '/launch/demo.launch.py']),
        launch_arguments={'use_rviz': 'false', 'use_sim_time': 'false'}.items(),
        condition=IfCondition(LaunchConfiguration('use_fake_hardware'))
    )

    # --- 2. MODO REAL ---
    real = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([pkg_moveit, '/launch/moveit_planning_execution.launch.py']),
        launch_arguments={'use_rviz': 'false', 'robot_ip': LaunchConfiguration('robot_ip')}.items(),
        condition=UnlessCondition(LaunchConfiguration('use_fake_hardware'))
    )

    return LaunchDescription([use_fake, ip_robot, simulacion, real])
