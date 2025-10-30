import multiprocessing 
import time 
import os 
 
class ProcesadorImagenes: 
    def __init__(self): 
        self.imagenes_procesadas = multiprocessing.Value('i', 0) 
     
    def procesar_imagen(self, nombre_imagen, resultado_compartido): 
        """Simula el procesamiento de una imagen""" 
        print(f"Procesando {nombre_imagen} en proceso {os.getpid()}") 
         
        # Simular trabajo intensivo 
        tiempo_procesamiento = len(nombre_imagen) * 0.2 
        time.sleep(tiempo_procesamiento) 
         
        # Resultado del procesamiento (simulado) 
        tamaño_resultante = len(nombre_imagen) * 100 
        resultado_compartido.value = tamaño_resultante 
         
        # Contador compartido entre procesos 
        with self.imagenes_procesadas.get_lock(): 
            self.imagenes_procesadas.value += 1 
         
        print(f"{nombre_imagen} procesada. Tamaño: {tamaño_resultante}KB") 
        return tamaño_resultante 
 
def worker_procesar(procesador, nombre_imagen, resultado): 
    """Función wrapper para el proceso""" 
    procesador.procesar_imagen(nombre_imagen, resultado) 
 
# Configuración 
def main(): 
    procesador = ProcesadorImagenes() 
    imagenes = ["foto_familia.jpg", "selfie.png", "paisaje.tiff",  
                "documento.pdf", "captura_pantalla.png", "memes.jpg"] 
     
    procesos = [] 
    resultados = [] 
     
    print("Iniciando procesamiento distribuido de imágenes...") 
    inicio = time.time() 
     
    # Crear procesos para cada imagen 
    for i, imagen in enumerate(imagenes): 
        # Crear valor compartido para este proceso 
        resultado = multiprocessing.Value('i', 0) 
        resultados.append(resultado) 
         
        proceso = multiprocessing.Process( 
            target=worker_procesar,  
            args=(procesador, imagen, resultado) 
        ) 
        procesos.append(proceso) 
        proceso.start() 
     
    # Esperar a que todos terminen 
    for proceso in procesos: 
        proceso.join() 
     
    tiempo_total = time.time() - inicio 
     
    # Recopilar resultados 
    print(f"\nRESUMEN FINAL:") 
    print(f"Imágenes procesadas: {procesador.imagenes_procesadas.value}") 
    print(f"Tiempo total: {tiempo_total:.2f} segundos") 
    print(f"Tiempo secuencial estimado: {sum(len(img) for img in imagenes) * 0.2:.2f} segundos") 
     
    # Mostrar resultados individuales 
    for i, (imagen, resultado) in enumerate(zip(imagenes, resultados)): 
        print(f"  {imagen}: {resultado.value}KB") 
 
if __name__ == '__main__': 
    main()