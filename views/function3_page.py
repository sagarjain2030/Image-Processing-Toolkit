from image_processing.process3_function import process_function3
from utils.ui_utils import load_image,get_image_formatted

def function3_page(main_content):
    main_content.write("Inside function3 page")
    uploaded_image = load_image(main_content=main_content, key="function3_uploader")
    image = get_image_formatted(uploaded_image)

    if image is not None:
        out = process_function3(image)
        main_content.image(out)
    else:
        main_content.write("No image received")