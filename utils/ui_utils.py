import numpy as np
import cv2

def load_image(main_content,key):
    uploaded_file = main_content.file_uploader(label="Upload an image",
                               type = ["png", "jpg","jpeg"],key=key)
    return uploaded_file

def get_image_formatted(uploaded_file):
    image_bytes = None
    if uploaded_file is not None:
        image_bytes = uploaded_file.getvalue()
    if image_bytes:
        image = np.frombuffer(image_bytes, dtype=np.uint8)
        opencv_img = cv2.imdecode(image, cv2.IMREAD_COLOR)
        return opencv_img
    else :
        return None

def get_image_download_bytes(img, extension):
    extension = extension.lower().lstrip(".")
    if extension not in ("png", "jpg", "jpeg"):
        raise ValueError("Unsupported output image format")
    success, encoded_img = cv2.imencode("." + extension, img)
    if not success:
        raise ValueError("Failed to encode image for download")
    return encoded_img.tobytes()