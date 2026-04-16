import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose
from moveit_msgs.action import MoveGroup
from moveit_msgs.msg import Constraints, PositionConstraint, OrientationConstraint
from shape_msgs.msg import SolidPrimitive
from rclpy.action import ActionClient
import time

class Ejercicio1Node(Node):
    def __init__(self):
        super().__init__('ejercicio1_node')
        self.cli = ActionClient(self, MoveGroup, 'move_action')
        self.get_logger().info('🚀 Iniciando Ejercicio 1 (Ruta Cartesiana) en ROS 2...')

    def crear_pose(self, x_mm, y_mm, z_mm, qw, qx, qy, qz):
        """Convierte las coordenadas de RAPID a ROS (Pasando de mm a metros)"""
        p = Pose()
        p.position.x = x_mm / 1000.0
        p.position.y = y_mm / 1000.0
        p.position.z = z_mm / 1000.0
        # OJO: ROS usa el orden [x, y, z, w]. RAPID te los da en orden [w, x, y, z]
        p.orientation.x = qx
        p.orientation.y = qy
        p.orientation.z = qz
        p.orientation.w = qw
        return p

    def mover(self, pose_obj, nombre):
        self.get_logger().info(f"📍 Moviendo a: {nombre}")
        goal = MoveGroup.Goal()
        goal.request.group_name = "manipulator"
        goal.request.num_planning_attempts = 10
        goal.request.allowed_planning_time = 5.0 # Tiempo extra para asegurar un buen MoveL

        # --- RESTRICCIÓN DE POSICIÓN ---
        pc = PositionConstraint()
        pc.header.frame_id = "base_link"
        pc.link_name = "tool0"
        box = SolidPrimitive(type=SolidPrimitive.BOX, dimensions=[0.001, 0.001, 0.001])
        pc.constraint_region.primitives.append(box)
        pc.constraint_region.primitive_poses.append(pose_obj)

        # --- RESTRICCIÓN DE ORIENTACIÓN ---
        oc = OrientationConstraint()
        oc.header.frame_id = "base_link"
        oc.link_name = "tool0"
        oc.orientation = pose_obj.orientation
        oc.absolute_x_axis_tolerance = 0.05
        oc.absolute_y_axis_tolerance = 0.05
        oc.absolute_z_axis_tolerance = 0.05
        oc.weight = 1.0

        constraints = Constraints()
        constraints.position_constraints.append(pc)
        constraints.orientation_constraints.append(oc)
        goal.request.goal_constraints.append(constraints)

        self.cli.wait_for_server()
        future = self.cli.send_goal_async(goal)
        rclpy.spin_until_future_complete(self, future)
        
        result_handle = future.result()
        if not result_handle.accepted:
            self.get_logger().error(f"❌ MoveIt rechazó el punto: {nombre}")
            return False

        res_future = result_handle.get_result_async()
        rclpy.spin_until_future_complete(self, res_future)
        return True

def main():
    rclpy.init()
    nodo = Ejercicio1Node()

    # --- 🛡️ AJUSTE DE ALTURA (Para evitar chocar con la mesa real) ---
    # Como en RAPID tienes Z=0, aquí sumamos unos milímetros para mayor seguridad.
    # Si quieres que roce la mesa, ponlo a 0.0
    ALTURA_SEGURIDAD_Z = 100.0 # 10 cm de elevación

    # --- CONSTANTES EXTRAÍDAS DE TU CÓDIGO RAPID ---
    # Orden RAPID cuaterniones: [q1(w), q2(x), q3(y), q4(z)]
    # Todas las orientaciones son [0, 1, 0, 0] lo que significa TCP mirando hacia abajo.
    puntos = [
        ("Target_10", nodo.crear_pose(119.966, -262.293, 0 + ALTURA_SEGURIDAD_Z, 0, 1, 0, 0)),
        ("Target_20", nodo.crear_pose(233.063, -191.395, 0 + ALTURA_SEGURIDAD_Z, 0, 1, 0, 0)),
        ("Target_30", nodo.crear_pose(237.291, -493.770, 0 + ALTURA_SEGURIDAD_Z, 0, 1, 0, 0)),
        ("Target_40", nodo.crear_pose(350.679, -379.739, 0 + ALTURA_SEGURIDAD_Z, 0, 1, 0, 0)),
        ("Target_60", nodo.crear_pose(540.614, -389.914, 0 + ALTURA_SEGURIDAD_Z, 0, 1, 0, 0)),
        ("Target_70", nodo.crear_pose(375.994,  229.119, 0 + ALTURA_SEGURIDAD_Z, 0, 1, 0, 0)),
        ("Target_80", nodo.crear_pose(536.751,  184.048, 0 + ALTURA_SEGURIDAD_Z, 0, 1, 0, 0)),
        ("Target_90", nodo.crear_pose(509.763,  341.877, 0 + ALTURA_SEGURIDAD_Z, 0, 1, 0, 0))
    ]

    # Punto seguro inicial (Home)
    home = nodo.crear_pose(400.0, 0.0, 500.0, 0, 1, 0, 0)
    
    # ============================================================
    # EJECUCIÓN DEL CICLO AUTOMÁTICO
    # ============================================================
    nodo.mover(home, "Home")

    for nombre, destino in puntos:
        nodo.mover(destino, nombre)
        # Una pequeña pausa para que el movimiento sea estable y visible
        time.sleep(1.0) 

    nodo.get_logger().info("\n🏠 Volviendo a posición inicial (Home)...")
    nodo.mover(home, "Home (Fin de ciclo)")

    nodo.get_logger().info("🏁 Ejercicio 1 completado con éxito.")
    nodo.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
