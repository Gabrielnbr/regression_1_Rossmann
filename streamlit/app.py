import streamlit as st
import pandas as pd
import requests
import json
import numpy as np
from typing import List



def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')


# loading test dataset
#from typing import List
#import pandas as pd
#import json

def load_dataset(store_ids: List[int], test: pd.DataFrame, store: pd.DataFrame) -> str:

    # Realiza o merge do conjunto de dados de teste com as informações das lojas
    df_test = pd.merge(test, store, how='left', on='Store')

    # Filtra o conjunto de dados para incluir apenas as lojas cujos IDs estão presentes na lista fornecida
    df_test = df_test[df_test['Store'].isin(store_ids)]

    if not df_test.empty:
        # Remove os dias em que as lojas estavam fechadas ('Open' == 0) e as linhas com valores nulos na coluna 'Open'
        df_test = df_test[df_test['Open'] != 0]
        df_test = df_test[~df_test['Open'].isnull()]

        # Remove a coluna 'Id' do conjunto de dados
        df_test = df_test.drop('Id', axis=1)

        # Converte o DataFrame resultante em formato JSON
        data = json.dumps(df_test.to_dict(orient='records'))
    else:
        data = 'error'

    return data

# Streamlit app code
def main():

    test = pd.read_csv('data_set/test.csv')
    store = pd.read_csv('data_set/store.csv')
    tab1, tab2 = st.tabs(['Slider','Multiselect'])
    
    with tab1:
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
            st.dataframe(predictions, use_container_width= True)
            
            #converter para excel
            csv = convert_df(predictions)
            
            # download
            st.download_button(
            label="Download CSV",
            data= csv,
            file_name='predictions.csv',
            mime='text/csv',     )       
            
    with tab2:
        st.title('Sales Prediction App')

        budget = st.slider('Percentual para Orçamento ', 0,100,1)
        budget = budget/100
        
        store_ids = st.multiselect('Escolha as Lojas',test['Store'].unique())
        if st.button('Predict'):
            predictions = get_predictions(load_dataset(store_ids, test, store))
            predictions['budget'] = budget*predictions['prediction']
            
            #Show Dataframe
            st.dataframe(predictions, use_container_width= True)
            
            #converter para excel
            csv = convert_df(predictions)
            
            # download
            st.download_button(
            label="Download CSV",
            data= csv,
            file_name='predictions.csv',
            mime='text/csv',
                        )

#from typing import List
#import pandas as pd
#import requests

def get_predictions(data: str) -> pd.DataFrame:

    url = 'http://localhost:5000/rossmann/predict'
    #url = 'https://rossmann-api-45ni.onrender.com/rossmann/predict'
    
    headers = {'Content-type': 'application/json'}
    try:
        r = requests.post(url, json=data, headers=headers)
        r.raise_for_status()  # Raise an exception for HTTP errors (non-2xx responses)
        
        df_result = pd.DataFrame(r.json(), columns= r.json()[0].keys())
        df_result = df_result[['store', 'prediction']].groupby('store').sum().reset_index()
        return df_result
    
    except requests.exceptions.RequestException as e:
        st.write(f"Error occurred during prediction: {e}")
        return pd.DataFrame(columns=['store', 'prediction'])

if __name__ == '__main__':

    main()


