import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped, Pose
from moveit_msgs.action import MoveGroup
from moveit_msgs.msg import Constraints, PositionConstraint, OrientationConstraint
from shape_msgs.msg import SolidPrimitive
from rclpy.action import ActionClient
import math
import socket
import time

# --- CONFIGURACIÓN DEL ROBOT ---
ROBOT_IP = "192.168.125.1"
ROBOT_PORT = 11000

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
        
        # Cliente de MoveIt (Para RViz)
        self.cli = ActionClient(self, MoveGroup, 'move_action')
        self.ultimo_comando = ""
        
        self.get_logger().info('🧠 CEREBRO HÍBRIDO BLINDADO LISTO')

    def enviar_feedback(self, mensaje):
        msg = String()
        msg.data = mensaje
        self.pub_feedback.publish(msg)
        if "ERROR" in mensaje:
            self.get_logger().error(mensaje)
        else:
            self.get_logger().info(mensaje)

    def enviar_al_robot_real(self, comando_str):
        """Intenta enviar el comando al robot. Si falla, asume que es simulación."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.5) # Espera maximo 1.5 seg
            s.connect((ROBOT_IP, ROBOT_PORT))
            s.send(comando_str.encode('utf-8'))
            respuesta = s.recv(1024).decode('utf-8')
            s.close()
            return True
        except Exception:
            return False

    def listener_callback(self, msg):
        cmd = msg.data
        self.get_logger().info(f"📨 Recibido de la web: {cmd}")
        
        if cmd == "STOP":
            self.ultimo_comando = "STOP"
            self.cli.cancel_all_goals()
            exito = self.enviar_al_robot_real("STOP")
            if exito:
                self.enviar_feedback("INFO: ⛔ PARADA EN ROBOT REAL")
            else:
                self.enviar_feedback("INFO: ⛔ PARADA EN SIMULACIÓN")
            return
        
        if cmd.startswith("MOVE:"):
            try:
                # 1. Extraer coordenadas
                parts = cmd.replace("MOVE:", "").split(",")
                x, y, z = map(float, parts[:3])
                q = euler_to_quaternion(*parts[3:])
                
                # --- 🛡️ MAGIA ANTI-ERRORES (RECORTE) 🛡️ ---
                # Redondeamos a 4 decimales. Así garantizamos que el mensaje
                # nunca supere los 60 caracteres (límite del robot: 80).
                # Además, le enviamos el Cuaternión directamente (q0, q1, q2, q3)
                comando_seguro = f"MOVE:{x:.4f},{y:.4f},{z:.4f},{q[0]:.4f},{q[1]:.4f},{q[2]:.4f},{q[3]:.4f}"
                self.ultimo_comando = comando_seguro
                
                self.enviar_feedback("INFO: ⏳ Calculando trayectoria en RViz...")

                # 2. Configurar MoveIt para RViz
                goal = MoveGroup.Goal()
                goal.request.group_name = "manipulator"
                goal.request.num_planning_attempts = 10
                goal.request.allowed_planning_time = 2.0
                
                pc = PositionConstraint()
                pc.header.frame_id = "base_link"
                pc.link_name = "tool0"
                pc.weight = 1.0
                box = SolidPrimitive(type=SolidPrimitive.BOX, dimensions=[0.01, 0.01, 0.01])
                pc.constraint_region.primitives.append(box)
                
                target = Pose()
                target.position.x, target.position.y, target.position.z = x, y, z
                target.orientation.x, target.orientation.y, target.orientation.z, target.orientation.w = q[0], q[1], q[2], q[3]
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

                # 3. Mandar a simular a MoveIt
                self.cli.wait_for_server()
                self.future = self.cli.send_goal_async(goal)
                self.future.add_done_callback(self.goal_accepted_cb)

            except Exception as e:
                self.enviar_feedback(f"ERROR: Sintaxis incorrecta ({e})")

    def goal_accepted_cb(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.enviar_feedback("ERROR: ⚠️ Rechazado por MoveIt")
            return
        
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.result_cb)

    def result_cb(self, future):
        result = future.result().result
        error_code = result.error_code.val
        
        # Si MoveIt lo hace con éxito (RViz se mueve)
        if error_code == 1:
            # ¡AHORA INTENTAMOS ENVIARLO AL ROBOT REAL!
            # Enviamos nuestro comando recortado y seguro
            exito_real = self.enviar_al_robot_real(self.ultimo_comando)
            
            if exito_real:
                self.enviar_feedback("EXITO: ✅ Movimiento completado (RViz + Robot Real)")
            else:
                self.enviar_feedback("INFO: 🎮 Simulación completada (Robot Físico no detectado)")
        else:
            self.enviar_feedback(f"ERROR: ⚠️ Fallo de planificación MoveIt (Colisión o Inalcanzable).")

def main():
    rclpy.init()
    node = CerebroWeb()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
