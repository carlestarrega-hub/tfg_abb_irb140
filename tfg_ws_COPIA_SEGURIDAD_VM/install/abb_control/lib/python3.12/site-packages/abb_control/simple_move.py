#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import math
from moveit.planning import MoveItPy
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped

comando_recibido = None
valores_recibidos = []

# --- CONVERSOR MATEMÁTICO ---
def get_quaternion_from_euler(roll, pitch, yaw):
  """
  Convierte grados de Euler a Cuaternios (x,y,z,w)
  """
  roll = math.radians(roll)
  pitch = math.radians(pitch)
  yaw = math.radians(yaw)

  qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
  qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
  qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
  qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)

  return [qx, qy, qz, qw]

class EscuchaWeb(Node):
    def __init__(self):
        super().__init__('nodo_escucha_web')
        self.subscription = self.create_subscription(String, '/orden_web', self.callback, 10)

    def callback(self, msg):
        global comando_recibido, valores_recibidos
        texto = msg.data
        
        if texto.startswith("MOVE:"):
            try:
                # MOVE:X,Y,Z,ROLL,PITCH,YAW
                datos = texto.split(":")[1]
                valores_recibidos = [float(p) for p in datos.split(",")]
                comando_recibido = "MOVER"
                print(f"📨 Datos recibidos: {valores_recibidos}")
            except ValueError:
                print("❌ Error de formato en números")

def main():
    rclpy.init()
    global comando_recibido, valores_recibidos
    print("🤖 SISTEMA DE 6 EJES LISTO. Esperando órdenes...")

    try:
        dark_robot = MoveItPy(node_name="moveit_py")
        abb_arm = dark_robot.get_planning_component("manipulator")
    except Exception as e:
        print(e)
        return

    nodo_escucha = EscuchaWeb()

    while rclpy.ok():
        rclpy.spin_once(nodo_escucha, timeout_sec=0.1)

        if comando_recibido == "MOVER":
            # ESTA ES LA LÍNEA QUE FALLABA ANTES
            # Ahora desempaquetamos 6 valores correctamente
            x, y, z, r, p, w = valores_recibidos
            
            print(f"🚀 Moviendo a Pos:({x},{y},{z}) | Rot:({r},{p},{w})")
            
            abb_arm.set_start_state_to_current_state()
            pose_goal = PoseStamped()
            pose_goal.header.frame_id = "base_link"
            
            # Posición
            pose_goal.pose.position.x = x
            pose_goal.pose.position.y = y
            pose_goal.pose.position.z = z
            
            # Orientación (Calculada con los 3 sliders)
            qx, qy, qz, qw = get_quaternion_from_euler(r, p, w)
            pose_goal.pose.orientation.x = qx
            pose_goal.pose.orientation.y = qy
            pose_goal.pose.orientation.z = qz
            pose_goal.pose.orientation.w = qw

            abb_arm.set_goal_state(pose_stamped_msg=pose_goal, pose_link="link_6")
            
            plan = abb_arm.plan()
            
            if plan:
                dark_robot.execute(plan.trajectory, controllers=[])
            else:
                print("⚠️ MOVIMIENTO IMPOSIBLE. Prueba otros ángulos.")
            
            comando_recibido = None

    rclpy.shutdown()

if __name__ == "__main__":
    main()
