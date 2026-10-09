def function1_page(main_content, image):
    main_content.write("Inside function1 page")
    if image is not None:
        out = process_function1(image)
        main_content.image(out)
    else:
        main_content.write("No image received")