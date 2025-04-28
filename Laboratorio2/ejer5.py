import cv2
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  
import matplotlib.pyplot as plt

class Contorno:
    def __init__(self, ruta):
        self.imagen=cv2.imread(ruta)

    def preprocesamiento(self):
        self.imagen_preprocesada1=cv2.cvtColor(self.imagen, cv2.COLOR_RGB2GRAY)
        self.imagen_preprocesada2=cv2.GaussianBlur(self.imagen,(15,15),0)

    def detectar_contornos(self):
        self.bordes=cv2.Canny(self.imagen_preprocesada2, 20,100)
        self.contornos, _ = cv2.findContours(self.bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #representación de los contornos más simple

    def dibujar_contorno(self):
        self.imagen_contorneada=self.imagen.copy()
        cv2.drawContours(self.imagen_contorneada, self.contornos, -1, (0, 255, 0), 2)

    def mostrar(self):
        plt.figure(figsize=(12,6))
        plt.subplot(1,3,1)
        plt.title('Original')
        plt.imshow(cv2.cvtColor(self.imagen, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.subplot(1,3,2)
        plt.title('Bordes (Canny)')
        plt.imshow(self.bordes, cmap='gray')
        plt.axis('off')
        plt.subplot(1,3,3)
        plt.title('Contornos')
        plt.imshow(cv2.cvtColor(self.imagen_contorneada, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.show()

    def run(self):
        self.preprocesamiento()
        self.detectar_contornos()
        self.dibujar_contorno()
        self.mostrar()
ruta= 'paris.jpg' 
detector = Contorno(ruta)
detector.run()