import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Pose
from moveit_msgs.action import MoveGroup
from moveit_msgs.msg import Constraints, PositionConstraint
from shape_msgs.msg import SolidPrimitive
from rclpy.action import ActionClient
import math
import socket
import struct
import sys
import os
import subprocess

# --- CONFIGURACIÓN DE RED DINÁMICA ---
# El script master_robot.sh le pasa la IP detectada automáticamente
if len(sys.argv) > 1:
    TARGET_IP = sys.argv[1]
else:
    TARGET_IP = "10.192.123.209" # IP por defecto (Hotspot móvil detectada)

TARGET_PORT = 12000 # Puerto actualizado para evitar conflictos

def euler_to_quaternion(roll, pitch, yaw):
    roll, pitch, yaw = map(math.radians, [float(roll), float(pitch), float(yaw)])
    qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
    qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
    qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) - math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
    qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
    return [qx, qy, qz, qw]

class CerebroWeb(Node):
    def __init__(self):
        super().__init__('cerebro_web_node')
        self.sub_web = self.create_subscription(String, '/orden_web', self.listener_callback, 10)
        self.sub_joints = self.create_subscription(JointState, '/joint_states', self.joint_states_callback, 10)
        self.pub_feedback = self.create_publisher(String, '/web_feedback', 10)
        self.cli = ActionClient(self, MoveGroup, 'move_action')
        self.sock = None
        
        # Intentamos la conexión inicial
        self.conectar_destino()
        self.get_logger().info(f'🧠 CEREBRO DIGITAL TWIN LISTO (IP: {TARGET_IP}:{TARGET_PORT})')

    def conectar_destino(self):
        """Intenta abrir el socket con RobotStudio y reporta el estado exacto"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(2.0) # Tiempo de espera para redes móviles
            self.sock.connect((TARGET_IP, TARGET_PORT))
            self.get_logger().info(f"✅ CONEXIÓN EXITOSA con RobotStudio en {TARGET_IP}")
        except socket.timeout:
            self.get_logger().error(f"❌ ERROR: Tiempo de espera agotado. ¿Está el puerto {TARGET_PORT} abierto en el PC?")
            self.sock = None
        except Exception as e:
            self.get_logger().error(f"❌ FALLO DE CONEXIÓN: {e}")
            self.sock = None

    def joint_states_callback(self, msg):
        """Envía la posición de los motores al robot virtual/real en tiempo real"""
        if self.sock is None: 
            return
            
        try:
            joints_deg = [math.degrees(pos) for pos in msg.position]
            if len(joints_deg) >= 6:
                ext = [9E9] * 6 # Ejes externos no usados
                
                # Protocolo ABB: Start (1) -> Data (0) -> End (2)
                self.sock.sendall(struct.pack('<I4i13f', 68, 10, 1, 0, 1, *[0]*6, *ext, 1.0))
                payload = struct.pack('<I4i13f', 68, 10, 1, 0, 0, *joints_deg[:6], *ext, 0.1)
                self.sock.sendall(payload)
                self.sock.sendall(struct.pack('<I4i13f', 68, 10, 1, 0, 2, *[0]*6, *ext, 1.0))
        except Exception as e:
            self.get_logger().warn(f"⚠️ Conexión perdida durante el streaming: {e}")
            self.sock = None

    def listener_callback(self, msg):
        cmd = msg.data
        if cmd == "STOP":
            self.cli.cancel_all_goals()
            self.enviar_feedback("INFO: ⛔ PARADA SOLICITADA")
            return

        # Lanzador de ejercicios externos
        if cmd.startswith("RUN:"):
            num_ejercicio = cmd.split(":")[1]
            self.enviar_feedback(f"INFO: ⚙️ Lanzando Ejercicio {num_ejercicio}...")
            try:
                ruta_script = os.path.expanduser("~/tfg_ws/ejercicios_ros.py")
                subprocess.Popen(["python3", ruta_script, num_ejercicio])
            except Exception as e:
                self.enviar_feedback(f"ERROR: No se pudo lanzar el script ({e})")
            return

        if cmd.startswith("MOVE:"):
            if self.sock is None: 
                self.conectar_destino()
            self.planificar(cmd)

    def planificar(self, cmd):
        try:
            parts = cmd.replace("MOVE:", "").split(",")
            x, y, z = map(float, parts[:3])
            q = euler_to_quaternion(*parts[3:])
            self.enviar_feedback("INFO: ⏳ Calculando trayectoria...")

            goal = MoveGroup.Goal()
            goal.request.group_name = "manipulator"
            target = Pose()
            target.position.x, target.position.y, target.position.z = x, y, z
            target.orientation.x, target.orientation.y, target.orientation.z, target.orientation.w = q[0], q[1], q[2], q[3]

            pc = PositionConstraint()
            pc.header.frame_id = "base_link"
            pc.link_name = "tool0"
            box = SolidPrimitive(type=SolidPrimitive.BOX, dimensions=[0.01, 0.01, 0.01])
            pc.constraint_region.primitives.append(box)
            pc.constraint_region.primitive_poses.append(target)

            goal.request.goal_constraints.append(Constraints(position_constraints=[pc]))
            self.cli.wait_for_server()
            self.cli.send_goal_async(goal)
        except Exception as e:
            self.enviar_feedback(f"ERROR: {e}")

    def enviar_feedback(self, mensaje):
        msg = String()
        msg.data = mensaje
        self.pub_feedback.publish(msg)

def main():
    rclpy.init()
    node = CerebroWeb()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node.sock:
            node.sock.close()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
