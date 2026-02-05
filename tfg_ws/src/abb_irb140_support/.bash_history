# 1. Configurar y actualizar el sistema
sudo apt update && sudo apt upgrade -y
sudo apt install software-properties-common curl -y
sudo add-apt-repository universe -y
# 2. Configurar la clave y el repositorio de ROS 2 Jazzy
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
# 3. Actualizar la lista de paquetes
sudo apt update
# 1. INSTALACIÓN DEL DESKTOP (INCLUYE TODAS LAS DEPENDENCIAS BASE)
sudo apt install ros-jazzy-desktop python3-colcon-common-extensions -y
# 2. INSTALACIÓN DE MOVEIT 2 Y UTILIDADES UR
sudo apt install ros-jazzy-moveit-py ros-jazzy-ur-moveit-config ros-jazzy-ur-robot-driver -y
sudo killall unattended-upgr
sudo rm /var/lib/dpkg/lock-frontend
sudo rm /var/lib/dpkg/lock
# 1. INSTALACIÓN DEL DESKTOP (INCLUYE TODAS LAS DEPENDENCIAS BASE)
sudo apt install ros-jazzy-desktop python3-colcon-common-extensions -y
# 2. INSTALACIÓN DE MOVEIT 2 Y UTILIDADES UR
sudo apt install ros-jazzy-moveit-py ros-jazzy-ur-moveit-config ros-jazzy-ur-robot-driver -y
# 1. Matar el proceso que tiene el candado (el PID es 2447)
sudo kill -9 2447
# 2. Eliminar los archivos de candado para liberar el gestor APT
sudo rm /var/lib/dpkg/lock-frontend
sudo rm /var/lib/dpkg/lock
sudo rm /var/cache/apt/archives/lock
# 1. INSTALACIÓN DEL DESKTOP (INCLUYE TODAS LAS DEPENDENCIAS BASE)
sudo apt install ros-jazzy-desktop python3-colcon-common-extensions -y
# 2. INSTALACIÓN DE MOVEIT 2 Y UTILIDADES UR
sudo apt install ros-jazzy-moveit-py ros-jazzy-ur-moveit-config ros-jazzy-ur-robot-driver -y
# 1. INSTALACIÓN DEL DESKTOP (INCLUYE TODAS LAS DEPENDENCIAS BASE)
sudo apt install ros-jazzy-desktop python3-colcon-common-extensions -y
# 2. INSTALACIÓN DE MOVEIT 2 Y UTILIDADES UR
sudo apt install ros-jazzy-moveit-py ros-jazzy-ur-moveit-config ros-jazzy-ur-robot-driver -y
# 1. INSTALACIÓN DEL DESKTOP (INCLUYE TODAS LAS DEPENDENCIAS BASE)
sudo apt install ros-jazzy-desktop python3-colcon-common-extensions -y
# 2. INSTALACIÓN DE MOVEIT 2 Y UTILIDADES UR
sudo apt install ros-jazzy-moveit-py ros-jazzy-ur-moveit-config ros-jazzy-ur-robot-driver -y
# 1. Cargar el entorno ROS 2
source /opt/ros/jazzy/setup.bash
# 2. Crear el nuevo workspace de ROS 2
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
# 3. Mover los archivos de tu proyecto al workspace (Asumimos que están en ~/)
mv ~/web_tfg .
mv ~/robot_control_pkg .
mv ~/abb_irb140_moveit_config .
# 1. INSTALACIÓN DEL DESKTOP (INCLUYE TODAS LAS DEPENDENCIAS BASE)
sudo apt install ros-jazzy-desktop python3-colcon-common-extensions -y
# 2. INSTALACIÓN DE MOVEIT 2 Y UTILIDADES UR
sudo apt install ros-jazzy-moveit-py ros-jazzy-ur-moveit-config ros-jazzy-ur-robot-driver -y
# 1. Cargar el entorno ROS 2
source /opt/ros/jazzy/setup.bash
# 2. Crear el nuevo workspace de ROS 2
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
# 3. Mover los archivos de tu proyecto al nuevo /src (Debe estar en la carpeta ~/)
mv ~/web_tfg .
mv ~/robot_control_pkg .
mv ~/abb_irb140_moveit_config .
cd ~
tar -xzvf TFG_FINAL_BACKUP.tar.gz
# 1. Cargar el entorno ROS 2 (necesario para el próximo paso)
source /opt/ros/jazzy/setup.bash
# 2. Crear el nuevo workspace de ROS 2
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
# 3. Mover los archivos de tu proyecto al nuevo /src 
mv ~/web_tfg .
mv ~/robot_control_pkg .
mv ~/abb_irb140_moveit_config .
# 1. Cargar el entorno ROS 2
source /opt/ros/jazzy/setup.bash
# 2. Asegurarse de estar en el nuevo src
cd ~/ros2_ws/src
# 3. Mover el código Python (está anidado en el backup)
mv ~/ros2_ws_clean/src/robot_control_pkg .
# 4. Mover la Interfaz Web (Flask)
mv ~/web_tfg .
# 5. Mover la Configuración ABB (Está anidada, la movemos entera)
mv ~/ros2_ws_clean/src/abb_irb140_moveit_config .
cd ~
ls -d */
# 1. Aseguramos que estamos en la carpeta de destino
cd ~/ros2_ws/src
# 2. Mover el código Python reescrito (está anidado en el backup)
mv ~/ros2_ws_clean/src/robot_control_pkg .
# 3. Mover la configuración de tu robot ABB
mv ~/ros2_ws_clean/src/abb_irb140_moveit_config .
# 4. Mover la Interfaz Web (Flask)
mv ~/web_tfg .
cd ~
ls -F | grep -E "web|ros2|abb|TFG"
# 1. Aseguramos que estamos en el directorio de inicio
cd ~
# 2. EXTRAER EL ARCHIVO COMPRIMIDO (Esto crea las carpetas web_tfg y ros2_ws_clean)
tar -xzvf TFG_FINAL_BACKUP.tar.gz
# 3. Cargar el entorno ROS 2
source /opt/ros/jazzy/setup.bash
# 4. Crear el nuevo workspace de ROS 2
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
# 5. Mover los archivos extraídos al nuevo /src (La ruta correcta)
# Mueve la configuración ABB
mv ~/ros2_ws_clean/src/abb_irb140_moveit_config .
# Mueve el código Python reescrito
mv ~/ros2_ws_clean/src/robot_control_pkg .
# Mueve la Interfaz Web (Flask)
mv ~/web_tfg .
cd ~/ros2_ws/src
# Borra los intentos fallidos y la estructura ABB rota
rm -rf web_tfg robot_control_pkg abb_irb140_moveit_config
# 1. Mueve el código Python reescrito
mv ~/ros2_ws_clean/src/robot_control_pkg .
# 2. Mueve la Interfaz Web (Flask)
mv ~/web_tfg .
# 3. Mueve la Configuración ABB
mv ~/ros2_ws_clean/src/abb_irb140_moveit_config .
cd ~
ls -d * | grep "web\|abb\|ros2"
ls -F ~/ros2_ws_clean
cd ~
rm -rf ros2_ws
# 1. Extraer el archivo de backup para que las carpetas aparezcan
tar -xzvf TFG_FINAL_BACKUP.tar.gz
# 2. Crear el nuevo y limpio workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
# 3. Mover los archivos fuente (asumiendo que ahora están en ~/)
mv ~/web_tfg .
mv ~/ros2_ws_clean/src/robot_control_pkg .
mv ~/ros2_ws_clean/src/abb_irb140_moveit_config .
# 1. Aseguramos estar en el directorio de inicio
cd ~
# 2. BORRAR EL TALLER ANTIGUO QUE FALLA Y CREAR UNO LIMPIO
rm -rf ros2_ws # Eliminar el workspace fallido
mkdir -p ros2_ws/src 
# 3. Mover SOLO las carpetas de código fuente esenciales al nuevo /src
# Nota: La configuración ABB se mantiene en el sistema, solo movemos tu código.
mv web_tfg ros2_ws/src/
mv ros2_ws_clean/src/robot_control_pkg ros2_ws/src/
sudo shutdown now
echo $ROS_DISTRO
source /opt/ros/jazzy/setup.bash
ls /opt/ros/
source /opt/ros/jazzy/setup.bash
echo "ROS Actual: $ROS_DISTRO"
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
source ~/.bashrc
echo $ROS_DISTRO
mkdir -p ~/tfg_ws/src
cd ~/tfg_ws
colcon build
echo "source ~/tfg_ws/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
echo $COLCON_PREFIX_PATH
cd ~/tfg_ws/src
git clone -b ros2 https://github.com/ros-industrial/abb.git
cd ~/tfg_ws
rosdep install --from-paths src --ignore-src -r -y
sudo apt update
sudo apt install python3-rosdep
sudo rosdep init
rosdep update
rosdep install --from-paths src --ignore-src -r -y
sudo shutdown now
ros2 topic list
cd ~/tfg_ws
colcon build --symlink-install
rm -rf ~/tfg_ws/src/abb
cd ~/tfg_ws/src
git clone --branch ros2 https://github.com/ros-industrial/abb.git
grep "ament_cmake" ~/tfg_ws/src/abb/abb_resources/package.xml
rm -rf ~/tfg_ws/src/abb
cd ~/tfg_ws/src
git clone -b ros2 https://github.com/PickNikRobotics/abb.git
rm -rf ~/tfg_ws/src/abb
cd ~/tfg_ws/src
git clone https://github.com/ros-industrial/abb_ros2.git
rm -rf ~/tfg_ws/src/abb
rm -rf ~/tfg_ws/src/abb_ros2
cd ~/tfg_ws/src
git clone https://github.com/PickNikRobotics/abb_ros2.git
ls ~/tfg_ws/src/abb_ros2
cd ~/tfg_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
cd ~/tfg_ws
rm -rf build install log
cd ~/tfg_ws/src
git clone -b ros2 https://github.com/ros-industrial/abb.git abb_description
cd ~/tfg_ws/src/abb_description
# Borramos todo lo que NO sea el irb140
find . -maxdepth 1 -type d -name "abb_irb*" ! -name "abb_irb140_support" -exec rm -rf {} +
cd ~/tfg_ws/src/abb_ros2/robot_specific_config
rm -rf abb_irb1200_support abb_irb2600_support abb_irb4600_support abb_irb6640_support
cd ~/tfg_ws
colcon build --symlink-install
rm -rf ~/tfg_ws/src/abb_description/abb_resources
rm -rf ~/tfg_ws/src/abb_description/moveit
cd ~/tfg_ws
colcon build --symlink-install
find ~/tfg_ws/src -type d -name "*irb1200*" -exec rm -rf {} +
find ~/tfg_ws/src/abb_description -type d -name "*gazebo*" -exec rm -rf {} +
ls -R ~/tfg_ws/src | grep "abb_"
rm -rf ~/tfg_ws/src/abb_description/abb_crb15000_support
# 1. Ir a la carpeta home temporalmente
cd ~
# 2. Descargar el repositorio completo en una carpeta temporal
git clone -b ros2 https://github.com/ros-industrial/abb.git temp_abb_repo
# 3. Mover SOLO la carpeta del IRB 140 a tu proyecto
mv temp_abb_repo/abb_irb140_support ~/tfg_ws/src/abb_description/
# 4. Borrar la carpeta temporal (limpieza)
rm -rf temp_abb_repo
ls ~/tfg_ws/src/abb_description
cd ~/tfg_ws/src
rm -rf abb_description abb_irb140_support temp_abb_repo
cd ~
git clone -b noetic-devel https://github.com/ros-industrial/abb.git temp_abb_legacy
mv ~/temp_abb_legacy/abb_irb140_support ~/tfg_ws/src/
find ~/temp_abb_legacy -type d -name "abb_irb140_support" -exec mv {} ~/tfg_ws/src/ \;
ls ~/tfg_ws/src
cd ~
rm -rf temp_abb_manual
git clone -b noetic-devel https://github.com/ros-industrial/abb.git temp_abb_manual
find ~/temp_abb_manual -name "abb_irb140_support" -type d
sudo apt update && sudo apt install wget unzip -y
cd ~
# Descargar el ZIP
wget https://github.com/ros-industrial/abb/archive/refs/heads/noetic-devel.zip
# Descomprimirlo
unzip noetic-devel.zip
mv ~/abb-noetic-devel/abb_irb140_support ~/tfg_ws/src/
sudo apt update && sudo apt install subversion -y
svn export https://github.com/ros-industrial/abb/branches/noetic-devel/abb_irb140_support ~/tfg_ws/src/abb_irb140_support
# 1. Borrar intentos fallidos previos
cd ~
rm -rf temp_abb_fix
# 2. Crear carpeta limpia e iniciar git
mkdir temp_abb_fix
cd temp_abb_fix
git init
git remote add -f origin https://github.com/ros-industrial/abb.git
# 3. Activar el modo "Sparse" (parcial)
git config core.sparseCheckout true
# 4. Decirle qué carpeta queremos exactamente
echo "abb_irb140_support/" >> .git/info/sparse-checkout
# 5. Descargar SOLO esa carpeta de la rama antigua (noetic)
git pull origin noetic-devel
# 6. Mover la carpeta descargada a tu workspace
mv ~/temp_abb_fix/abb_irb140_support ~/tfg_ws/src/
# 7. Borrar lo temporal
cd ~
rm -rf temp_abb_fix
cd ~
# Borramos intentos anteriores
rm -rf temp_abb_fix full_abb_repo
# Clonamos TODO el historial de la rama antigua (Tardará un poco más, pero es seguro)
git clone -b noetic-devel https://github.com/ros-industrial/abb.git full_abb_repo
# Copiamos la carpeta del IRB 140 desde el repo completo a tu src
cp -r ~/full_abb_repo/abb_irb140_support ~/tfg_ws/src/
find ~/full_abb_repo -name "abb_irb140_support" -type d -exec mv {} ~/tfg_ws/src/ \;
ls -F ~/tfg_ws/src
ls -F ~/full_abb_repo
cd ~
rm -rf ~/full_abb_repo
wget -O abb_kinetic.zip https://github.com/ros-industrial/abb/archive/refs/heads/kinetic-devel.zip
unzip -q abb_kinetic.zip
cp -r ~/abb-kinetic-devel/abb_irb140_support ~/tfg_ws/src/
cd ~/tfg_ws/src
rm -rf abb_irb140_support
cd ~
rm -rf abb_kinetic.zip abb-kinetic-devel full_abb_repo temp_abb_fix
cd ~/tfg_ws/src
git clone https://github.com/joshua-g/abb_irb140_support.git
cd ~/tfg_ws/src
rm -rf abb_irb140_support
cd ~
rm -rf temp_abb_old
git clone -b indigo-devel --depth 1 https://github.com/ros-industrial/abb.git temp_abb_old
find ~/temp_abb_old -name "abb_irb140_support" -type d -exec mv {} ~/tfg_ws/src/ \;
ls ~/tfg_ws/src
cd ~/tfg_ws/src
# Descargamos la rama 'kinetic-devel' en una carpeta llamada 'rescate_abb'
git clone -b kinetic-devel https://github.com/ros-industrial/abb.git rescate_abb
ls ~/tfg_ws/src/rescate_abb
~/tfg_ws/src
cd ~/tfg_ws/src
git clone https://github.com/ros-industrial/abb_experimental.git
cd ~/tfg_ws
colcon build
source install/setup.bash
[200~ls ~/tfg_ws/src/abb_experimental
~ls ~/tfg_ws/src/abb_experimental
cd ~/tfg_ws/src
rm -rf rescate_abb abb_irb140_support
git clone https://github.com/gramaziokohler/abb_irb140_support.git
cd ~
rm -rf temp_abb_old abb_irb140_support
# Descargamos el ZIP de la rama 'hydro-devel' (Esta rama es inmortal)
wget -O abb_hydro.zip https://github.com/ros-industrial/abb/archive/refs/heads/hydro-devel.zip
# Lo descomprimimos en silencio
unzip -q abb_hydro.zip
ls ~/abb-hydro-devel
find ~/abb-hydro-devel -name "*140*"
ls ~/abb-hydro-devel/abb
cd ~
git clone https://github.com/ros-industrial/abb_experimental.git
find ~/abb_experimental -name "*140*"
mkdir -p ~/tfg_ws/src/abb_irb140_support/config
mkdir -p ~/tfg_ws/src/abb_irb140_support/launch
mkdir -p ~/tfg_ws/src/abb_irb140_support/meshes
mkdir -p ~/tfg_ws/src/abb_irb140_support/urdf
cd ~/tfg_ws/src/abb_irb140_support
cat <<EOF > package.xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>abb_irb140_support</name>
  <version>0.1.0</version>
  <description>Paquete generado manualmente para ABB IRB 140</description>
  <maintainer email="usuario@tfg.com">Usuario TFG</maintainer>
  <license>Apache 2.0</license>

  <buildtool_depend>ament_cmake</buildtool_depend>
  <exec_depend>abb_resources</exec_depend>
  <exec_depend>joint_state_publisher</exec_depend>
  <exec_depend>robot_state_publisher</exec_depend>
  <exec_depend>rviz2</exec_depend>
  <exec_depend>xacro</exec_depend>

  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>
EOF

cat <<EOF > CMakeLists.txt
cmake_minimum_required(VERSION 3.5)
project(abb_irb140_support)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

find_package(ament_cmake REQUIRED)

# Instalar las carpetas que acabamos de crear
install(DIRECTORY config launch meshes urdf
  DESTINATION share/\${PROJECT_NAME}
)

ament_package()
EOF

cat <<EOF > urdf/irb140.urdf
<?xml version="1.0" ?>
<robot name="abb_irb140">
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.1 0.1 0.1"/>
      </geometry>
    </visual>
  </link>
</robot>
EOF

cd ~/tfg_ws
colcon build --symlink-install
cd ~/tfg_ws/src
# 1. Librería base de comunicación EGM
git clone https://github.com/ros-industrial/abb_libegm.git
# 2. Gestor de comunicación RWS/EGM (El que te dio el error)
git clone https://github.com/ros-industrial/abb_egm_rws_managers.git
ls ~/tfg_ws/src
rm -rf ~/tfg_ws/src/abb_experimental
cd ~/tfg_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
cd ~/tfg_ws/src
git clone https://github.com/ros-industrial/abb_librws.git
cd ~/tfg_ws
colcon build --symlink-install
cd ~/tfg_ws
sudo apt update
# Este comando leerá el paquete abb_librws e instalará 'libpoco-dev'
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
cd ~/tfg_ws/src
git clone https://github.com/ros-industrial/abb_egm_msgs.git
touch ~/tfg_ws/src/abb_ros2/abb_rws_client/COLCON_IGNORE
cd ~/tfg_ws
colcon build --symlink-install
# 1. Cargar el entorno
source ~/tfg_ws/install/setup.bash
# 2. Lanzar la visualización
ros2 launch abb_irb140_support view_robot.launch.py
ros2 run rviz2 rviz2
mkdir -p ~/tfg_ws/src/abb_irb140_support/launch
cd ~/tfg_ws/src/abb_irb140_support/launch
cat <<EOF > rsp.launch.py
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('abb_irb140_support')
    
    # Busca el archivo URDF (sea .urdf o .xacro)
    urdf_file = os.path.join(pkg_share, 'urdf', 'irb140.urdf')
    # Si no existe irb140.urdf, intentamos buscar el xacro común
    if not os.path.exists(urdf_file):
         # Ajusta este nombre si tu archivo se llama diferente dentro de la carpeta urdf
         urdf_file = os.path.join(pkg_share, 'urdf', 'irb140.xacro')

    # Nodo que lee el URDF y lo publica en la red
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': Command(['xacro ', urdf_file])}]
    )

    # Nodo falso para publicar posiciones de articulaciones (solo para pruebas sin robot real)
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher'
    )

    return LaunchDescription([
        robot_state_publisher,
        joint_state_publisher
    ])
