import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from moveit_msgs.action import MoveGroup
from moveit_msgs.msg import Constraints, JointConstraint
from rclpy.action import ActionClient
from std_msgs.msg import String
import math
import time
import sys
import socket
import struct
import concurrent.futures

class EjerciciosMasterNode(Node):
    def __init__(self):
        super().__init__('ejercicios_master_node')
        self.cli = ActionClient(self, MoveGroup, 'move_action')
        self.feedback_pub = self.create_publisher(String, '/web_feedback', 10)
        
        self.puerto = 11000
        self.ip_casa = "192.168.1.134"
        self.socket_robot = None
        
        self.get_logger().info('🚀 Nodo de Ejercicios (ROS 2 + SOCKETS) Iniciado.')
        self.conectar_robot()

    def conectar_robot(self):
        self.get_logger().info(f"🔍 Probando IP fija ({self.ip_casa})...")
        self.socket_robot, ip = self.probar_conexion(self.ip_casa, self.puerto)
        
        if self.socket_robot:
            self.enviar_feedback(f"EXITO: Conectado a RobotStudio en {ip}")
        else:
            self.enviar_feedback("ERROR: No se encontró RobotStudio. Comprueba que el RAPID está en PLAY.")
            self.get_logger().error("⚠️ No hay conexión por socket. Solo se moverá RViz.")

    def probar_conexion(self, ip, puerto):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.2) 
            s.connect((ip, puerto))
            s.settimeout(None)
            return s, ip
        except:
            return None, None

    def enviar_feedback(self, mensaje):
        msg = String()
        msg.data = mensaje
        self.feedback_pub.publish(msg)
        self.get_logger().info(f"🌐 Web: {mensaje}")

    def mover_en_robotstudio(self, joints, duracion=5.0):
        """Envía el paquete binario exacto que espera ABB"""
        if not self.socket_robot:
            return
        try:
            ext = [9E9] * 6
            # Instrucción 1: Iniciar
            self.socket_robot.sendall(struct.pack('<I4i13f', 68, 10, 1, 0, 1, *[0]*6, *ext, 1.0))
            # Instrucción 0: Mover Articulaciones
            self.socket_robot.sendall(struct.pack('<I4i13f', 68, 10, 1, 0, 0, *joints, *ext, duracion))
            # Instrucción 2: Detener/Confirmar
            self.socket_robot.sendall(struct.pack('<I4i13f', 68, 10, 1, 0, 2, *[0]*6, *ext, 1.0))
        except Exception as e:
            self.get_logger().error(f"❌ Error de Socket: {e}")

    def mover_a_grados(self, lista_grados, nombre, duracion=2.0):
        """Mueve tanto en ROS 2 (RViz) como en RobotStudio (Socket)"""
        self.get_logger().info(f"📍 Moviendo a: {nombre}")
        
        # 1. ENVIAR A ROBOTSTUDIO (Físico/Simulado)
        self.mover_en_robotstudio(lista_grados, duracion)
        
        # 2. ENVIAR A RVIZ (Simulación Visual en ROS)
        radianes = [math.radians(float(g)) for g in lista_grados]
        goal = MoveGroup.Goal()
        goal.request.group_name = "manipulator"
        goal.request.max_velocity_scaling_factor = 0.2
        goal.request.max_acceleration_scaling_factor = 0.1
        
        joint_names = ['joint_1', 'joint_2', 'joint_3', 'joint_4', 'joint_5', 'joint_6']
        constraints = Constraints()
        for i in range(6):
            jc = JointConstraint()
            jc.joint_name = joint_names[i]
            jc.position = radianes[i]
            jc.tolerance_above = 0.01
            jc.tolerance_below = 0.01
            jc.weight = 1.0
            constraints.joint_constraints.append(jc)
        
        goal.request.goal_constraints.append(constraints)
        goal.request.num_planning_attempts = 10
        goal.request.allowed_planning_time = 5.0

        self.cli.wait_for_server()
        future = self.cli.send_goal_async(goal)
        rclpy.spin_until_future_complete(self, future)
        
        result_handle = future.result()
        if not result_handle or not result_handle.accepted:
            return False

        res_future = result_handle.get_result_async()
        rclpy.spin_until_future_complete(self, res_future)
        
        # Pausa extra para asegurar que el robot físico termine el movimiento
        time.sleep(duracion)
        return True

