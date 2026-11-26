import platform
import psutil

print("=" * 45)
print("WOLF SYSTEM DIAGNOSTIC V1.1")
print("=" * 45)

print("\n[SISTEMA OPERACIONAL]")
print("Sistema:", platform.system())
print("Versao:", platform.release())
print("Arquitetura:", platform.machine())

print("\n[PROCESSADOR]")
print("Processador:", platform.processor())
print("Nucleos fisicos:", psutil.cpu_count(logical=False))
print("Nucleos logicos:", psutil.cpu_count())
print("Uso da CPU:", psutil.cpu_percent(interval=1), "%")

print("\n[MEMORIA RAM]")
ram = psutil.virtual_memory()
print(f"Total: {ram.total / 1024**3:.2f} GB")
print(f"Disponivel: {ram.available / 1024**3:.2f} GB")
print(f"Uso da RAM: {ram.percent}%")

print("\n[ARMAZENAMENTO]")
disco = psutil.disk_usage("C:\\")
print(f"Total: {disco.total / 1024**3:.2f} GB")
print(f"Utilizado: {disco.used / 1024**3:.2f} GB")
print(f"Livre: {disco.free / 1024**3:.2f} GB")
print(f"Uso do disco: {disco.percent}%")

print("\n" + "=" * 45)
print("Diagnostico concluido!")