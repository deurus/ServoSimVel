import re
import numpy as np
import matplotlib.pyplot as plt
import os

# Ruta al archivo .m
ruta_archivo = "Steptest.m"

# Leer el contenido del archivo
with open(ruta_archivo, "r", encoding="utf-8") as f:
    contenido = f.read()

# Buscar el bloque que contiene los datos
coincidencias = re.findall(r"data\s*=\s*\[([\s\S]+?)\];", contenido)

if not coincidencias:
    raise ValueError("No se encontró el bloque de datos en el archivo.")

# Procesar las filas de datos
filas = coincidencias[0].strip().split("\n")
datos = np.array([[float(valor) for valor in fila.strip().split()] for fila in filas])

# Separar columnas
t, th, w, u, ref = datos.T

# Nombre del archivo de salida PNG (mismo nombre que el .m)
nombre_base = os.path.splitext(os.path.basename(ruta_archivo))[0]
nombre_png = f"{nombre_base}.png"

# Crear la gráfica (solo velocidad y control)
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(t, w, color='orange', label='PV')
plt.ylabel('PV (°/s)')
plt.legend()
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(t, u, color='green', label='OP')
plt.xlabel('Tiempo (s)')
plt.ylabel('OP (V)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig(nombre_png, dpi=300)
plt.close()

print(f"Gráfica guardada como {nombre_png}")
