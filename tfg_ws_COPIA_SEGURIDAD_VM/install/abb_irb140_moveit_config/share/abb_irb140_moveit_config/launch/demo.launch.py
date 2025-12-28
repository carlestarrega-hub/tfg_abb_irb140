import os
from launch import LaunchDescription
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_demo_launch

def generate_launch_description():
    user_home = os.path.expanduser("~")
    
    # Rutas absolutas
    urdf_path = os.path.join(user_home, "tfg_ws/src/abb_irb140_final.urdf")
    srdf_path = os.path.join(user_home, "tfg_ws/src/abb_irb140_moveit_config/config/abb_irb140.srdf")
    moveit_controllers_path = os.path.join(user_home, "tfg_ws/src/abb_irb140_moveit_config/config/moveit_controllers.yaml")

    # Construir la configuración FORZANDO la carga de OMPL
    moveit_config = MoveItConfigsBuilder("abb_irb140", package_name="abb_irb140_moveit_config") \
        .robot_description(file_path=urdf_path) \
        .robot_description_semantic(file_path=srdf_path) \
        .trajectory_execution(file_path=moveit_controllers_path) \
        .planning_pipelines(pipelines=["ompl"]) \
        .to_moveit_configs()

    return generate_demo_launch(moveit_config)
