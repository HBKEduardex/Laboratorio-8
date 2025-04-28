import serial
import time
import RPi.GPIO as GPIO

# Configurar UART
ser = serial.Serial('/dev/ttyACM0', 9600)
ser.reset_input_buffer()

# Configurar pin PWM para el motor
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
motor_pwm_pin = 18  # Puedes cambiarlo si tu motor está en otro pin
GPIO.setup(motor_pwm_pin, GPIO.OUT)

pwm = GPIO.PWM(motor_pwm_pin, 1000)  # 1kHz de frecuencia
pwm.start(0)  # Motor inicialmente apagado

print("⏳ Esperando datos de la TIVA...")

try:
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            print(f"Mensaje recibido: {data}")

            if data == "verde":
                pwm.ChangeDutyCycle(100)  # Motor al 100%
                print("🚀 Motor al 100%")
            elif data == "amarillo":
                pwm.ChangeDutyCycle(25)   # Motor al 25%
                print("⚡ Motor al 25%")
            elif data == "rojo":
                pwm.ChangeDutyCycle(0)    # Motor apagado
                print("🛑 Motor detenido")

except KeyboardInterrupt:
    print("\nSaliendo del programa...")
    pwm.stop()
    GPIO.cleanup()
    ser.close()