def main():
    rclpy.init()
    nodo = EjerciciosMasterNode()

    t = {
        10:  [-87.81, 63.08, 26.73, 0.00, 0.20, 92.19],
        20:  [-44.75, 64.97, 11.39, 0.00, 13.64, 135.25],
        30:  [-36.38, 74.04, -17.79, 0.00, 33.75, 143.62],
        40:  [-31.92, 78.02, -27.88, 0.00, 39.85, 148.08],
        50:  [-30.25, 73.32, -15.88, 0.00, 32.55, 149.75],
        60:  [-28.31, 69.71, -5.60, 0.00, 25.89, 151.69],
        70:  [-24.04, 73.26, -15.72, 0.00, 32.45, 155.96],
        80:  [-14.48, 63.14, 24.32, 0.00, 2.53, 165.52],
        90:  [-8.99, 76.61, -24.39, 0.00, 37.78, 171.01],
        100: [10.88, 66.46, 5.25, 0.00, 18.30, 10.88],
        110: [29.99, 64.00, 16.53, 0.00, 9.47, 29.99],
        120: [19.47, 80.28, -33.30, 0.00, 43.03, 19.47],
        130: [87.89, 63.15, 24.27, 0.00, 2.58, -92.11],
        140: [52.24, 64.27, 14.94, 0.00, 10.79, -127.76],
        150: [52.24, 64.27, 14.94, 0.00, 10.79, -127.76],
        160: [36.74, 82.29, -38.01, 0.00, 45.72, -143.26]
    }

    if len(sys.argv) > 1:
        seleccion = sys.argv[1]
    else:
        seleccion = "0"

    # --- EJERCICIO 1 ---
    if seleccion == "1":
        nodo.enviar_feedback("INFO: 🚀 INICIANDO EJERCICIO 1")
        for idx in sorted(t.keys()):
            nodo.mover_a_grados(t[idx], f"Target_{idx}", duracion=1.5)

    # --- EJERCICIO 2 ---
    elif seleccion == "2":
        nodo.enviar_feedback("INFO: 🚀 INICIANDO EJERCICIO 2 (Pick & Place)")
        j_pick_base = t[140]
        j_place_base = t[80]
        for i in range(5):
            pos_z = -20.0 + (i * 4.0)
            j_pick = [j_pick_base[0], j_pick_base[1] + pos_z, j_pick_base[2], j_pick_base[3], j_pick_base[4] - pos_z, j_pick_base[5]]
            nodo.mover_a_grados(j_pick, f"Pick Caja {i+1}", duracion=2.5)

            mod_j2, mod_j3 = i * 1.0, i * -5.5
            j_place = [j_place_base[0], j_place_base[1] + mod_j2, j_place_base[2] + mod_j3, j_place_base[3], j_place_base[4] - (mod_j2 + mod_j3), j_place_base[5]]
            nodo.mover_a_grados(j_place, f"Place Caja {i+1}", duracion=2.5)

    # --- EJERCICIO 3 ---
    elif seleccion == "3":
        nodo.enviar_feedback("INFO: 🚀 INICIANDO EJERCICIO 3 (Electroimán y Arcos)")
        nodo.mover_a_grados(t[20], "Target_20 (Agarre)", duracion=2.0)
        
        nodo.enviar_feedback("INFO: 🧲 IMÁN ACTIVADO. Agarrando pieza...")
        time.sleep(2.0)

        nodo.mover_a_grados(t[40], "Punto Intermedio Arco 1", duracion=1.5)
        nodo.mover_a_grados(t[90], "Fin Arco 1", duracion=1.5)
        nodo.mover_a_grados(t[120], "Target_120 (Transición)", duracion=2.0)
        nodo.mover_a_grados(t[160], "Punto Intermedio Arco 2", duracion=1.5)
        nodo.mover_a_grados(t[110], "Fin Arco 2", duracion=1.5)
        nodo.mover_a_grados(t[20], "Target_20 (Soltar)", duracion=2.0)
        
        nodo.enviar_feedback("INFO: ❌ IMÁN DESACTIVADO. Pieza liberada.")
        time.sleep(1.0)

    # Retorno a casa (Si se ha ejecutado algún ejercicio)
    if seleccion in ["1", "2", "3"]:
        nodo.enviar_feedback("INFO: 🏠 Volviendo a posición de reposo...")
        nodo.mover_a_grados([0.0, 0.0, 0.0, 0.0, 0.0, 0.0], "Home", duracion=3.0)
        nodo.enviar_feedback("EXITO: ✅ Ejercicio finalizado correctamente.")
    
    if nodo.socket_robot:
        nodo.socket_robot.close()
    nodo.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
