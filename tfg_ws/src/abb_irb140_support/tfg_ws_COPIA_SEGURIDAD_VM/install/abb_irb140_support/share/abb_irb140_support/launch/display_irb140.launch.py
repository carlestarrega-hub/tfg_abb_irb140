import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command

def generate_launch_description():
    pkg_dir = get_package_share_directory('abb_irb140_support')
    
    # 1. RUTA AL ARCHIVO
    xacro_file = os.path.join(pkg_dir, 'urdf', 'irb140.urdf.xacro')

    # 2. PROCESAR XACRO
    robot_description_config = Command(['xacro ', xacro_file])

    # 3. PUBLICADOR DE ESTADO DEL ROBOT (Estructura)
    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_config}]
    )

    # 4. PUBLICADOR DE ARTICULACIONES (¡ESTO ES LO NUEVO!)
    # Esto publica los ángulos de los motores para que el robot se "arme"
    jsp_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui'
    )

    # 5. Rviz
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', os.path.join(pkg_dir, 'rviz', 'default.rviz')]
    )
    
    # 6. Transformada estática (World -> base_link)
    static_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='world_to_base',
        arguments=['0', '0', '0', '0', '0', '0', 'world', 'base_link']
    )

    return LaunchDescription([
        static_tf,
        rsp_node,
        jsp_gui_node,  # <--- Añadido aquí
        rviz_node
    ])
