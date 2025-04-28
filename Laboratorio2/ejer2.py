import cv2
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  
import matplotlib.pyplot as plt

class camara_filtro:
    def __init__(self):
        self.camara = cv2.VideoCapture(0)
        self.selecion_filtro = 'normal'

    def aplicar_filtro(self, frame):
        if self.selecion_filtro == 'grayscale':
            return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        elif self.selecion_filtro == 'canny':
            return cv2.Canny(frame, 100, 200)
        elif self.selecion_filtro == 'blur':
            return cv2.GaussianBlur(frame, (15, 15), 0)
        else:
            return frame

    def run(self):
        print("Presiona 'g' para Grayscale, 'c' para Canny, 'b' para Blur, 'n' para Normal, 'q' para salir.")
        
        while True:  # El 'true' debe ser 'True' con mayúscula
            ret, frame = self.camara.read()
            if not ret:
                print("no se puede prender la camara")
                break
            filtrado = self.aplicar_filtro(frame)
            cv2.imshow('camara :)', filtrado)
            
            key = cv2.waitKey(1) & 0xFF  # Esta línea debe estar dentro del bucle while
            if key == ord('q'):
                break
            elif key == ord('g'):
                self.selecion_filtro = 'grayscale'
            elif key == ord('c'):
                self.selecion_filtro = 'canny'
            elif key == ord('b'):
                self.selecion_filtro = 'blur'
            elif key == ord('n'):
                self.selecion_filtro = 'normal'

        self.camara.release()
        cv2.destroyAllWindows()

aux = camara_filtro()
aux.run()
