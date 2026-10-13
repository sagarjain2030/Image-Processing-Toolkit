from image_processing.process4_function import process_function4
from utils.ui_utils import load_image,get_image_formatted

def function4_page(main_content):
    main_content.write("Inside function4 page")
    uploaded_image = load_image(main_content=main_content, key="function4_uploader")
    image = get_image_formatted(uploaded_image)

    if image is not None:
        out = process_function4(image)
        main_content.image(out)
    else:
        main_content.write("No image received")