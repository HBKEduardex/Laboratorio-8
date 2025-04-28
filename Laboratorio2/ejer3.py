import cv2
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  
import os

class capturas:
    def __init__(self):
        self.camara = cv2.VideoCapture(0)
        self.contador = 1
        if not os.path.exists('Capturas'):
            os.makedirs('Capturas')

    def guardar(self, frame):
        filename = f'Capturas/imagen{self.contador}.jpg'
        cv2.imwrite(filename, frame)
        print(f"la imagen se guardo como: {filename}")
        self.contador += 1

    def filtro(self, frame):
        frame_filtrado = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        alto, largo = frame_filtrado.shape
        c1 = frame_filtrado[0:alto//2, 0:largo//2]
        c2 = frame_filtrado[0:alto//2, largo//2:]
        c3 = frame_filtrado[alto//2:, 0:largo//2]
        c4 = frame_filtrado[alto//2:, largo//2:]
        return (c1, c2, c3, c4)

    def mostrar_cuadrantes(self, c1, c2, c3, c4):
        fig, axs = plt.subplots(2, 2)
        axs[0, 0].imshow(c1, cmap='gray')
        axs[0, 0].set_title('Cuadrante 1')
        axs[0, 1].imshow(c2, cmap='gray')
        axs[0, 1].set_title('Cuadrante 2')
        axs[1, 0].imshow(c3, cmap='gray')
        axs[1, 0].set_title('Cuadrante 3')
        axs[1, 1].imshow(c4, cmap='gray')
        axs[1, 1].set_title('Cuadrante 4')

        for ax in axs.flat:
            ax.axis('off')
        plt.tight_layout()
        plt.show()

    def run(self):
        print("Presiona 'f' para guardar la imagen, 'q' para salir.")
        while True:
            ret, frame = self.camara.read()
            if not ret:
                print("No se puede leer la cámara.")
                break
            cv2.imshow('webcam', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('f'):
                self.guardar(frame)
            elif key == ord('q'):
                break

        self.camara.release()
        cv2.destroyAllWindows()

        if self.contador > 1:
            path_imagen = f'Capturas/imagen{self.contador - 1}.jpg'
            ultima_imagen = cv2.imread(path_imagen)
            if ultima_imagen is None:
                print(f"No se pudo cargar la imagen: {path_imagen}")
                return
            c1, c2, c3, c4 = self.filtro(ultima_imagen)
            self.mostrar_cuadrantes(c1, c2, c3, c4)

webcam = capturas()
webcam.run()

