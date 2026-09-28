import numpy as np
import streamlit as st
from streamlit.logger import get_logger
import cv2

LOGGER = get_logger(__name__)

st.set_page_config (
    page_title="Image Processing Toolkit",
    layout="wide",
    initial_sidebar_state="expanded",
)

sidebar_dictionary = { "category1": ["Function1", "Function2"],
"category2": ["Function3", "Function4"]}


def create_main_content(main_content):
    main_content.write("This is where we show content")
    main_content.write("")
    main_content.write(st.session_state["Function"])
    uploaded_file = main_content.file_uploader(label="Upload an image",
                               type = ["png", "jpg","jpeg"],)
    if uploaded_file is not None:
        main_content.write(f"Name :{uploaded_file.name}" )
        main_content.write(f"Type :{uploaded_file.type}" )
        main_content.write(f"Size :{uploaded_file.size}")
        main_content.image(uploaded_file)
        image_bytes = uploaded_file.getvalue()
        main_content.write(type(image_bytes))
        main_content.write(len(image_bytes))
        image = np.frombuffer(image_bytes,dtype=np.uint8)
        main_content.write(type(image).__name__)
        main_content.write(image.dtype)
        main_content.write(image.size)
        main_content.write(image.shape)
        main_content.write(image.ndim)
        opencv_img = cv2.imdecode(image, cv2.IMREAD_COLOR)
        main_content.write(type(opencv_img).__name__)
        main_content.write(opencv_img.dtype)
        main_content.write(opencv_img.size)
        main_content.write(opencv_img.shape)
        main_content.write(opencv_img.ndim)


def run():
    header = st.container()
    header.title("Image Processing Toolkit")
    if "Function" not in st.session_state:
        st.session_state["Function"] = None
    add_sidebar_menu()
    main_content, doc_panel = st.columns([3, 1])
    create_main_content(main_content)

    doc_panel.write("It is document sidebar")

def on_click_function(string:str):
    st.session_state["Function"] = string

def add_sidebar_menu():
    st.sidebar.header("Functionalities")
    for key,values in sidebar_dictionary.items():
        with st.sidebar.expander(key, True):
            for value in values:
                st.button(label=value, on_click=on_click_function,args=(value,))

if __name__== "__main__":
    run()