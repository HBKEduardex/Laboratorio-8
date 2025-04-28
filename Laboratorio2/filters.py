import cv2 as opencv
import matplotlib.pyplot as plt

class image_operations():
    def __init__(self, img):
        self.img = img
        self.o_image = opencv.imread(self.img)
    
    def grayscale(self):
        g_image = opencv.cvtColor(self.o_image, opencv.COLOR_BGR2GRAY)
        self.o_image = g_image
    
    def rgb(self):
        rgb_image = opencv.cvtColor(self.o_image, opencv.COLOR_BGR2RGB)
        self.o_image = rgb_image

    def show_image(self, header):
        if len(self.o_image.shape) == 2:
            plt.imshow(self.o_image, cmap='gray')
            plt.savefig('grayscale.png')
        else:
            self.rgb()
            plt.imshow(self.o_image)
            plt.savefig('rgb.png')

class threshold_versions(image_operations):
    def normal_threshold(self, th, max):
        _, n_thresh = opencv.threshold(self.o_image, th, max, opencv.THRESH_BINARY)
        plt.imshow(n_thresh, cmap='gray')
        plt.savefig('binary_thresh.png')

    def adaptive_threshold(self, max):
        a_thresh = opencv.adaptiveThreshold(self.o_image, max, opencv.ADAPTIVE_THRESH_GAUSSIAN_C, opencv.THRESH_BINARY, 17, 19)
        plt.imshow(a_thresh, cmap="gray")
        plt.savefig("adaptive_thresh.png")

apple_img = threshold_versions("mercedes.jpg")
apple_img.grayscale()
apple_img.normal_threshold(127,255)
apple_img.adaptive_threshold(255)