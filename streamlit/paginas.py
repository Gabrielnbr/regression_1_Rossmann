import streamlit as st
import pandas as pd
from carregamentos import get_predictions, load_dataset, convert_df
from datetime import datetime

def page_bem_vindo():
    st.title('Bem vindo ao Projeto de Predição do Rossmann group')
    
    orientacao = '''<p>Este projeto está já está funcionando em produção.</p>
                    <p>Caso queira acessar mais informações específicas do projeto, segue os links a baixo:</p>
                    <p><i class="fa-brands fa-linkedin"></i><a href="https://www.linkedin.com/in/gabriel-nobre-galvao/"> Linkedin: Aprendizado do projeto de previsão — Rossmann Group</a></p>
                    <p><i class="fa-brands fa-medium"></i><a href="https://medium.com/@gabrielnobregalvao/aprendizado-do-projeto-de-previs%C3%A3o-rossmann-group-c33eef1c6855"> Medium: Aprendizado do projeto de previsão — Rossmann Group</a></p>
                    <p><i class="fa-brands fa-github"></i><a href="https://github.com/Gabrielnbr/regression_1_Rossmann"> Git Hub: regression_1_Rossmann</a></p>
                    '''
    
    st.write(orientacao, unsafe_allow_html = True)
    
    st.subheader("Contato Profissional", divider='blue')
    
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

def multiselect(test: pd.DataFrame, store: pd.DataFrame, train: pd.DataFrame):
    st.title('Previsão de Vendas')
    
    #slide selection
    #store_ids = st.slider('Escolha as Lojas', value = [1,1115], key=0)
    #store_ids = np.arange(store_ids[0], store_ids[1]+1, 1)
    
    store_ids = st.multiselect('Escolha as Lojas',test['Store'].unique(), key=5 )
        
    if st.button('Predict ', key=4):
        predictions = get_predictions(load_dataset(store_ids, test, store))
        
        st.write('''
                 Premissas de Negócio para a seleção das lojas:
                 1. Se a média do faturamento predict_mean for menor do que a média das sales_mean, então não podemos fazer a reforma; caso contrário podemos fazer a reforma.
                 2. Se a diferença do faturamento previsto for menor do que 2,5%, pode-se utilizar 7,5% do faturamento total para a reforma. Se estiver entre 2,5% e 5%, utiliza-se 10%; se for superior a 5%, utiliza-se 12,5% do faturamento.
                 
                 As lojas selecionadas são:
                 ''')
        
        data_csv = negocio(predictions, train)
        
        csv = convert_df(data_csv)
        
        # download
        st.download_button(
        label="Download CSV",
        data= csv,
        file_name='orçamento.csv',
        mime='text/csv')
        
def graficos(data: pd.DataFrame, x : str, y: str):
    
    fig, axs = plt.subplots(figsize=(6,6))
    
    h1_aux1 = data[[x,y]].groupby(x).mean().reset_index()
    sns.scatterplot(x=x, y=y, data=h1_aux1, ax=axs);
    
    st.pyplot(fig)
    
def negocio(predict: pd.DataFrame, train: pd.DataFrame) -> pd.DataFrame:
    
    predictions = round(predict[['store', 'prediction']].groupby('store').agg(['mean', 'sum']).reset_index(),2)
    predictions.columns = ['store', 'prediction_mean', 'prediction_sum']
    
    df_treino = train.loc[train['store'].isin(predictions['store'])]
    df_treino = round(df_treino[['store', 'sales']].groupby('store').mean().reset_index(),2)
    df_treino.columns = ['store', 'sales_mean']
    
    df_final = df_treino.merge(predictions, how='left', on='store')
    df_final['reforma'] = df_final.apply(lambda x: 1 if x['prediction_mean'] > x['sales_mean'] else 0, axis=1)
    
    df_final = df_final.loc[df_final['reforma'] == 1]
    
    if df_final.empty:
        st.text("Infelizmente as lojas selecionadas não atendem aos critérios de realização da reforma")
        return df_final
    else:
        df_final['porcentagem'] = ((df_final['prediction_mean'] / df_final['sales_mean']) - 1)
    
        df_final['porcetagem_orcamento'] = df_final['porcentagem'].apply(lambda x : 0.075 if x < 0.025
                                                                            else 0.1 if x < 0.05
                                                                            else 0.125)
        
        df_final['orcamento'] = round(df_final['prediction_sum']*df_final['porcetagem_orcamento'],2)
        
        df_final = df_final.drop(columns=['reforma','porcentagem'], axis=1)
        
        st.dataframe(df_final)
        return df_final