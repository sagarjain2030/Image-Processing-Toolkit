from utils.ui_utils import load_image,get_image_formatted

def home_page(main_content):
    main_content.write("Inside Home Page")
    uploaded_image = load_image(main_content=main_content, key="homepage_uploader")
    image = get_image_formatted(uploaded_image)
    if image is not None:
        main_content.image(image)
    else:
        main_content.write("No image received")