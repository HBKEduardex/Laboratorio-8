import cv2
import RPi.GPIO as GPIO
import time

# Configuración
BUZZER_PIN = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.output(BUZZER_PIN, GPIO.LOW)

# Inicializar cámara
cap = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=50, detectShadows=True)

print("⏳ Inicializando fondo...")

# Estabilizar fondo
for _ in range(60):
    ret, frame = cap.read()
    if ret:
        fgbg.apply(frame)
    time.sleep(0.05)

print("✅ Fondo capturado. Sistema listo.")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Preprocesar imagen
        fgmask = fgbg.apply(frame)
        fgmask = cv2.GaussianBlur(fgmask, (7, 7), 0)
        _, fgmask = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)

        # Eliminar pequeños ruidos
        fgmask = cv2.erode(fgmask, None, iterations=2)
        fgmask = cv2.dilate(fgmask, None, iterations=2)

        # Contar píxeles blancos (movimiento)
        white_pixels = cv2.countNonZero(fgmask)

        # Umbral mucho más alto
        threshold = 15000

        if white_pixels > threshold:
            print("⚡ ¡Movimiento REAL detectado!")
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
        else:
            GPIO.output(BUZZER_PIN, GPIO.LOW)

        # Mostrar ventanas
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
    print("✅ Sistema apagado correctamente.")
