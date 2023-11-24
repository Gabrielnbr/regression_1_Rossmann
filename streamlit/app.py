import streamlit as st
import pandas as pd
import requests
import json
import numpy as np
from typing import List
import paginas as pg

# Streamlit app code
def main():

    test = pd.read_csv('data_set/test.csv')
    store = pd.read_csv('data_set/store.csv')
    tab1, tab2, tab3 = st.tabs(['Bem-vindo','Slider','Multiselect'])
    
    with tab1:
        
        pg.page_bem_vindo()
    
    with tab2:
        
        pg.page_selec_slider(test, store)
        
    with tab3:
        
        pg.page_select_multiselect(test, store)

if __name__ == '__main__':

    main()


