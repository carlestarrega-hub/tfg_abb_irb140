import socket
import struct
import time
import concurrent.futures

puerto = 11000
ip_casa = "192.168.1.134" # Tu IP segura del PC

def probar_conexion(ip, puerto):
    """Intenta conectar a una IP específica muy rápido"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.2) 
        s.connect((ip, puerto))
        s.settimeout(None)
        return s, ip
    except:
        return None, None

def auto_conectar(puerto):
    """Busca al robot automáticamente en cualquier red"""
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

def mover_a_punto_exacto(s, joints, duracion=5.0): 
    ext = [9E9] * 6
    s.sendall(struct.pack('<I4i13f', 68, 10, 1, 0, 1, *[0]*6, *ext, 1.0))
    s.sendall(struct.pack('<I4i13f', 68, 10, 1, 0, 0, *joints, *ext, duracion))
    s.sendall(struct.pack('<I4i13f', 68, 10, 1, 0, 2, *[0]*6, *ext, 1.0))

try:
    # 🚀 Llama al escáner automático
    s = auto_conectar(puerto)
    print("\n🚀 Ejecutando Ejercicio 1 (16 puntos a alta velocidad).")

    trayectoria = [
        [-87.81, 63.08, 26.73, 0.00, 0.20, 92.19],   # Target_10
        [-44.75, 64.97, 11.39, 0.00, 13.64, 135.25], # Target_20
        [-36.38, 74.04, -17.79, 0.00, 33.75, 143.62],# Target_30
        [-31.92, 78.02, -27.88, 0.00, 39.85, 148.08],# Target_40
        [-30.25, 73.32, -15.88, 0.00, 32.55, 149.75],# Target_50
        [-28.31, 69.71, -5.60, 0.00, 25.89, 151.69], # Target_60
        [-24.04, 73.26, -15.72, 0.00, 32.45, 155.96],# Target_70
        [-14.48, 63.14, 24.32, 0.00, 2.53, 165.52],  # Target_80
        [-8.99, 76.61, -24.39, 0.00, 37.78, 171.01], # Target_90
        [10.88, 66.46, 5.25, 0.00, 18.30, 10.88],    # Target_100
        [29.99, 64.00, 16.53, 0.00, 9.47, 29.99],    # Target_110
        [19.47, 80.28, -33.30, 0.00, 43.03, 19.47],  # Target_120
        [87.89, 63.15, 24.27, 0.00, 2.58, -92.11],   # Target_130
        [52.24, 64.27, 14.94, 0.00, 10.79, -127.76], # Target_140
        [52.24, 64.27, 14.94, 0.00, 10.79, -127.76], # Target_150
        [36.74, 82.29, -38.01, 0.00, 45.72, -143.26] # Target_160
    ]

    for i, j_vals in enumerate(trayectoria):
        # offset_z = -5.0              
        # j_vals[1] = j_vals[1] + offset_z  
        # j_vals[4] = j_vals[4] - offset_z  
        
        print(f"📍 Moviendo a Target_{(i+1)*10}...")
        mover_a_punto_exacto(s, j_vals, duracion=5.0)
        time.sleep(6) # Pausa de 6s para asegurar la ejecución fluida

    print("\n🏠 Volviendo a posición inicial (Home)...")
    mover_a_punto_exacto(s, [0,0,0,0,0,0], duracion=5.0)
    time.sleep(6)

    s.close()
    print("🏁 Ejercicio 1 finalizado.")

except Exception as e:
    print(f"\n❌ Error Crítico: {e}")
