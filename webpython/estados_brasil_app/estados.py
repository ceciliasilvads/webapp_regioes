import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from unidecode import unidecode

url = 'file:///home/cecelhax/Downloads/brasil_wikipedia.html'
lista_df = pd.read_html(url)

#Quantidade de habitantes por região
qhr = lista_df[1]
qhr['Municípios'] = qhr['Municípios'].apply(lambda x: (unidecode(x).replace(' ',''))).astype(int)

#Quantidade de municípios por estado
qme = lista_df[2]

#Alterando o nome de algumas colunas para melhor visualização
dic_alteracao = {'Número demunicípios[8]': 'Número de municípios', 'Média de habitantespor município': 'Média por município', 'Número de habitantespor estado federado[9]': 'Habitantes por estado'}
qme.rename(columns = dic_alteracao, inplace=True)
qme['Habitantes por estado'] = qme['Habitantes por estado'].apply(lambda x: (unidecode(x).replace(' ',''))).astype(int)
qme['Média por município']=qme['Habitantes por estado']/qme['Número de municípios']

def regiao_plot(select_r):
    if (select_r == 'Sul'):
        regiao = qme.query('Região == "Sul"')
        regiao2 = qhr.query('Região == "Sul"')
    if (select_r == 'Sudeste'):
        regiao = qme.query('Região == "Sudeste"')
        regiao2 = qhr.query('Região == "Sudeste"')
    if (select_r == 'Norte'):
        regiao = qme.query('Região == "Norte"')
        regiao2 = qhr.query('Região == "Norte"')
    if (select_r == 'Nordeste'):
        regiao = qme.query('Região == "Nordeste"')
        regiao2 = qhr.query('Região == "Nordeste"')
    if (select_r == 'Centro-Oeste'):
        regiao = qme.query('Região == "Centro-Oeste"')
        regiao2 = qhr.query('Região == "Centro-Oeste"')
    
    #Numero de estados
    num_estados = regiao2['Unidadesfederativas'].values
    st.write('## **Numero de estados: **', str(num_estados[0]))
    
    st.write(' ')

    #Estados
    estados = list(regiao['Estado'].values)
    st.write('## **Estados: **', str(tuple(estados[0::])))

    st.write(' ')
    st.write(' ')
    st.write(' ')

    #Numero de municipios da regiao
    num_municipios = regiao2['Municípios'].values
    #porcentagem = regiao2['Porcentagem'].values
    st.write('## **Numero de municipios da região: **', str(num_municipios[0]))
    #st.write('Porcentagem: ', porcentagem[0])
    
    st.write(' ')

    #Numero de habitantes da regiao
    hab_regiao = regiao['Habitantes por estado'].sum()
    st.write('## **Habitantes da região: **', str(hab_regiao))

    st.write(' ')

    #Numero de municipios por estado
    fig1, ax = plt.subplots(figsize=(7, 3))
    sns.barplot(x=regiao['Número de municípios'], y=regiao['Estado'].values, palette='Set2')
    ax.set_title('Número de municípios por estado', weight = 'bold', size=15)
    ax.set_xlabel('Número de municípios', weight = 'bold')    
    fig1.tight_layout()
    st.pyplot(fig1)

    st.write(' ')

    #Numero de habitantes por estado
    fig2, ax = plt.subplots(figsize=(7, 3))
    sns.barplot(x=regiao['Habitantes por estado'], y=regiao['Estado'].values, palette='Set2')
    ax.set_title('Número de municípios por estado', weight = 'bold', size=15)
    ax.set_xlabel('Quantidade de habitantes', weight = 'bold')
    fig2.tight_layout()
    st.pyplot(fig2)

st.markdown('''# Regiões do Brasil
## **Algumas informações sobre as regiões brasileiras**

### **O que são as regiões?**
A Divisão Regional do Brasil consiste no agrupamento de Estados e Municípios em regiões com a finalidade de atualizar o conhecimento regional do País e viabilizar a definição de uma base territorial para fins de levantamento e divulgação de dados estatísticos. Ademais, visa contribuir com uma perspectiva para a compreensão da organização do território nacional e assistir o governo federal, bem como Estados e Municípios, na implantação e gestão de políticas públicas e investimentos (IBGE).

## **Mapa do Brasil em divisão por regiões**
''')

endereco_img = '/home/cecelhax/Downloads/regioes.jpeg'
st.image(endereco_img, width=700)

regi_select = st.selectbox('Selecione uma regiao',['Centro-Oeste', 'Nordeste', 'Norte', 'Sudeste', 'Sul'])

st.write(regiao_plot(select_r=regi_select))

  