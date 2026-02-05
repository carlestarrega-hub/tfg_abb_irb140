#!/bin/bash
# Script: master_robot.sh (CORREGIDO)
# DÓNDE: En la Raspberry Pi 5

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
echo "  1) 🎮 MODO SIMULACIÓN (Fake Hardware)"
echo "  2) 🦾 MODO REAL (Conexión Ethernet)"
echo "=========================================="
read -p "Opción [1/2]: " OPCION

source ~/tfg_ws/install/setup.bash

# --- CONFIGURACIÓN DE LANZAMIENTO ---
# ⚠️ CORRECCIÓN 1: Cambiado 'abb_control' por 'abb_irb140_support'
# Si tu archivo production.launch.py tiene otro nombre, cámbialo aquí abajo.
PACKAGE_NAME="abb_irb140_support" 
LAUNCH_FILE="production.launch.py"

if [ "$OPCION" == "2" ]; then
    echo "🚀 INICIANDO MODO REAL..."
    ROBOT_IP="192.168.125.1"
    
    if ! ping -c 1 -W 1 $ROBOT_IP &> /dev/null; then
        echo "⚠️  ADVERTENCIA: No detecto el robot en $ROBOT_IP"
        read -p "    Pulsa ENTER para continuar igual..."
    fi

    ros2 launch $PACKAGE_NAME $LAUNCH_FILE use_fake_hardware:=false robot_ip:=$ROBOT_IP &
else
    echo "🎮 INICIANDO MODO SIMULACIÓN..."
    # Intenta lanzar el production, si falla, avísame
    ros2 launch $PACKAGE_NAME $LAUNCH_FILE use_fake_hardware:=true &
fi

echo "⏳ Esperando 10 segundos..."
sleep 10

# --- SERVICIOS COMUNES ---

echo "bridge [2/4] Levantando puente Web..."
ros2 run rosbridge_server rosbridge_websocket --ros-args -p address:=0.0.0.0 > /dev/null 2>&1 &

echo "🌐 [3/4] Iniciando Servidor Web..."
# CAMBIO: Entramos en la carpeta support (donde está app.py), NO en web
cd ~/tfg_ws/src/abb_irb140_support
python3 app.py > /dev/null 2>&1 &

echo "🧠 [4/4] Activando Cerebro..."
sleep 2
cd ~/tfg_ws/src/abb_irb140_support/
python3 cerebro.py &

# --- INFO FINAL ---
MY_IP=$(hostname -I | awk '{print $1}')
echo "---------------------------------------------------"
echo "✅ SISTEMA LISTO."
echo "👉 En tu VM pon esta IP: $MY_IP"
echo "---------------------------------------------------"
wait
