import streamlit as st
import pathlib
from utils.constants import sidebar_dictionary,function_dictionary, doc_file_dictionary

def define_configs():
    st.set_page_config (
        page_title="Image Processing Toolkit",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    if "selected_page" not in st.session_state:
        st.session_state["selected_page"] = "Home"

def set_homepage():
    header = st.container()
    header.title("Image Processing Toolkit")

def create_main_content(main_content):
    if st.session_state["selected_page"] is not None:
        try :
            s = function_dictionary[st.session_state["selected_page"]]
        except KeyError :
            main_content.write("Could not find selected_page")
        else:
            s(main_content)

def load_documentation(file_path):
    try:
        with open(file_path) as f:
            return f.read()
    except FileNotFoundError:
        return "### File not found"

def create_doc_content(doc_panel):
    file_folder_path = pathlib.Path(__file__).resolve().parent / "docs"
    if st.session_state["selected_page"] is not None:
        text = load_documentation(
            file_folder_path / doc_file_dictionary[st.session_state["selected_page"]]
        )
    else:
        text = load_documentation(file_folder_path / "home.md")
    doc_panel.markdown(text)

def on_click_function(string:str,):
    st.session_state["selected_page"] = string

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