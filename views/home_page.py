def home_page(main_content, image):
    main_content.write("Inside function1 page")
    if image is not None:
        main_content.image(image)
    else:
        main_content.write("No image received")