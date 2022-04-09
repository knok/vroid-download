#
import cv2
import numpy as np
import PIL

class FaceDetector:
    def __init__(self) -> None:
        self.cascade = cv2.CascadeClassifier("lbpcascade_animeface.xml")

    def detect_faces(self, image, scaleFactor=1.1, minNeighbors=5, minSize=(24, 24)):
        if isinstance(image, PIL.Image.Image):
            gray_image = self.pil2cv2gray(image)
        else:
            gray_image = image
        faces = self.cascade.detectMultiScale(gray_image,
            scaleFactor=scaleFactor, minNeighbors=minNeighbors,
            minSize=minSize)
        return faces

    def pil2cv2gray(self, image):
        img = np.array(image, dtype=np.uint8)
        # cvimg = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        img = img[:, :, ::-1]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        return gray

    def extend_face_pos(self, x, y, w, h, rate=1.1):
        new_w = w * rate
        new_h = h * rate
        diff_x = w * rate - w
        diff_y = h * rate - h
        new_x = x - (diff_x // 2)
        new_y = y - (diff_y // 2)
        ret = filter(int, [new_x, new_y, new_w, new_h])
        return ret
