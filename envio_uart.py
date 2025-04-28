import serial
import time

# Configurar UART
ser = serial.Serial('/dev/ttyACM0', 9600)
ser.reset_input_buffer()

print("=== MENÚ DE ENVÍO ===")
print("1. Enviar palabra 'objetos'")
print("2. Enviar palabra 'uno'")
opcion = input("Selecciona una opción (1/2): ")

if opcion == "1":
    ser.write(("objetos\n").encode('utf-8'))
    print("✅ Enviado: objetos")
elif opcion == "2":
    ser.write(("uno\n").encode('utf-8'))
    print("✅ Enviado: uno")
else:
    print("❌ Opción no válida.")

ser.close()
