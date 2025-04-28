import cv2
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  
import matplotlib.pyplot as plt

class Video:
    def __init__(self, ruta):
        self.vidio= cv2.VideoCapture(ruta)

    def resize_frame(self,frame,largo=400,alto=600):
        return cv2.resize(frame,(largo,alto))
    
    def detect_edges(self,frame):
        return cv2.Canny(frame,100,200)
    
    def dividir(self,frame):
        alto, largo=frame.shape[:2]
        mitad_izquierda=frame[:, :largo//2]
        mitad_derecha=frame[:, largo//2:]
        return mitad_izquierda, mitad_derecha
    
    def cuadrantes(self,frame):
        alto, largo=frame.shape[:2]
        mitad_alto = alto // 2
        mitad_ancho = largo // 2
        cuadrante1 = frame[0:mitad_alto, 0:mitad_ancho]  # arriba izquierda
        cuadrante2 = frame[0:mitad_alto, mitad_ancho:largo]  # arriba derecha
        cuadrante3 = frame[mitad_alto:alto, 0:mitad_ancho]  # abajo izquierda
        cuadrante4 = frame[mitad_alto:alto, mitad_ancho:largo]  # abajo derecha
        return cuadrante1, cuadrante2, cuadrante3, cuadrante4
    
    def procesar_vidio(self):
        while True:
            ret, frame = self.vidio.read()
            if not ret:
                self.vidio.set(cv2.CAP_PROP_POS_FRAMES, 0)  
                continue

            cambio_escala= self.resize_frame(frame)
            detecion_bordes = self.detect_edges(cambio_escala)

            mitad_izquierda, mitad_derecha = self.dividir(cambio_escala)
            cuadrantes_final = self.cuadrantes(cambio_escala)

            # Mostrar ventanas
            cv2.imshow('Video original', frame)
            cv2.imshow('Video Redimensionado', cambio_escala)
            cv2.imshow('Bordes', detecion_bordes)
            cv2.imshow('Mitad Izquierda', mitad_izquierda)
            cv2.imshow('Mitad Derecha', mitad_derecha)
            cv2.imshow('Cuadrante 1', cuadrantes_final[0])
            cv2.imshow('Cuadrante 2', cuadrantes_final[1])
            cv2.imshow('Cuadrante 3', cuadrantes_final[2])
            cv2.imshow('Cuadrante 4', cuadrantes_final[3])

            if cv2.waitKey(30) & 0xFF == ord('q'):
                break

        self.vidio.release()
        cv2.waitKey(0)        
        cv2.destroyAllWindows()

processor = Video('peces1.mp4') 
processor.procesar_vidio()
