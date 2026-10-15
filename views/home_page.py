from utils.ui_utils import load_image,get_image_formatted,get_image_download_bytes

def home_page(main_content):
    main_content.title("Welcome to the Image Processing Toolkit")
    main_content.write(
        "Explore image processing concepts using Python, OpenCV, and NumPy. "
        "Upload an image to preview it, experiment with image processing operations, "
        "and download the output.")
    uploaded_image = load_image(main_content=main_content, key="homepage_uploader")
    if uploaded_image is None:
        main_content.info("Upload a JPG or PNG image to get started.")
        return
    image = get_image_formatted(uploaded_image)
    if image is None:
        main_content.error("Invalid image received")
        return
    source_extension = uploaded_image.name.rsplit(".", 1)[-1].lower()
    main_content.image(image, channels="BGR",  caption="This is the image you uploaded.")
    data = get_image_download_bytes(image,source_extension)
    file_name = f"output.{source_extension}"
    mime = "image/png" if source_extension == "png" else "image/jpeg"
    main_content.download_button(label="Download Output Image",data=data, file_name=file_name,mime=mime)