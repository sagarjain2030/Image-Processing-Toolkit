import streamlit as st
from streamlit.logger import get_logger

from utils.constants import sidebar_dictionary,function_dictionary, doc_file_dictionary
from utils.ui_utils import get_image_formatted

LOGGER = get_logger(__name__)

def define_configs():
    st.set_page_config (
        page_title="Image Processing Toolkit",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    if "Function" not in st.session_state:
        st.session_state["Function"] = "Home"

def set_homepage():
    header = st.container()
    header.title("Image Processing Toolkit")

def create_main_content(main_content):
    main_content.write("This is where we show content")
    main_content.write("")
    uploaded_file = main_content.file_uploader(label="Upload an image",
                               type = ["png", "jpg","jpeg"],)
    opencv_img = None
    if uploaded_file is not None:
        opencv_img = get_image_formatted(uploaded_file)
        if opencv_img is None:
            main_content.write("Could not decode the uploaded image")
        else:
            main_content.write(type(opencv_img).__name__)
            main_content.write(opencv_img.dtype)
            main_content.write(opencv_img.size)
            main_content.write(opencv_img.shape)
            main_content.write(opencv_img.ndim)
    if st.session_state["Function"] is not None:
        main_content.write(st.session_state["Function"])
        try :
            s = function_dictionary[st.session_state["Function"]]
        except KeyError :
            main_content.write("Could not find function")
        else:
            s(main_content, opencv_img)

def load_documentation(file_path):
    try:
        with open(file_path) as f:
            return f.read()
    except FileNotFoundError:
        return "### File not found"

def create_doc_content(doc_panel):
    doc_panel.write("It is document sidebar")
    if st.session_state["Function"] is not None:
        text = load_documentation("docs/" + doc_file_dictionary[st.session_state["Function"]])
        doc_panel.markdown(text)
    else:
        text = load_documentation("docs/home.md")
        doc_panel.markdown(text)

def on_click_function(string:str,):
    st.session_state["Function"] = string

def add_sidebar_menu():
    st.sidebar.header("Functionalities")
    st.sidebar.button(label="Home", on_click=on_click_function,args=("Home",))
    for key,values in sidebar_dictionary.items():
        with st.sidebar.expander(key, True):
            for value in values:
                st.button(label=value, on_click=on_click_function,args=(value,))

def run():
    define_configs()
    set_homepage()
    main_content, doc_panel = st.columns([3, 1])
    add_sidebar_menu()
    create_main_content(main_content)
    create_doc_content(doc_panel)

if __name__== "__main__":
    run()