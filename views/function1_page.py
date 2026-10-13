from image_processing.process1_function import process_function1
from utils.ui_utils import load_image,get_image_formatted

def function1_page(main_content):
    main_content.write("Inside function1 page")
    uploaded_image = load_image(main_content=main_content, key="function1_uploader")
    image = get_image_formatted(uploaded_image)

    if image is not None:
        out = process_function1(image)
        main_content.image(out)
    else:
        main_content.write("No image received")