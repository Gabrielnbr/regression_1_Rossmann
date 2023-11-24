import streamlit as st
import pandas as pd
import requests
import json
import numpy as np
from typing import List
from carregamentos import get_predictions, load_dataset, convert_df

def page_bem_vindo():
    st.title('Bem vindo ao Projeto de Predição do Rossmann group')
    
    orientacao = '''<p>Este projeto está já está funcionando em produção.</p>
                    <p>Só estou terminando de escrever as orientações finais para publicação.</p>
                    <p>Ele estará 100% concluído até dia 31/11/2023.</p>
                    '''
    
    st.write(orientacao, unsafe_allow_html = True)
    
    st.subheader("Contato", divider = 'blue')
    
    contato = '''
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    
    
    <ul class="actions">
        <table>
            <tr>
                <th><i class="fa-solid fa-folder-tree"></i><a href="https://bit.ly/portfolio-gabriel-nobre"> Portfólio de Projetos</a></th>
                <th><i class="fa-brands fa-linkedin"></i><a href="https://www.linkedin.com/in/gabriel-nobre-galvao/"> Linkedin</a></th>
                <th><i class="fa-brands fa-medium"></i><a href="https://medium.com/@gabrielnobregalvao"> Medium</a></th>
                <th><i class="fa-brands fa-github"></i><a href="https://github.com/Gabrielnbr"> Git Hub</a></th>
                <th><i class="fa-solid fa-envelope"></i><a href="mailto:gabrielnobregalvao@gmail.com"> E-mail</a></th>
            </tr>
        </table>
    </ul>
    '''
    st.write(contato, unsafe_allow_html=True)

def page_selec_slider(test: pd.DataFrame, store: pd.DataFrame):
    
    st.title('Sales Prediction App')
    
    col1, col2 = st.columns(2)
    
    with col1:
        store_ids = st.slider('Escolha as Lojas', value = [1,1115] )
        store_ids = np.arange(store_ids[0], store_ids[1]+1, 1)
        
    with col2:
        budget = st.slider('Percentual para Orçamento', 0,100,10)
        budget = budget/100
    
    if st.button('Predict '):
        predictions = get_predictions(load_dataset(store_ids, test, store))
        predictions['budget'] = budget*predictions['prediction']
        
        #Show Dataframe
        st.dataframe(predictions,
                     #use_container_width= True
                     )
        
        #converter para excel
        csv = convert_df(predictions)
        
        # download
        st.download_button(
        label="Download CSV",
        data= csv,
        file_name='predictions.csv',
        mime='text/csv',     )     
    

def page_select_multiselect(test: pd.DataFrame, store: pd.DataFrame):
    st.title('Sales Prediction App')

    budget = st.slider('Percentual para Orçamento ', 0,100,1)
    budget = budget/100

    store_ids = st.multiselect('Escolha as Lojas',test['Store'].unique())
    if st.button('Predict'):
        predictions = get_predictions(load_dataset(store_ids, test, store))
        predictions['budget'] = budget*predictions['prediction']

        #Show Dataframe
        st.dataframe(predictions,
                     #use_container_width= True
                     )

        #converter para excel
        csv = convert_df(predictions)

        # download
        st.download_button(
        label="Download CSV",
        data= csv,
        file_name='predictions.csv',
        mime='text/csv',
                    )