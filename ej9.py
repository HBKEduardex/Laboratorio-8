import cv2
import RPi.GPIO as GPIO
import time
import serial

# Configuración de GPIO
BUZZER_PIN = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.output(BUZZER_PIN, GPIO.LOW)

# Inicializar cámara
cap = cv2.VideoCapture(0)

# Inicializar Background Subtractor
fgbg = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=50, detectShadows=True)

# Inicializar UART
ser = serial.Serial('/dev/ttyACM0', 9600)  # Ajustar puerto si es necesario
ser.reset_input_buffer()

print("⏳ Inicializando fondo...")

# Capturar fondo inicial
for _ in range(60):
    ret, frame = cap.read()
    if ret:
        fgbg.apply(frame)
    time.sleep(0.05)

print("✅ Sistema de detección listo.")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Preprocesar
        fgmask = fgbg.apply(frame)
        fgmask = cv2.GaussianBlur(fgmask, (7, 7), 0)
        _, fgmask = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)

        fgmask = cv2.erode(fgmask, None, iterations=2)
        fgmask = cv2.dilate(fgmask, None, iterations=2)

        # Encontrar contornos
        contours, _ = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 500]

        num_objects = len(valid_contours)
        print(f"🔍 Objetos detectados: {num_objects}")

        # Dibujar contornos
        for cnt in valid_contours:
            cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)  # Verde

        # Mostrar el número de objetos
        cv2.putText(frame, f"Objetos: {num_objects}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Activar buzzer si detecta cualquier objeto
        if num_objects > 0:
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
        else:
            GPIO.output(BUZZER_PIN, GPIO.LOW)

        # Enviar mensajes por UART
        if num_objects > 1:
            ser.write(("objetos\n").encode('utf-8'))
            print("✅ Enviado: objetos")
        elif num_objects == 1:
            ser.write(("uno\n").encode('utf-8'))
            print("✅ Enviado: uno")
        # No se envía nada si no hay objetos

        # Mostrar cámaras
        cv2.imshow('Camara', frame)
        cv2.imshow('Movimiento', fgmask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\n🚪 Programa detenido por teclado.")

finally:
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()
    ser.close()
    print("✅ Sistema apagado correctamente.")
