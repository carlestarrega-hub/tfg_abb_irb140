import os
import subprocess

# Rutas
xacro_file = os.path.expanduser("~/tfg_ws/src/abb_irb140_support/urdf/irb140.urdf.xacro")
output_file = os.path.expanduser("~/tfg_ws/src/abb_irb140_final.urdf")

# 1. Generar URDF base limpio desde Xacro
result = subprocess.run(["xacro", xacro_file], capture_output=True, text=True)
base_xml = result.stdout

# 2. Definir el bloque de control ROS2 CORRECTO
control_block = """
  <ros2_control name="IgnitionSystem" type="system">
    <hardware>
      <plugin>mock_components/GenericSystem</plugin>
    </hardware>
    <joint name="joint_1">
      <command_interface name="position"/>
      <state_interface name="position"><param name="initial_value">0.0</param></state_interface>
      <state_interface name="velocity"/>
    </joint>
    <joint name="joint_2">
      <command_interface name="position"/>
      <state_interface name="position"><param name="initial_value">0.0</param></state_interface>
      <state_interface name="velocity"/>
    </joint>
    <joint name="joint_3">
      <command_interface name="position"/>
      <state_interface name="position"><param name="initial_value">0.0</param></state_interface>
      <state_interface name="velocity"/>
    </joint>
    <joint name="joint_4">
      <command_interface name="position"/>
      <state_interface name="position"><param name="initial_value">0.0</param></state_interface>
      <state_interface name="velocity"/>
    </joint>
    <joint name="joint_5">
      <command_interface name="position"/>
      <state_interface name="position"><param name="initial_value">0.0</param></state_interface>
      <state_interface name="velocity"/>
    </joint>
    <joint name="joint_6">
      <command_interface name="position"/>
      <state_interface name="position"><param name="initial_value">0.0</param></state_interface>
      <state_interface name="velocity"/>
    </joint>
  </ros2_control>
</robot>"""

# 3. Reemplazar la etiqueta de cierre final por el bloque + cierre
# Esto evita duplicados y errores de sintaxis
final_xml = base_xml.replace("</robot>", control_block)

# 4. Guardar
with open(output_file, "w") as f:
    f.write(final_xml)

print("✅ Archivo URDF regenerado y reparado correctamente.")
