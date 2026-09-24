import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

st.set_page_config (
    page_title="Image Processing Toolkit",
    layout="wide",
    initial_sidebar_state="expanded",
)

def run():
    header = st.container()
    header.title("Image Processing Toolkit")
    if "Function" not in st.session_state:
        st.session_state["Function"] = None
    add_sidebar_menu()
    main_content, doc_panel = st.columns([3, 1])
    main_content.write("This is where we show content")
    main_content.write("")
    main_content.write(st.session_state["Function"])
    doc_panel.write("It is document sidebar")

def on_click_function(string:str):
    st.session_state["Function"] = string

def add_sidebar_menu():
    st.sidebar.header("Functionalities")
    with st.sidebar.expander("Category1"):
        st.button("Function1", on_click=on_click_function, args=("Function1",))
        st.button("Function2", on_click=on_click_function, args=("Function2",))
    with st.sidebar.expander("Category2"):
        st.button("Function3", on_click=on_click_function, args=("Function3",))
        st.button("Function4", on_click=on_click_function, args=("Function4",))

if __name__== "__main__":
    run()