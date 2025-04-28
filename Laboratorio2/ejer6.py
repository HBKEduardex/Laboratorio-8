import cv2
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

class ContornoWebcam:
    def __init__(self):
        self.camara = cv2.VideoCapture(0)

    def preprocesamiento(self, imagen):
        imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        imagen_desfoque = cv2.GaussianBlur(imagen_gris, (19, 19), 0)
        return imagen_desfoque

    def detectar_contornos(self, imagen):
        bordes = cv2.Canny(imagen, 20, 50)
        contornos, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return bordes, contornos

    def dibujar_contornos(self, imagen, contornos):
        imagen_contorneada = imagen.copy()
        cv2.drawContours(imagen_contorneada, contornos, -1, (0, 255, 0), 2) 
        return imagen_contorneada

    def run(self):
        print("Detectando contornos en tiempo real. Presiona 'q' para salir.")
        
        while True:
            ret, frame = self.camara.read()
            if not ret:
                print("No se puede leer la cámara.")
                break

            imagen_preprocesada = self.preprocesamiento(frame)
            
            bordes, contornos = self.detectar_contornos(imagen_preprocesada)
            
            imagen_contorneada = self.dibujar_contornos(frame, contornos)

            # Mostrar las tres imágenes: original, bordes (Canny) y contornos
            cv2.imshow('Webcam - Contornos', imagen_contorneada)
            cv2.imshow('Bordes Canny', bordes)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.camara.release()
        cv2.destroyAllWindows()

detector_webcam = ContornoWebcam()
detector_webcam.run()

