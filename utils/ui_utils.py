import numpy as np
import cv2

def get_image_formatted(uploaded_file):
    image_bytes = uploaded_file.getvalue()
    image = np.frombuffer(image_bytes, dtype=np.uint8)
    opencv_img = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return opencv_img
