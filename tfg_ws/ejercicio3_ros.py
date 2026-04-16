import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose
from moveit_msgs.action import MoveGroup
from moveit_msgs.msg import Constraints, PositionConstraint
from shape_msgs.msg import SolidPrimitive
from rclpy.action import ActionClient
import time

class Ejercicio3Node(Node):
    def __init__(self):
        super().__init__('ejercicio3_node')
        self.cli = ActionClient(self, MoveGroup, 'move_action')
        self.get_logger().info('🚀 Iniciando Ejercicio 3 (Pick & Place) con tiempos de espera optimizados...')

    def crear_pose(self, x_mm, y_mm, z_mm, qw, qx, qy, qz):
        p = Pose()
        p.position.x = x_mm / 1000.0
        p.position.y = y_mm / 1000.0
        p.position.z = z_mm / 1000.0
        p.orientation.w = qw
        p.orientation.x = qx
        p.orientation.y = qy
        p.orientation.z = qz
        return p

    def mover(self, pose_obj, nombre):
        self.get_logger().info(f"📍 Moviendo a: {nombre}")
        goal = MoveGroup.Goal()
        goal.request.group_name = "manipulator"
        
        pc = PositionConstraint()
        pc.header.frame_id = "base_link"
        pc.link_name = "tool0"
        box = SolidPrimitive(type=SolidPrimitive.BOX, dimensions=[0.01, 0.01, 0.01])
        pc.constraint_region.primitives.append(box)
        pc.constraint_region.primitive_poses.append(pose_obj)
        goal.request.goal_constraints.append(Constraints(position_constraints=[pc]))

        self.cli.wait_for_server()
        future = self.cli.send_goal_async(goal)
        rclpy.spin_until_future_complete(self, future)
        
        result_future = future.result().get_result_async()
        rclpy.spin_until_future_complete(self, result_future)
        return True

def main():
    rclpy.init()
    nodo = Ejercicio3Node()

    # Puntos extraídos de RAPID
    home      = nodo.crear_pose(815.48, 0.0, 923.69,   0.5, 0.0, 0.866025, 0.0)
    seguro    = nodo.crear_pose(-32.38, 982.34, 636.90, 0.09317, 0.2183, 0.9593, -0.1527)
    pick      = nodo.crear_pose(723.84, 53.26, 674.47,  0.5, 0.0, 0.866025, 0.0)
    target_90 = nodo.crear_pose(116.55, 991.84, 243.99, 0.05026, 0.23765, 0.95568, -0.16628)
    target_60 = nodo.crear_pose(-79.29, 962.59, 244.00, 0.5, 0.0, 0.866025, 0.0)
    target_50 = nodo.crear_pose(6.90, 1100.10, 394.38,  0.5, 0.0, 0.866025, 0.0)

    # --- TIEMPOS DE ESPERA (Configurables) ---
    TIEMPO_COGER = 2.0  # Tiempo para activar imán/ventosa
    TIEMPO_SOLTAR = 3.0 # Tiempo para soltar (Aumentado para seguridad)

    # --- CICLO ---
    nodo.mover(home, "Home")

    puntos_entrega = [("Target 90", target_90), ("Target 60", target_60), ("Target 50", target_50)]

    for nombre, destino in puntos_entrega:
        nodo.get_logger().info("⏳ Esperando llegada de pieza...")
        time.sleep(1.5)
        
        nodo.mover(pick, "Pick Pieza")
        nodo.get_logger().info(f"🧲 COGIENDO... (Esperando {TIEMPO_COGER}s)")
        time.sleep(TIEMPO_COGER)
        
        nodo.mover(seguro, "Aduana (Seguridad)")
        nodo.mover(destino, nombre)
        
        nodo.get_logger().info(f"💨 SOLTANDO... (Esperando {TIEMPO_SOLTAR}s)")
        time.sleep(TIEMPO_SOLTAR)
        
        nodo.mover(seguro, "Aduana (Seguridad)")

    nodo.mover(home, "Fin de Ciclo")
    nodo.get_logger().info("🏁 Ciclo completado.")

    nodo.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
