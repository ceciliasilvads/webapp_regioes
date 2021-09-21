import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from unidecode import unidecode
from matplotlib.backends.backend_agg import RendererAgg

#Contenção de erro no Matplotlib
_lock = RendererAgg.lock

#Buscando os dados
url = 'https://pt.wikipedia.org/wiki/Lista_de_estados_brasileiros_por_n%C3%BAmero_de_munic%C3%ADpios'
lista_df = pd.read_html(url)

#Tabela: Quantidade de habitantes por região
qhr = lista_df[1]
qhr['Municípios'] = qhr['Municípios'].apply(lambda x: (unidecode(x).replace(' ',''))).astype(int)

#Tabela: Quantidade de municípios por estado
qme = lista_df[2]

#Alterando o nome de algumas colunas para melhor entendimento
dic_alteracao = {'Número demunicípios[8]': 'Número de municípios', 'Média de habitantespor município': 'Média por município', 'Número de habitantespor estado federado[9]': 'Habitantes por estado'}
qme.rename(columns = dic_alteracao, inplace=True)
qme['Habitantes por estado'] = qme['Habitantes por estado'].apply(lambda x: (unidecode(x).replace(' ',''))).astype(int)
qme['Média por município']=qme['Habitantes por estado']/qme['Número de municípios']

def regiao_plot(select_r):
    #Verificando a seleção
    if (select_r == 'Sul'):
        regiao = qme.query('Região == "Sul"')
        regiao2 = qhr.query('Região == "Sul"')
        st.write('# Sul')
        st.image('https://cdn.britannica.com/29/142829-073-93CB10FA.jpg', width=350)
    if (select_r == 'Sudeste'):
        regiao = qme.query('Região == "Sudeste"')
        regiao2 = qhr.query('Região == "Sudeste"')
        st.write('# Sudeste')
        st.image('https://cdn.britannica.com/28/142828-073-D5231995.jpg', width=400)
    if (select_r == 'Norte'):
        regiao = qme.query('Região == "Norte"')
        regiao2 = qhr.query('Região == "Norte"')
        st.write('# Norte')
        st.image('https://cdn.britannica.com/27/142827-073-39F29921.jpg', width=500)
    if (select_r == 'Nordeste'):
        regiao = qme.query('Região == "Nordeste"')
        regiao2 = qhr.query('Região == "Nordeste"')
        st.write('# Nordeste')
        st.image('https://cdn.britannica.com/26/142826-073-477DC908.jpg', width=400)
    if (select_r == 'Centro-Oeste'):
        regiao = qme.query('Região == "Centro-Oeste"')
        regiao2 = qhr.query('Região == "Centro-Oeste"')
        st.write('# Centro-Oeste')
        st.image('https://cdn.britannica.com/25/142825-073-4C36265E.jpg', width=400)
    
    #Número de estados
    num_estados = regiao2['Unidadesfederativas'].values
    st.write('### **Número de unidades federativas: **', str(num_estados[0]))
    
    st.write(' ')

    #Estados
    estados = list(regiao['Estado'].values)
    st.write('### **Estados: **', str(tuple(estados[0::])))

    st.write(' ')

    #Número de municipios da região
    num_municipios = regiao2['Municípios'].values
    st.write('### **Número de municipios da região: **', str(num_municipios[0]))
    
    st.write(' ')

    #Número de habitantes da região
    hab_regiao = regiao['Habitantes por estado'].sum()
    st.write('### **Número de habitantes da região: **', str(hab_regiao))

    st.write(' ')

    #Número de municipios por estado
    with _lock:
        fig1, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x=regiao['Número de municípios'], y=regiao['Estado'].values, palette='Set2')
        ax.set_title('Número de municípios por estado', weight = 'bold', size=18)
        ax.set_xlabel('Quantidade de municípios', weight = 'bold')    
        fig1.tight_layout()
        st.pyplot(fig1)

        st.write(' ')

    #Número de habitantes por estado
    with _lock:
        fig2, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x=regiao['Habitantes por estado'], y=regiao['Estado'].values, palette='Set2')
        ax.set_title('Número de habitantes por estado', weight = 'bold', size=18)
        ax.set_xlabel('Quantidade de habitantes', weight = 'bold')
        fig2.tight_layout()
        st.pyplot(fig2)

st.markdown('''# As macrorregiões do Brasil
## **Algumas informações sobre as regiões brasileiras**

### **O que são as regiões?**
A Divisão Regional do Brasil consiste no agrupamento de Estados e Municípios em regiões com a finalidade de atualizar o conhecimento regional do País e viabilizar a definição de uma base territorial para fins de levantamento e divulgação de dados estatísticos. Ademais, visa contribuir com uma perspectiva para a compreensão da organização do território nacional e assistir o governo federal, bem como Estados e Municípios, na implantação e gestão de políticas públicas e investimentos [(IBGE)](https://www.ibge.gov.br/geociencias/cartas-e-mapas/redes-geograficas/15778-divisoes-regionais-do-brasil.html?=&t=o-que-e).

Os critérios para identificação destas unidades foram naturais, sociais e econômicos. Considera-se a partir destes critérios, as seguintes análises [(TudoGEO)](https://tudogeo.com.br/2019/03/17/mapa-das-macrorregioes-do-brasil-ibge/):

- Os domínios ecológicos e como estes influenciam nas atividades e nas formas de organização humanas;
- A distribuição espacial da população e seu comportamento demográfico quantitativo e dinâmico;
- Estrutura agrária, forma de utilização da terra e produção agrícola;
- Atividades industriais, em seus gêneros e dimensões;
- Infraestrutura de transportes, em seu grau de acessibilidade maior ou menor aos meios;
- Atividades terciárias.

## **Mapa do Brasil em divisão por regiões**
''')

st.image('https://tudogeo.com.br/wp-content/uploads/2019/03/macrorregioes_ibge_estados.jpeg', width=700)
st.write('# **Descubra mais sobre cada região!**')
regi_select = st.selectbox('Selecione uma região',['Centro-Oeste', 'Nordeste', 'Norte', 'Sudeste', 'Sul'])
st.write(regiao_plot(select_r=regi_select))
st.markdown(''' **Por: Cecília Silva de Souza**

[![Linkedin Badge](https://img.shields.io/badge/-LinkedIn-4682B4?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/ceciliasilvads)](https://www.linkedin.com/in/ceciliasilvads)
[![Medium Badge](https://img.shields.io/badge/-Medium-000000?style=flat-square&logo=Medium&logoColor=white&link=https://ceciliasilvads.medium.com)](https://ceciliasilvads.medium.com)
[![Gmail Badge](https://img.shields.io/badge/-Gmail-FF0000?style=flat-square&logo=Gmail&logoColor=white&link=mailto:souza.cecilia@acad.ifma.edu.br)](mailto:souza.cecilia@acad.ifma.edu.br)
[![Instagram Badge](https://img.shields.io/badge/-Instagram-E1306C?style=flat-square&logo=Instagram&logoColor=white&link=https://instagram.com/cecilia_souz4)](https://instagram.com/cecilia_souz4)
[![Github Badge](https://img.shields.io/badge/-Github-000000?style=flat-square&logo=Github&logoColor=white&link=https://github.com/ceciliasilvads)](https://github.com/ceciliasilvads)

''')
