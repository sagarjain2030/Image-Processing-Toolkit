def function4_page(main_content, image):
    main_content.write("Inside function4 page")
    if image is not None:
        out = process_function4(image)
        main_content.image(out)
    else:
        main_content.write("No image received")