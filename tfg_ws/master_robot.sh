#!/bin/bash
# Script: master_robot.sh (CORREGIDO FINAL)
# DÓNDE: En la Raspberry Pi 5

cleanup() {
    echo ""
    echo "🛑 APAGANDO SISTEMA..."
    # Mata todos los procesos hijos (ROS, Python, Bridge)
    pkill -P $$
    exit
}
trap cleanup SIGINT EXIT

clear
echo "=========================================="
echo "🤖 CONTROLADOR UNIVERSAL ABB IRB140"
echo "=========================================="
echo "Selecciona el modo de operación:"
echo "  1) 🎮 MODO SIMULACIÓN (Fake Hardware)"
echo "  2) 🦾 MODO REAL (Conexión Ethernet)"
echo "=========================================="
read -p "Opción [1/2]: " OPCION

# Cargamos el entorno de ROS 2
source ~/tfg_ws/install/setup.bash

# --- CONFIGURACIÓN DE LANZAMIENTO ---
# ⚠️ CORRECCIÓN IMPORTANTE:
# El archivo 'demo.launch.py' vive en la carpeta de configuración de MoveIt,
# NO en la carpeta de soporte.
PACKAGE_NAME="abb_irb140_moveit_config"
LAUNCH_FILE="demo.launch.py"
ROBOT_IP="192.168.125.1"

if [ "$OPCION" == "2" ]; then
    echo "🚀 INICIANDO MODO REAL..."
    
    # Comprobación de PING (Solo advertencia)
    if ! ping -c 1 -W 1 $ROBOT_IP &> /dev/null; then
        echo "⚠️  ADVERTENCIA: No detecto el robot en $ROBOT_IP"
        echo "   (Si estás en casa, esto es normal. Pulsa ENTER para probar el 'Dry Run')"
        read -p ""
    fi

    # LANZAMIENTO REAL
    # Usamos demo.launch.py pero forzamos que NO sea simulado
    ros2 launch $PACKAGE_NAME $LAUNCH_FILE use_fake_hardware:=false robot_ip:=$ROBOT_IP &

else
    echo "🎮 INICIANDO MODO SIMULACIÓN..."
    # LANZAMIENTO SIMULADO
    ros2 launch $PACKAGE_NAME $LAUNCH_FILE use_fake_hardware:=true &
fi

echo "⏳ Esperando 10 segundos a que arranque ROS..."
sleep 10

# --- SERVICIOS COMUNES ---

echo "bridge [2/4] Levantando puente Web..."
# Corregida la sintaxis de redirección de logs
ros2 run rosbridge_server rosbridge_websocket --ros-args -p address:=0.0.0.0 > /dev/null 2>&1 &

echo "🌐 [3/4] Iniciando Servidor Web..."
# Aseguramos que la ruta es correcta para tu app.py
cd ~/tfg_ws/src/abb_irb140_support
python3 app.py > /dev/null 2>&1 &

echo "🧠 [4/4] Activando Cerebro..."
sleep 2
# El cerebro también suele estar en support
cd ~/tfg_ws/src/abb_irb140_support/
python3 cerebro.py &

# --- INFO FINAL ---
MY_IP=$(hostname -I | awk '{print $1}')
echo "---------------------------------------------------"
echo "✅ SISTEMA LISTO."
echo "👉 En tu VM pon esta IP: $MY_IP"
echo "---------------------------------------------------"
# Mantenemos el script vivo para que el 'trap' funcione al salir
wait
