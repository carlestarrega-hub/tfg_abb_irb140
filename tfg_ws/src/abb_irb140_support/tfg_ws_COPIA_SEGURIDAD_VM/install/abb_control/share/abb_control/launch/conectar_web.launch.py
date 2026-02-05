import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Nodo 1: El Servidor Websocket (Con el parche del 0.0)
        Node(
            package='rosbridge_server',
            executable='rosbridge_websocket',
            name='rosbridge_websocket',
            output='screen',
            parameters=[{
                'delay_between_messages': 0.0,
                'port': 9090
            }]
        ),
        # Nodo 2: La API (Ahora con el paquete correcto)
        Node(
            package='rosapi',  # <--- CAMBIO AQUÍ: 'rosapi', no 'rosbridge_server'
            executable='rosapi_node',
            name='rosapi',
            output='screen'
        )
    ])
