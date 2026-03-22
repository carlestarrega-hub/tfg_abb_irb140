import socket
import time

# IP de tu portátil (el puente que acabamos de crear)
ip_de_tu_pc = "192.168.1.134"
puerto_motion = 11000

print(f"🔌 Intentando conectar a RobotStudio en el PC ({ip_de_tu_pc}:{puerto_motion})...")

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0) 
    
    s.connect((ip_de_tu_pc, puerto_motion))

    print("✅ ¡BINGO! Conexión TCP establecida desde la Raspberry Pi al PC.")
    print("🤖 El brazo virtual (Servidor) está escuchando.")
    print("⏳ Manteniendo la conexión abierta 5 segundos...")

    time.sleep(5)
    s.close()
    print("🏁 Prueba finalizada. Conexión cerrada correctamente.")

except Exception as e:
    print(f"❌ Error de conexión: {e}")
