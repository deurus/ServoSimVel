import re
import numpy as np
import matplotlib.pyplot as plt
import os
from tkinter import Tk, filedialog

# --- OpenFileDialog para seleccionar el archivo .m ---
Tk().withdraw()
ruta_archivo = filedialog.askopenfilename(
    title="Selecciona el archivo .m",
    filetypes=[("Archivos MATLAB", "*.m")]
)

if not ruta_archivo:
    raise FileNotFoundError("No se seleccionó ningún archivo.")

# --- CONFIGURACIÓN ---
t_inicial = 37.5
t_final = 42.5

# Rango de operación
PV_min = -30
PV_max = 30
OP_min = -5
OP_max = 5

# Leer archivo
with open(ruta_archivo, "r", encoding="utf-8") as f:
    contenido = f.read()

coincidencias = re.findall(r"data\s*=\s*\[([\s\S]+?)\];", contenido)
if not coincidencias:
    raise ValueError("No se encontró el bloque de datos en el archivo.")

filas = coincidencias[0].strip().split("\n")
datos = np.array([[float(valor) for valor in fila.strip().split()] for fila in filas])
t, th, w, u, ref = datos.T

Ts = np.mean(np.diff(t))

mask = (t >= t_inicial) & (t <= t_final)
t_sel = t[mask]
w_sel = w[mask]
u_sel = u[mask]

delta_u = np.diff(u_sel)
idx_salto = np.where(np.abs(delta_u) > 0.1)[0]
if len(idx_salto) == 0:
    raise ValueError("No se detectó un escalón en el rango seleccionado.")

i_salto = idx_salto[0] + 1
t0 = t_sel[i_salto]
u_ini, u_fin = u_sel[i_salto - 1], u_sel[i_salto]
w_ini = w_sel[i_salto]
w_resp = w_sel[i_salto:]
t_resp = t_sel[i_salto:]

delta_u_val = u_fin - u_ini
delta_w_val = w_resp[-1] - w_ini
Kp = delta_w_val / delta_u_val
Kp_norm = (delta_w_val / (PV_max - PV_min)) / (delta_u_val / (OP_max - OP_min))

PV28 = w_ini + 0.283 * delta_w_val
PV63 = w_ini + 0.632 * delta_w_val

idx_t1 = np.argmax(w_resp > PV28)
idx_t2 = np.argmax(w_resp > PV63)

T1_abs = t0 + idx_t1 * Ts
T2_abs = t0 + idx_t2 * Ts

Tp = 1.5 * (T2_abs - T1_abs)
T0_abs = T2_abs - Tp
T0_rel = T0_abs - t0
T0_mostrar = Ts if T0_rel < 3 * Ts else T0_rel

# Sintonías Lambda
Ti = Tp
Tf1, Tf2, Tf3 = 4 * Tp, 10 * Tp, 20 * Tp

# PI
Kc_PI_1 = Tp / (Kp_norm * (Tf1 + T0_mostrar))
Kc_PI_2 = Tp / (Kp_norm * (Tf2 + T0_mostrar))
Kc_PI_3 = Tp / (Kp_norm * (Tf3 + T0_mostrar))

# PID
Kc_PID_1 = (Tp / (Kp_norm * (Tf1 + T0_mostrar))) * ((Tf1 + T0_mostrar) / (Tf1 + 0.5 * T0_mostrar))
Td1 = (T0_mostrar * Tf1) / (Tf1 + 0.5 * T0_mostrar)

Kc_PID_2 = (Tp / (Kp_norm * (Tf2 + T0_mostrar))) * ((Tf2 + T0_mostrar) / (Tf2 + 0.5 * T0_mostrar))
Td2 = (T0_mostrar * Tf2) / (Tf2 + 0.5 * T0_mostrar)

Kc_PID_3 = (Tp / (Kp_norm * (Tf3 + T0_mostrar))) * ((Tf3 + T0_mostrar) / (Tf3 + 0.5 * T0_mostrar))
Td3 = (T0_mostrar * Tf3) / (Tf3 + 0.5 * T0_mostrar)

