import threading
import time
import random

class Banco:
    def __init__(self, saldo_inicial):
        self.saldo = saldo_inicial
        self.lock = threading.Lock()
    
    def retirar(self, cantidad, cliente_id):
        print(f"Cliente {cliente_id} intenta retirar ${cantidad}")

        # Implementar retiro seguro con lock
        with self.lock:
            print(f"--> Cliente {cliente_id} obtuvo el lock")
            
            if self.saldo >= cantidad:
                # Simular procesamiento
                time.sleep(0.1)
                self.saldo -= cantidad
                print(f"Cliente {cliente_id} retiró ${cantidad}. Saldo restante: ${self.saldo}")
                return True
            else:
                print(f"Cliente {cliente_id} - Fondos insuficientes")
                return False

def cliente(banco, cliente_id, retiros):
    for intento in range(retiros):
        cantidad = random.randint(50, 200)
        banco.retirar(cantidad, cliente_id)
        time.sleep(random.uniform(0.1, 0.3))

# Configuración
saldo_inicial = 1000
num_clientes = 5
retiros_por_cliente = 4

banco = Banco(saldo_inicial)
hilos = []

print(f"Saldo inicial: ${saldo_inicial}")

# Crear hilos para cada cliente
for i in range(num_clientes):
    hilo = threading.Thread(target=cliente, args=(banco, i, retiros_por_cliente))
    hilos.append(hilo)
    hilo.start()

# Esperar a que todos terminen
for hilo in hilos:
    hilo.join()

print(f"\nSaldo final: ${banco.saldo}")
print(f"Saldo teórico esperado: ${saldo_inicial - (num_clientes * retiros_por_cliente * 125)}")
