#Codigo completo  con integra Pool + Hilos + Progreso + Comparación

import multiprocessing
import threading
import time
import os
import sys

# --- Procesamiento con PROCESOS ---
def procesar_imagen_proceso(nombre_imagen, contador, total):
    tiempo_procesamiento = len(nombre_imagen) * 0.2
    time.sleep(tiempo_procesamiento)
    tamaño_resultante = len(nombre_imagen) * 100

    # El Manager maneja la sincronización, no usar get_lock()
    contador.value += 1
    progreso = (contador.value / total) * 100
    sys.stdout.write(f"\r[PROCESOS] Progreso: {progreso:.1f}% ({contador.value}/{total})")
    sys.stdout.flush()

    return (nombre_imagen, tamaño_resultante)

# --- Procesamiento con HILOS ---
def procesar_imagen_hilo(nombre_imagen, procesador):
    tiempo_procesamiento = len(nombre_imagen) * 0.2
    time.sleep(tiempo_procesamiento)
    tamaño_resultante = len(nombre_imagen) * 100
    with procesador['lock']:
        procesador['procesadas'] += 1
        progreso = (procesador['procesadas'] / procesador['total']) * 100
        sys.stdout.write(f"\r[HILOS] Progreso: {progreso:.1f}% ({procesador['procesadas']}/{procesador['total']})")
        sys.stdout.flush()
    return (nombre_imagen, tamaño_resultante)

def ejecutar_con_procesos(imagenes):
    total = len(imagenes)
    manager = multiprocessing.Manager()
    contador = manager.Value('i', 0)  # ✅ proxy compartido compatible
    inicio = time.time()

    with multiprocessing.Pool(processes=4) as pool:
        resultados_async = [
            pool.apply_async(procesar_imagen_proceso, args=(img, contador, total))
            for img in imagenes
        ]
        resultados = [r.get() for r in resultados_async]

    print(f"\n\n[PROCESOS] Tiempo total: {time.time() - inicio:.2f} s")
    return resultados

def ejecutar_con_hilos(imagenes):
    procesador = {'procesadas': 0, 'lock': threading.Lock(), 'total': len(imagenes)}
    resultados = []
    inicio = time.time()

    hilos = [threading.Thread(target=lambda img=img: resultados.append(procesar_imagen_hilo(img, procesador))) for img in imagenes]
    for hilo in hilos: hilo.start()
    for hilo in hilos: hilo.join()

    print(f"\n\n[HILOS] Tiempo total: {time.time() - inicio:.2f} s")
    return resultados

# --- Principal ---
def main():
    imagenes = [
        "foto_familia.jpg",
        "selfie.png",
        "paisaje.tiff",
        "documento.pdf",
        "captura_pantalla.png",
        "memes.jpg"
    ]

    print("Iniciando comparación de rendimiento...\n")

    resultados_proc = ejecutar_con_procesos(imagenes)
    resultados_hilos = ejecutar_con_hilos(imagenes)

    print("\n--- RESUMEN FINAL ---")
    print(f"Procesos: {len(resultados_proc)} imágenes procesadas")
    print(f"Hilos: {len(resultados_hilos)} imágenes procesadas")

if __name__ == "__main__":
    multiprocessing.freeze_support()  # 🔒 Necesario en Windows
    main()
