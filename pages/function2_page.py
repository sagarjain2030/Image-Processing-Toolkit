def function2_page(main_content, image):
    main_content.write("Inside function2 page")
    if image is not None:
        out = process_function2(image)
        main_content.image(out)
    else:
        main_content.write("No image received")