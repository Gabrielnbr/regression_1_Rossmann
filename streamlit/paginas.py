import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import plotly_express as px
import seaborn as sns
import requests
import json
import numpy as np
from typing import List
from carregamentos import get_predictions, load_dataset, convert_df
from datetime import datetime

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
        store_ids = st.slider('Escolha as Lojas', value = [1,1115], key=0)
        store_ids = np.arange(store_ids[0], store_ids[1]+1, 1)
        
    with col2:
        budget = st.slider('Percentual para Orçamento', 0,100,10, key=1)
        budget = budget/100
    
    if st.button('Predict '):
        predictions = get_predictions(load_dataset(store_ids, test, store))
        predictions = predictions[['store', 'sales']].groupby('store').mean().reset_index()
        predictions['budget'] = budget*predictions['sales']
        
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
        predictions['budget'] = budget*predictions['sales']

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
    
def outra_pg(test: pd.DataFrame, store: pd.DataFrame, train: pd.DataFrame):
    
    col1, col2 = st.columns(2)
    
    with col1:
        store_ids = st.slider('Escolha as Lojas', value = [1,1115], key=2 )
        store_ids = np.arange(store_ids[0], store_ids[1]+1, 1)
        
    if st.button('Predict ', key=4):
        predictions = get_predictions(load_dataset(store_ids, test, store))
        #predictions = predictions[['store', 'sales']].groupby('store').mean().reset_index()
        predictions['budget'] = 0.1*predictions['sales']
        
        
        graficos(predictions)
        
        st.write(predictions.dtypes, use_container_width= True)
        #Show Dataframe
        st.dataframe(predictions.head(10),
                     #use_container_width= True
                     )
        
        df_treino = train.loc[train['store'].isin(store_ids)]
        
        st.dataframe(df_treino.head(10))
        st.write(df_treino.dtypes, use_container_width= True)
        graficos(df_treino)
        
        #converter para excel
        csv = convert_df(predictions)
        
        # download
        st.download_button(
        label="Download CSV",
        data= csv,
        file_name='predictions.csv',
        mime='text/csv')
        
def graficos(data: pd.DataFrame):
    
    fig, axs = plt.subplots(figsize=(6,6))
    
    h1_aux1 = data[['store','sales']].groupby('store').mean().reset_index()
    sns.barplot(x='store', y='sales', data=h1_aux1, ax=axs);
    #fig = px.bar(h1_aux1, x='store', y='sales', color= 'sales')
    
    #plt.tight_layout()
    #st.plotly_chart(fig)
    st.pyplot(fig)