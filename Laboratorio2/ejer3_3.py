import cv2
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  
import matplotlib.pyplot as plt
import os

class capturas:
    def __init__(self,ruta):
        self.camara=cv2.VideoCapture(ruta)
        if not self.camara.isOpened():
            print("Error: No se pudo abrir el video.")
        self.contador=1
        if not os.path.exists('Capturas'):
            os.makedirs('Capturas')

    def guardar(self,frame):
        filename=f'Capturas/imagen{self.contador}.jpg'
        cv2.imwrite(filename,frame)
        print(f"la imagen se guardo como: {filename}")
        self.contador+=1

    def filtro (self,frame):
        frame_filtrado=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        alto, largo=frame_filtrado.shape
        c1=frame_filtrado[0:alto//2, 0:largo//2]
        c2=frame_filtrado[0:alto//2, largo//2:]
        c3=frame_filtrado[alto//2:, 0:largo//2]
        c4=frame_filtrado[alto//2:, largo//2:]
        return (c1,c2,c3,c4)
    
    def run(self):
        print("Presiona 's' para guardar la imagen, 'q' para salir.")
        
        while True:
            ret, frame=self.camara.read()
            if not ret:
                print ("No se puede leeer la camara")
                break
            frame = cv2.resize(frame, (600, 400))
            cv2.imshow('webcam', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('f'):  
                self.guardar(frame)
            elif key == ord('q'):  
                break
        if self.contador > 1:  
            ultima_imagen = cv2.imread(f'Capturas/imagen{self.contador-1}.jpg')
            cuadrante_1, cuadrante_2, cuadrante_3, cuadrante_4 = self.filtro(ultima_imagen)
            
            cv2.imshow('Cuadrante 1', cuadrante_1)
            cv2.imshow('Cuadrante 2', cuadrante_2)
            cv2.imshow('Cuadrante 3', cuadrante_3)
            cv2.imshow('Cuadrante 4', cuadrante_4)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        self.camara.release()
        cv2.destroyAllWindows()
ruta='peces1.mp4'
webcam=capturas(ruta)
webcam.run()
