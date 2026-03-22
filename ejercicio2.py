import socket
import struct
import time
import concurrent.futures

puerto = 11000
ip_casa = "192.168.1.134" # Tu IP segura del PC

# ==========================================
# 🛠️ CALIBRACIÓN FINA (ALTURA CONSTANTE)
# ==========================================
inicio_z_alto = -20.0  
bajada_z_caja = 4.0    

avance_x_hombro = 1.0  # Ajuste para evitar hundimiento
avance_x_codo = -5.5   # Ajuste para levantar al estirar

# ==========================================
# 🤖 MOTOR DE AUTO-DESCUBRIMIENTO
# ==========================================
def probar_conexion(ip, puerto):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.2) 
        s.connect((ip, puerto))
        s.settimeout(None)
        return s, ip
    except:
        return None, None

def auto_conectar(puerto):
    print(f"🔍 1. Probando IP fija del PC ({ip_casa})...")
    s, ip = probar_conexion(ip_casa, puerto)
    if s: 
        print(f"✅ ¡Conectado por cable a {ip}!")
        return s

    print("⚠️ Fallo en IP fija. Iniciando rastreo de red dinámica...")
    
    try:
        s_temp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s_temp.connect(("8.8.8.8", 80))
        mi_ip = s_temp.getsockname()[0]
        s_temp.close()
    except:
        raise ConnectionError("❌ La Raspberry Pi no está conectada a ninguna red.")

    red_base = ".".join(mi_ip.split(".")[:-1]) + "."
    print(f"📡 2. Escaneando la red {red_base}X en busca del robot o PC...")

    ips_a_probar = [red_base + str(i) for i in range(1, 255) if red_base + str(i) != mi_ip]
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futuros = {executor.submit(probar_conexion, ip, puerto): ip for ip in ips_a_probar}
        for futuro in concurrent.futures.as_completed(futuros):
            s, ip_encontrada = futuro.result()
            if s:
                print(f"✅ ¡ENCONTRADO! -> Conectado a {ip_encontrada}")
                return s
                
    raise ConnectionError("❌ Rastreo fallido: Ningún dispositivo tiene el puerto 11000 abierto en esta red.")

def mover_a_punto_exacto(s, joints, duracion=5.0): # Velocidad aumentada
    ext = [9E9] * 6
    s.sendall(struct.pack('<I4i13f', 68, 10, 1, 0, 1, *[0]*6, *ext, 1.0))
    s.sendall(struct.pack('<I4i13f', 68, 10, 1, 0, 0, *joints, *ext, duracion))
    s.sendall(struct.pack('<I4i13f', 68, 10, 1, 0, 2, *[0]*6, *ext, 1.0))

# ==========================================
# 🚀 EJECUCIÓN DEL BUCLE PICK & PLACE
# ==========================================
try:
    s = auto_conectar(puerto)
    print("\n📦 Entregable 2: Pick & Place Rápido (Altura constante en Punto 8).")

    j_pick_base = [52.24, 64.27, 14.94, 0.00, 10.79, -127.76]
    j_place_base = [-14.48, 63.14, 24.32, 0.00, 2.53, 165.52]

    for i in range(5):
        print(f"\n🔄 --- CAJA {i+1} ---")
        
        # --- 📥 SENSOR 15 (Z DESCENDENTE) ---
        pos_z_actual = inicio_z_alto + (i * bajada_z_caja)
        j_pick_actual = [
            j_pick_base[0], 
            j_pick_base[1] + pos_z_actual, 
            j_pick_base[2], 
            j_pick_base[3], 
            j_pick_base[4] - pos_z_actual, 
            j_pick_base[5]
        ]
        print(f"📥 Sensor 15: Bajando por la columna...")
        mover_a_punto_exacto(s, j_pick_actual, duracion=5.0)
        time.sleep(6) # Ajuste de tiempo para movimiento más veloz

        # --- 📤 PUNTO 8 (X CONSTANTE EN Z) ---
        mod_j2 = i * avance_x_hombro
        mod_j3 = i * avance_x_codo
        
        j_place_actual = [
            j_place_base[0],
            j_place_base[1] + mod_j2, 
            j_place_base[2] + mod_j3, 
            j_place_base[3], 
            j_place_base[4] - (mod_j2 + mod_j3), # Mantiene la pinza horizontal
            j_place_base[5]
        ]
        print(f"📤 Punto 8: Estirando en X (J2: +{mod_j2}°, J3: {mod_j3}°)")
        mover_a_punto_exacto(s, j_place_actual, duracion=5.0)
        time.sleep(6)

    print("\n🏠 Volviendo a Home...")
    mover_a_punto_exacto(s, [0,0,0,0,0,0], duracion=5.0)
    time.sleep(6)

    s.close()
    print("🏁 Fin del ciclo.")

except Exception as e:
    print(f"\n❌ Error Crítico: {e}")
