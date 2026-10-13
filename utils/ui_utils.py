import numpy as np
import cv2

def load_image(main_content,key):
    uploaded_file = main_content.file_uploader(label="Upload an image",
                               type = ["png", "jpg","jpeg"],key=key)
    return uploaded_file

def get_image_formatted(uploaded_file):
    if uploaded_file is not None:
        image_bytes = uploaded_file.getvalue()
        image = np.frombuffer(image_bytes, dtype=np.uint8)
        opencv_img = cv2.imdecode(image, cv2.IMREAD_COLOR)
        return opencv_img
    else:
        return None
