import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch.conditions import IfCondition
from launch_ros.actions import Node

def generate_launch_description():
    pkg_dir = get_package_share_directory('abb_irb140_support')

    # 1. RUTA AL ARCHIVO XACRO
    xacro_file = os.path.join(pkg_dir, 'urdf', 'irb140.urdf.xacro')

    # 2. ARGUMENTOS (Para que el script pueda controlar si abrimos ventanas o no)
    use_gui = LaunchConfiguration('use_gui')
    use_rviz = LaunchConfiguration('use_rviz')

    # 3. NODOS
    # Publicador del estado del robot (Cerebro)
    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': Command(['xacro ', xacro_file])}]
    )

    # Publicador de articulaciones (Versión GUI - Ventanita)
    jsp_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        condition=IfCondition(use_gui) # SOLO se abre si el script lo pide
    )
    
    # Publicador de articulaciones (Versión Ciega - Sin ventana)
    jsp_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        condition=IfCondition("true") # Siempre activo para mantener el robot unido
    )

    # RViz (Visualizador)
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', os.path.join(pkg_dir, 'rviz', 'default.rviz')],
        condition=IfCondition(use_rviz) # SOLO se abre si el script lo pide
    )

    # Transformada estática
    static_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='world_to_base',
        arguments=['0', '0', '0', '0', '0', '0', 'world', 'base_link']
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_gui', default_value='true'),
        DeclareLaunchArgument('use_rviz', default_value='true'),
        DeclareLaunchArgument('robot_ip', default_value='192.168.125.1'),
        DeclareLaunchArgument('use_fake_hardware', default_value='true'),
        static_tf,
        rsp_node,
        jsp_gui_node,
        jsp_node,
        rviz_node
    ])
