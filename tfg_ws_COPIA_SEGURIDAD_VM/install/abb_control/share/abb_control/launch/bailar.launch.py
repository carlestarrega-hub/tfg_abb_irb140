import os
import yaml
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder

def load_yaml(package_name, file_path):
    package_path = get_package_share_directory(package_name)
    absolute_file_path = os.path.join(package_path, file_path)
    try:
        with open(absolute_file_path, 'r') as file:
            return yaml.safe_load(file)
    except OSError:
        return None

def generate_launch_description():
    # 1. Configuración Base (URDF, SRDF, Kinematics)
    moveit_config = MoveItConfigsBuilder("abb_irb140", package_name="abb_irb140_moveit_config").to_moveit_configs()

    # 2. Cargar OMPL manualmente para asegurar
    ompl_yaml = load_yaml("abb_irb140_moveit_config", "config/ompl_planning.yaml")
    ompl_yaml["planning_plugin"] = "ompl_interface/OMPLPlanner" # Parche de seguridad

    # 3. Convertir a diccionario
    moveit_params = moveit_config.to_dict()
    
    # 4. Inyectar OMPL explícitamente
    moveit_params["planning_pipelines"] = {
        "pipeline_names": ["ompl"],
        "default_planning_pipeline": "ompl",
        "ompl": ompl_yaml
    }
    
    # 5. Definir parámetros de petición por defecto (evita warnings)
    moveit_params["plan_request_params"] = {
        "planning_pipeline": "ompl",
        "planner_id": "RRTConnect",
        "planning_time": 2.0,
        "planning_attempts": 10
    }

    # 6. Lanzar el nodo
    return LaunchDescription([
        Node(
            package="abb_control",
            executable="bailar",
            output="screen",
            parameters=[moveit_params]
        )
    ])
