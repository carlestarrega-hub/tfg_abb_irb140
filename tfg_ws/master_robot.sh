#!/bin/bash
# Script: master_robot.sh (VERSIÓN UNIVERSAL AUTOMÁTICA v3)
# Soporta: Wi-Fi Casa, Datos Móviles y Conexión Directa.

cleanup() {
    echo ""
    echo "🛑 APAGANDO SISTEMA..."
    pkill -P $$
    exit
}
trap cleanup SIGINT EXIT

clear
echo "=========================================="
echo "🤖 CONTROLADOR UNIVERSAL ABB IRB140"
echo "=========================================="
echo "Selecciona el modo de operación:"
echo "  1) 🎮 MODO SIMULACIÓN (PC/RobotStudio)"
echo "  2) 🦾 MODO REAL (Robot Físico)"
echo "=========================================="
read -p "Opción [1/2]: " OPCION

# 1. Cargamos el entorno de ROS 2
source ~/tfg_ws/install/setup.bash

PACKAGE_NAME="abb_irb140_moveit_config"
LAUNCH_FILE="demo.launch.py"

if [ "$OPCION" == "2" ]; then
    echo "🚀 INICIANDO MODO REAL..."
    DESTINO_IP="192.168.125.1"
    ros2 launch $PACKAGE_NAME $LAUNCH_FILE use_fake_hardware:=false robot_ip:=$DESTINO_IP &
else
    echo "🎮 INICIANDO MODO SIMULACIÓN..."
    
    # --- DETECCIÓN AUTOMÁTICA DE LA IP DEL PC ---
    # Paso A: Intentar por la variable de entorno SSH
    PC_IP_DETECTED=$(echo $SSH_CLIENT | grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b" | head -n 1)

    # Paso B: Si falla A, mirar quién está conectado al puerto 22 (Putty)
    if [ -z "$PC_IP_DETECTED" ]; then
        PC_IP_DETECTED=$(netstat -tn | grep ':22 ' | awk '{print $5}' | cut -d: -f1 | grep -v '127.0.0.1' | head -n 1)
    fi

    # Paso C: Si falla B, avisar al usuario
    if [ -z "$PC_IP_DETECTED" ]; then
        echo "⚠️  No detecto tu PC. Por favor, asegúrate de estar conectado por Putty."
        read -p "Introduce la IP de tu PC manualmente (ipconfig): " PC_IP_DETECTED
    fi
    # --------------------------------------------

    DESTINO_IP=$PC_IP_DETECTED
    echo "🔍 RobotStudio detectado en IP: $DESTINO_IP"
    ros2 launch $PACKAGE_NAME $LAUNCH_FILE use_fake_hardware:=true &
fi

echo "⏳ Esperando arranque de ROS..."
sleep 10

echo "🌐 [2/4] Levantando puente Web..."
ros2 run rosbridge_server rosbridge_websocket --ros-args -p address:=0.0.0.0 > /dev/null 2>&1 &

echo "🌐 [3/4] Iniciando Servidor Web (App)..."
cd ~/tfg_ws/src/abb_irb140_support
python3 app.py > /dev/null 2>&1 &

echo "🧠 [4/4] Activando Cerebro Digital..."
sleep 2
# Se le pasa la IP detectada automáticamente al script cerebro.py
python3 cerebro.py $DESTINO_IP &

MY_IP=$(hostname -I | awk '{print $1}')
echo "---------------------------------------------------"
echo "✅ SISTEMA LISTO Y SINCRONIZADO."
echo "👉 IP Raspberry: $MY_IP"
echo "👉 IP Destino:   $DESTINO_IP"
echo "👉 Puerto:       12000"
echo "---------------------------------------------------"
echo "."
wait
