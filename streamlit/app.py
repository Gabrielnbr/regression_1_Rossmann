import streamlit as st
import pandas as pd
import paginas as pg

# Streamlit app code
def main():

    test = pd.read_csv('data_set/test.csv')
    store = pd.read_csv('data_set/store.csv')
    train = pd.read_csv('data_set/treino.csv')
    tab1, tab2= st.tabs(['Bem-vindo','Multiselect'])
    
    with tab1:
        
        pg.page_bem_vindo()
    
    with tab2:
        pg.multiselect(test, store, train)


if __name__ == '__main__':

    main()


