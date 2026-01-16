import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped, Pose
from moveit_msgs.action import MoveGroup
from moveit_msgs.msg import Constraints, PositionConstraint, OrientationConstraint
from shape_msgs.msg import SolidPrimitive
from rclpy.action import ActionClient
import math

# --- UTILIDADES ---
def euler_to_quaternion(roll, pitch, yaw):
    roll, pitch, yaw = map(math.radians, [float(roll), float(pitch), float(yaw)])
    qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
    qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
    qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
    qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
    return [qx, qy, qz, qw]

class CerebroWeb(Node):
    def __init__(self):
        super().__init__('cerebro_web_node')
        self.sub = self.create_subscription(String, '/orden_web', self.listener_callback, 10)
        self.pub_feedback = self.create_publisher(String, '/web_feedback', 10)
        self.cli = ActionClient(self, MoveGroup, 'move_action')
        self.get_logger().info('🧠 CEREBRO CON DETECCIÓN DE ERRORES LISTO')

    def enviar_feedback(self, mensaje):
        msg = String()
        msg.data = mensaje
        self.pub_feedback.publish(msg)
        # Log en terminal para que tú también lo veas
        if "ERROR" in mensaje:
            self.get_logger().error(mensaje)
        else:
            self.get_logger().info(mensaje)

    def listener_callback(self, msg):
        cmd = msg.data
        
        if cmd == "STOP":
            self.cli.cancel_all_goals()
            self.enviar_feedback("ERROR: ⛔ PARADA DE EMERGENCIA")
            return
        
        if cmd.startswith("MOVE:"):
            try:
                parts = cmd.replace("MOVE:", "").split(",")
                x, y, z = map(float, parts[:3])
                q = euler_to_quaternion(*parts[3:])
                
                self.enviar_feedback("INFO: ⏳ Calculando trayectoria...")

                goal = MoveGroup.Goal()
                goal.request.group_name = "manipulator"
                goal.request.num_planning_attempts = 10
                goal.request.allowed_planning_time = 2.0
                
                # Restricciones
                pc = PositionConstraint()
                pc.header.frame_id = "base_link"
                pc.link_name = "tool0"
                pc.weight = 1.0
                box = SolidPrimitive(type=SolidPrimitive.BOX, dimensions=[0.01, 0.01, 0.01])
                pc.constraint_region.primitives.append(box)
                
                target = Pose()
                target.position.x, target.position.y, target.position.z = x, y, z
                target.orientation.x, target.orientation.y, target.orientation.z, target.orientation.w = q
                pc.constraint_region.primitive_poses.append(target)
                
                oc = OrientationConstraint()
                oc.header.frame_id = "base_link"
                oc.link_name = "tool0"
                oc.orientation = target.orientation
                oc.absolute_x_axis_tolerance = 0.1
                oc.absolute_y_axis_tolerance = 0.1
                oc.absolute_z_axis_tolerance = 0.1
                oc.weight = 1.0

                constraints = Constraints()
                constraints.position_constraints.append(pc)
                constraints.orientation_constraints.append(oc)
                goal.request.goal_constraints.append(constraints)

                self.cli.wait_for_server()
                self.future = self.cli.send_goal_async(goal)
                self.future.add_done_callback(self.goal_accepted_cb)

            except Exception as e:
                self.enviar_feedback(f"ERROR: Sintaxis incorrecta ({e})")

    def goal_accepted_cb(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.enviar_feedback("ERROR: ⚠️ Rechazado por el sistema")
            return
        
        # Una vez aceptado, esperamos el RESULTADO FINAL
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.result_cb)

    def result_cb(self, future):
        result = future.result().result
        # MoveIt Error Code 1 significa "SUCCESS". Todo lo demás es fallo.
        error_code = result.error_code.val
        
        if error_code == 1:
            self.enviar_feedback("EXITO: ✅ Movimiento completado")
        else:
            # Aquí capturamos si no llega, si hay colisión, etc.
            self.enviar_feedback(f"ERROR: ⚠️ Fallo de planificación (Código {error_code}). Inalcanzable o colisión.")

def main():
    rclpy.init()
    node = CerebroWeb()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