EOF

cd ~/tfg_ws
colcon build --symlink-install
source install/setup.bash
ros2 launch abb_irb140_support rsp.launch.py
sudo apt install ros-jazzy-rosbridge-suite
cd ~/tfg_ws/src/abb_irb140_support/launch
cat <<EOF > interface.launch.py
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # 1. Localizar el launch del robot que ya creamos (rsp.launch.py)
    pkg_share = get_package_share_directory('abb_irb140_support')
    rsp_launch = os.path.join(pkg_share, 'launch', 'rsp.launch.py')

    # 2. Localizar el launch de Rosbridge (el servidor web)
    rosbridge_launch = os.path.join(
        get_package_share_directory('rosbridge_server'), 
        'launch', 
        'rosbridge_websocket_launch.xml'
    )

    return LaunchDescription([
        # Lanzar el Robot (Estado + TF)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(rsp_launch)
        ),
        # Lanzar el Servidor Web (Puerto 9090 por defecto)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(rosbridge_launch) # Nota: rosbridge usa XML o PY segun version, probamos XML primero
        )
    ])
EOF

cd ~/tfg_ws
colcon build --symlink-install
source install/setup.bash
ros2 launch abb_irb140_support interface.launch.py
cd ~/tfg_ws/src/abb_irb140_support/launch
cat <<EOF > interface.launch.py
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_xml.launch_description_sources import XmlLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # 1. Localizar el launch del robot (Python)
    pkg_share = get_package_share_directory('abb_irb140_support')
    rsp_launch = os.path.join(pkg_share, 'launch', 'rsp.launch.py')

    # 2. Localizar el launch de Rosbridge (XML)
    rosbridge_launch = os.path.join(
        get_package_share_directory('rosbridge_server'), 
        'launch', 
        'rosbridge_websocket_launch.xml'
    )

    return LaunchDescription([
        # Lanzar el Robot (Usa Python Source)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(rsp_launch)
        ),
        # Lanzar el Servidor Web (Usa XML Source - AQUI ESTABA EL ERROR)
        IncludeLaunchDescription(
            XmlLaunchDescriptionSource(rosbridge_launch)
        )
    ])
