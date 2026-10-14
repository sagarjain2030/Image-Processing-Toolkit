from utils.ui_utils import load_image,get_image_formatted,get_image_download_bytes

def home_page(main_content):
    main_content.write("Inside Home Page")
    uploaded_image = load_image(main_content=main_content, key="homepage_uploader")
    image = get_image_formatted(uploaded_image)
    if image is not None:
        source_extension = uploaded_image.name.rsplit(".", 1)[-1].lower()
        main_content.image(image, channels="BGR")
        data = get_image_download_bytes(image,source_extension)
        file_name = f"output.{source_extension}"
        mime = "image/png" if source_extension == "png" else "image/jpeg"
        if data is not None:
            main_content.download_button(label="Download Output Image",data=data, file_name=file_name,mime=mime)
        else:
            main_content.write("No image received")