# GRAFICAR
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(t_sel, w_sel, label='PV', color='orange')
plt.axvline(t0, color='gray', linestyle='--', label='Escalón')
plt.axvline(T1_abs, color='blue', linestyle=':', label='T1 (PV28.3%)')
plt.axvline(T2_abs, color='red', linestyle=':', label='T2 (PV63.2%)')
plt.axhline(PV28, color='blue', linestyle='--')
plt.axhline(PV63, color='red', linestyle='--')
plt.ylabel('PV (°/s)')
plt.legend()
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(t_sel, u_sel, label='OP', color='green')
plt.xlabel('Tiempo (s)')
plt.ylabel('OP (V)')
plt.grid(True)
plt.legend()
plt.tight_layout()

# Guardar archivos
base_name = os.path.splitext(os.path.basename(ruta_archivo))[0]
nombre_base = f"{base_name}_identificado"
plt.savefig(f"{nombre_base}.png", dpi=300)
plt.close()

# TXT
with open(f"{nombre_base}.txt", "w", encoding="utf-8") as ftxt:
    ftxt.write("------------------------------------------------------------\n")
    ftxt.write("ACLARACIÓN SOBRE UNIDADES Y NORMALIZACIÓN\n")
    ftxt.write("------------------------------------------------------------\n")
    ftxt.write("- El modelo del sistema se identifica en unidades de ingeniería reales:\n")
    ftxt.write("    * Velocidad (PV) en grados/segundo [°/s]\n")
    ftxt.write("    * Señal de control (OP) en voltios [V]\n")
    ftxt.write("    * Tiempos en segundos [s]\n")
    ftxt.write("- Para calcular las sintonías, se normaliza usando %/%\n")
    ftxt.write("------------------------------------------------------------\n\n")

    ftxt.write("--CÁLCULOS--\n")
    ftxt.write(f"ΔOP = {delta_u_val:.3f} V\n")
    ftxt.write(f"ΔPV = {delta_w_val:.3f} °/s\n")
    ftxt.write(f"PV28 = {PV28:.3f} °/s\n")
    ftxt.write(f"PV63 = {PV63:.3f} °/s\n")
    ftxt.write(f"T1 = {T1_abs:.4f} s\n")
    ftxt.write(f"T2 = {T2_abs:.4f} s\n")
    ftxt.write(f"T0 absoluto = {T0_abs:.4f} s\n\n")

    ftxt.write("--SISTEMA--\n")
    ftxt.write(f"Kp_EU  = {Kp:.4f}\n")
    ftxt.write(f"Kp_%/% = {Kp_norm:.4f}\n")
    ftxt.write(f"T0 = {T0_mostrar:.4f} s (tiempo muerto desde el escalón)\n")
    ftxt.write(f"Tp = {Tp:.4f} s\n\n")

    ftxt.write("--SINTONÍA LAMBDA--\n")
    ftxt.write(f"Kc = {Kc_PI_1:.4f}, Ti = {Tp:.4f} Td = 0 (Tp*4)\n")
    ftxt.write(f"Kc = {Kc_PI_2:.4f}, Ti = {Tp:.4f} Td = 0 (Tp*10)\n")
    ftxt.write(f"Kc = {Kc_PI_3:.4f}, Ti = {Tp:.4f} Td = 0 (Tp*20)\n\n")

    ftxt.write(f"Kc = {Kc_PID_1:.4f}, Ti = {Tp:.4f} Td = {Td1:.4f} (Tp*4)\n")
    ftxt.write(f"Kc = {Kc_PID_2:.4f}, Ti = {Tp:.4f} Td = {Td2:.4f} (Tp*10)\n")
    ftxt.write(f"Kc = {Kc_PID_3:.4f}, Ti = {Tp:.4f} Td = {Td3:.4f} (Tp*20)\n")

print(f"Archivos generados: {nombre_base}.png y {nombre_base}.txt")
