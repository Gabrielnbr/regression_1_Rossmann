import streamlit.components.v1 as components
import streamlit as st
from PIL import Image
from  app import main


st.set_page_config(
    page_title="Rossmann",
    page_icon="🧊",
    layout="wide")

main()