EOF

ros2 launch abb_irb140_support interface.launch.py
cd ~/tfg_ws/src/abb_irb140_support/launch
cat <<EOF > interface.launch.py
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # 1. Localizar el launch del robot (rsp.launch.py)
    pkg_share = get_package_share_directory('abb_irb140_support')
    rsp_launch = os.path.join(pkg_share, 'launch', 'rsp.launch.py')

    # 2. Configurar el Nodo Websocket directamente (Sin XML, sin errores)
    rosbridge_node = Node(
        package='rosbridge_server',
        executable='rosbridge_websocket',
        name='rosbridge_websocket',
        output='screen',
        parameters=[{'port': 9090}]
    )

    return LaunchDescription([
        # Lanzar primero el robot
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(rsp_launch)
        ),
        # Lanzar después el puente web
        rosbridge_node
    ])
EOF

ros2 launch abb_irb140_support interface.launch.py
hostname -I
sudo ufw allow 9090/tcp
cd ~/tfg_ws
source install/setup.bash
ros2 launch abb_irb140_support interface.launch.py
sudo apt update
sudo apt install ros-jazzy-moveit -y
sudo apt update
sudo apt install xauth -y
ls ~/tfg_ws/src/abb_irb140_support/urdf/
cd ~
rm -rf temp_rescue
git clone -b kinetic-devel https://github.com/ros-industrial/abb_experimental.git temp_rescue
# 1. Copiar los archivos de definición (URDF/Xacro)
cp -r ~/temp_rescue/abb_irb140_support/urdf/* ~/tfg_ws/src/abb_irb140_support/urdf/
# 2. Copiar las mallas 3D (¡Vital para que se vea bonito!)
cp -r ~/temp_rescue/abb_irb140_support/meshes/* ~/tfg_ws/src/abb_irb140_support/meshes/
# 3. Borrar lo temporal
rm -rf temp_rescue
cd ~
rm -rf temp_rescue
# Descargamos la rama 'kinetic-devel'
git clone -b kinetic-devel https://github.com/ros-industrial/abb_experimental.git temp_rescue
# 1. Asegurar que las carpetas de destino existen
mkdir -p ~/tfg_ws/src/abb_irb140_support/urdf
mkdir -p ~/tfg_ws/src/abb_irb140_support/meshes
# 2. Buscar y copiar los URDF/XACRO (Archivos de texto del robot)
find ~/temp_rescue -path "*/abb_irb140_support/urdf/*" -exec cp {} ~/tfg_ws/src/abb_irb140_support/urdf/ \;
# 3. Buscar y copiar las MESHES (Archivos 3D visuales)
find ~/temp_rescue -path "*/abb_irb140_support/meshes/*" -exec cp -r {} ~/tfg_ws/src/abb_irb140_support/meshes/ \;
ls ~/tfg_ws/src/abb_irb140_support/urdf/
# 1. Limpieza y Descarga
cd ~
rm -rf temp_rescue
git clone -b kinetic-devel https://github.com/ros-industrial/abb_experimental.git temp_rescue
# 2. DETECCIÓN AUTOMÁTICA (El Truco)
# Buscamos dónde está el archivo 'irb140.xacro' y guardamos esa ruta en una variable
CARPETA_URDF_ORIGEN=$(find ~/temp_rescue -name "irb140.xacro" -exec dirname {} \; | head -n 1)
# Buscamos dónde están las mallas visuales (.stl)
CARPETA_MESHES_ORIGEN=$(find ~/temp_rescue -name "visual" -type d | grep "abb_irb140_support" | head -n 1 | xargs dirname)
# 3. Copiado Inteligente (Usando las rutas detectadas)
echo "Copiando URDF desde: $CARPETA_URDF_ORIGEN"
cp -r "$CARPETA_URDF_ORIGEN"/* ~/tfg_ws/src/abb_irb140_support/urdf/
echo "Copiando Meshes desde: $CARPETA_MESHES_ORIGEN"
mkdir -p ~/tfg_ws/src/abb_irb140_support/meshes
cp -r "$CARPETA_MESHES_ORIGEN"/* ~/tfg_ws/src/abb_irb140_support/meshes/
# 4. Limpieza
rm -rf temp_rescue
# Borramos la carpeta del robot que se ha corrompido
rm -rf ~/tfg_ws/src/abb_irb140_support
nano ~/tfg_ws/instalar_irb140.sh
# Dar permisos y ejecutar
chmod +x ~/tfg_ws/instalar_irb140.sh
~/tfg_ws/instalar_irb140.sh
source ~/tfg_ws/install/setup.bash
xacro ~/tfg_ws/src/abb_irb140_support/urdf/irb140.xacro > ~/tfg_ws/src/abb_irb140_support/urdf/irb140_real.urdf
cat <<EOF > ~/tfg_ws/src/abb_irb140_support/urdf/irb140.xacro
<?xml version="1.0" ?>
<robot name="abb_irb140" xmlns:xacro="http://ros.org/wiki/xacro">
  <xacro:include filename="\$(find abb_irb140_support)/urdf/irb140_macro.xacro"/>
  <xacro:abb_irb140 prefix=""/>
</robot>
EOF

cat <<EOF > ~/tfg_ws/src/abb_irb140_support/urdf/irb140_macro.xacro
<?xml version="1.0"?>
<robot xmlns:xacro="http://ros.org/wiki/xacro">
  <xacro:macro name="abb_irb140" params="prefix">
    <link name="${prefix}base_link">
      <visual>
        <origin xyz="0 0 0" rpy="0 0 0"/>
        <geometry><mesh filename="package://abb_irb140_support/meshes/irb140/visual/base_link.stl"/></geometry>
        <material name="abb_orange"><color rgba="1 0.43 0 1"/></material>
      </visual>
      <collision>
        <origin xyz="0 0 0" rpy="0 0 0"/>
        <geometry><mesh filename="package://abb_irb140_support/meshes/irb140/collision/base_link.stl"/></geometry>
      </collision>
    </link>
    <link name="${prefix}link_1">
      <visual>
        <origin xyz="0 0 0" rpy="0 0 0"/>
        <geometry><mesh filename="package://abb_irb140_support/meshes/irb140/visual/link_1.stl"/></geometry>
        <material name="abb_orange"/>
      </visual>
      <collision>
        <origin xyz="0 0 0" rpy="0 0 0"/>
        <geometry><mesh filename="package://abb_irb140_support/meshes/irb140/collision/link_1.stl"/></geometry>
      </collision>
    </link>
    <link name="${prefix}link_2">
      <visual>
        <origin xyz="0 0 0" rpy="0 0 0"/>
        <geometry><mesh filename="package://abb_irb140_support/meshes/irb140/visual/link_2.stl"/></geometry>
        <material name="abb_orange"/>
      </visual>
      <collision>
        <origin xyz="0 0 0" rpy="0 0 0"/>
        <geometry><mesh filename="package://abb_irb140_support/meshes/irb140/collision/link_2.stl"/></geometry>
      </collision>
    </link>
    <link name="${prefix}link_3">
      <visual>
        <origin xyz="0 0 0" rpy="0 0 0"/>
        <geometry><mesh filename="package://abb_irb140_support/meshes/irb140/visual/link_3.stl"/></geometry>
        <material name="abb_orange"/>
      </visual>
      <collision>
        <origin xyz="0 0 0" rpy="0 0 0"/>
        <geometry><mesh filename="package://abb_irb140_support/meshes/irb140/collision/link_3.stl"/></geometry>
      </collision>
    </link>
    <link name="${prefix}link_4">
      <visual>
        <origin xyz="0 0 0" rpy="0 0 0"/>
        <geometry><mesh filename="package://abb_irb140_support/meshes/irb140/visual/link_4.stl"/></geometry>
        <material name="abb_orange"/>
      </visual>
      <collision>
        <origin xyz="0 0 0" rpy="0 0 0"/>
        <geometry><mesh filename="package://abb_irb140_support/meshes/irb140/collision/link_4.stl"/></geometry>
      </collision>
    </link>
    <link name="${prefix}link_5">
      <visual>
        <origin xyz="0 0 0" rpy="0 0 0"/>
        <geometry><mesh filename="package://abb_irb140_support/meshes/irb140/visual/link_5.stl"/></geometry>
        <material name="abb_orange"/>
      </visual>
      <collision>
        <origin xyz="0 0 0" rpy="0 0 0"/>
        <geometry><mesh filename="package://abb_irb140_support/meshes/irb140/collision/link_5.stl"/></geometry>
      </collision>
    </link>
    <link name="${prefix}link_6">
      <visual>
        <origin xyz="0 0 0" rpy="0 0 0"/>
        <geometry><mesh filename="package://abb_irb140_support/meshes/irb140/visual/link_6.stl"/></geometry>
        <material name="abb_black"><color rgba="0 0 0 1"/></material>
      </visual>
      <collision>
        <origin xyz="0 0 0" rpy="0 0 0"/>
        <geometry><mesh filename="package://abb_irb140_support/meshes/irb140/collision/link_6.stl"/></geometry>
      </collision>
    </link>

    <joint name="${prefix}joint_1" type="revolute">
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <parent link="${prefix}base_link"/>
      <child link="${prefix}link_1"/>
      <axis xyz="0 0 1"/>
      <limit lower="-3.1416" upper="3.1416" effort="0" velocity="2.618"/>
    </joint>
    <joint name="${prefix}joint_2" type="revolute">
      <origin xyz="0.070 0 0.352" rpy="0 0 0"/>
      <parent link="${prefix}link_1"/>
      <child link="${prefix}link_2"/>
      <axis xyz="0 1 0"/>
      <limit lower="-1.5708" upper="1.9198" effort="0" velocity="2.618"/>
    </joint>
    <joint name="${prefix}joint_3" type="revolute">
      <origin xyz="0 -0.065 0.360" rpy="0 0 0"/>
      <parent link="${prefix}link_2"/>
      <child link="${prefix}link_3"/>
      <axis xyz="0 1 0"/>
      <limit lower="-4.0142" upper="0.8726" effort="0" velocity="2.618"/>
    </joint>
    <joint name="${prefix}joint_4" type="revolute">
      <origin xyz="0.239 0.065 0" rpy="0 0 0"/>
      <parent link="${prefix}link_3"/>
      <child link="${prefix}link_4"/>
      <axis xyz="1 0 0"/>
      <limit lower="-3.4906" upper="3.4906" effort="0" velocity="6.2832"/>
    </joint>
    <joint name="${prefix}joint_5" type="revolute">
      <origin xyz="0.141 0 0" rpy="0 0 0"/>
      <parent link="${prefix}link_4"/>
      <child link="${prefix}link_5"/>
      <axis xyz="0 1 0"/>
      <limit lower="-2.0071" upper="2.0071" effort="0" velocity="6.2832"/>
    </joint>
    <joint name="${prefix}joint_6" type="revolute">
      <origin xyz="0.065 0 0" rpy="0 0 0"/>
      <parent link="${prefix}link_5"/>
      <child link="${prefix}link_6"/>
      <axis xyz="1 0 0"/>
      <limit lower="-6.9813" upper="6.9813" effort="0" velocity="7.854"/>
    </joint>
  </xacro:macro>
</robot>
EOF

source ~/tfg_ws/install/setup.bash
xacro ~/tfg_ws/src/abb_irb140_support/urdf/irb140.xacro > ~/tfg_ws/src/abb_irb140_support/urdf/irb140_real.urdf
cd ~/tfg_ws
colcon build --symlink-install
source install/setup.bash
xacro ~/tfg_ws/src/abb_irb140_support/urdf/irb140.xacro > ~/tfg_ws/src/abb_irb140_support/urdf/irb140_real.urdf
# 1. Asegurar que la carpeta de destino existe
mkdir -p ~/tfg_ws/install/abb_irb140_support/share/abb_irb140_support/urdf/
# 2. Copiar los archivos a la fuerza bruta
cp ~/tfg_ws/src/abb_irb140_support/urdf/* ~/tfg_ws/install/abb_irb140_support/share/abb_irb140_support/urdf/
# Cargar entorno por si acaso
source ~/tfg_ws/install/setup.bash
# Generar el URDF
xacro ~/tfg_ws/src/abb_irb140_support/urdf/irb140.xacro > ~/tfg_ws/src/abb_irb140_support/urdf/irb140_real.urdf
sudo apt update
sudo apt install xfce4 xfce4-goodies -y
sudo apt install xrdp -y
# Configurar la sesión
echo "xfce4-session" > ~/.xsession
# Reiniciar el servicio para aplicar cambios
sudo systemctl restart xrdp
sudo poweroff
# 1. Cargar el entorno de ROS
source ~/tfg_ws/install/setup.bash
# 2. Lanzar el Asistente de Configuración de MoveIt
ros2 launch moveit_setup_assistant setup_assistant.launch.py
source ~/tfg_ws/install/setup.bash
ros2 launch moveit_setup_assistant setup_assistant.launch.py
export LIBGL_ALWAYS_SOFTWARE=1
source ~/tfg_ws/install/setup.bash
ros2 launch moveit_setup_assistant setup_assistant.launch.py
ip a
sudo nano /etc/netplan/50-cloud-init.yaml
sudo netplan apply
sudo nmtui
nmcli c
sudo rm /etc/NetworkManager/system-connections/*
sudo reboot
