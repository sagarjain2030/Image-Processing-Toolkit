def function3_page(main_content, image):
    main_content.write("Inside function3 page")
    if image is not None:
        out = process_function3(image)
        main_content.image(out)
    else:
        main_content.write("No image received")