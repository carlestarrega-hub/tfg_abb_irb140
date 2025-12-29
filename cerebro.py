import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped, Quaternion
from moveit_msgs.action import MoveGroup
from moveit_msgs.msg import Constraints, PositionConstraint, OrientationConstraint, BoundingVolume
from shape_msgs.msg import SolidPrimitive
import math

# Función auxiliar para convertir grados a Cuaternión (lo que entiende el robot)
def euler_to_quaternion(roll_deg, pitch_deg, yaw_deg):
    roll = math.radians(roll_deg)
    pitch = math.radians(pitch_deg)
    yaw = math.radians(yaw_deg)
    
    qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
    qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
    qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
    qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
    return Quaternion(x=qx, y=qy, z=qz, w=qw)

class CerebroRobot(Node):
    def __init__(self):
        super().__init__('cerebro_web')
        
        # 1. Escuchar a la Web
        self.subscription = self.create_subscription(
            String, '/orden_web', self.listener_callback, 10)
            
        # 2. Cliente para hablar con MoveIt (Action Client)
        self._action_client = ActionClient(self, MoveGroup, 'move_action')
        
        self.get_logger().info('🧠 CEREBRO LISTO: Esperando órdenes para mover el robot...')

    def listener_callback(self, msg):
        datos = msg.data
        if datos.startswith("MOVE:"):
            try:
                # Extraer datos
                partes = datos.replace("MOVE:", "").split(",")
                x, y, z = float(partes[0]), float(partes[1]), float(partes[2])
                r, p, w = float(partes[3]), float(partes[4]), float(partes[5])

                self.get_logger().info(f'🚀 MOVIENDO A: X={x}, Y={y}, Z={z}')
                
                # Ejecutar movimiento
                self.enviar_a_moveit(x, y, z, r, p, w)
                
            except Exception as e:
                self.get_logger().error(f'Error calculando: {e}')

    def enviar_a_moveit(self, x, y, z, r, p, w):
        # Preparar el mensaje de Acción para MoveIt
        goal_msg = MoveGroup.Goal()
        goal_msg.request.group_name = 'manipulator' # Nombre del grupo en tu URDF
        goal_msg.request.num_planning_attempts = 10
        goal_msg.request.allowed_planning_time = 5.0
        
        # Definir restricciones (La Pose Objetivo)
        constraints = Constraints()
        
        # Posición
        p_const = PositionConstraint()
        p_const.header.frame_id = "base_link"
        p_const.link_name = "link_6" # La punta del robot
        p_const.constraint_region = BoundingVolume()
        p_const.constraint_region.primitives.append(SolidPrimitive(type=SolidPrimitive.SPHERE, dimensions=[0.01]))
        
        # Aquí definimos la posición destino
        pose = PoseStamped()
        pose.header.frame_id = "base_link"
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = z
        p_const.constraint_region.primitive_poses.append(pose.pose)
        p_const.weight = 1.0
        
        # Orientación
        o_const = OrientationConstraint()
        o_const.header.frame_id = "base_link"
        o_const.link_name = "link_6"
        o_const.orientation = euler_to_quaternion(r, p, w)
        o_const.absolute_x_axis_tolerance = 0.1
        o_const.absolute_y_axis_tolerance = 0.1
        o_const.absolute_z_axis_tolerance = 0.1
        o_const.weight = 1.0

        constraints.position_constraints.append(p_const)
        constraints.orientation_constraints.append(o_const)
        
        goal_msg.request.goal_constraints.append(constraints)

        # Enviar
        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(goal_msg)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('❌ MoveIt rechazó la orden (¿Fuera de rango?)')
            return
        self.get_logger().info('✅ MoveIt aceptó la orden, calculando ruta...')
        
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info('🏁 Movimiento TERMINADO.')

def main(args=None):
    rclpy.init(args=args)
    cerebro = CerebroRobot()
    rclpy.spin(cerebro)

if __name__ == '__main__':
    main()
