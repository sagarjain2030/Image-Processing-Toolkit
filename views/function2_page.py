from image_processing.process2_function import process_function2
from utils.ui_utils import load_image,get_image_formatted

def function2_page(main_content):
    main_content.write("Inside function2 page")
    uploaded_image = load_image(main_content=main_content, key="function2_uploader")
    image = get_image_formatted(uploaded_image)

    if image is not None:
        out = process_function2(image)
        main_content.image(out)
    else:
        main_content.write("No image received")