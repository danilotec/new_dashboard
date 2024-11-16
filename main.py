import streamlit as st
import json, os
import pandas as pd

DATA_BASE = 'data_base.json'

def cadastro():
    st.title('Cadastro de equipamentos!')

    unidade = st.text_input('Digite a unidade:', key="unidade")
    equipamento = st.text_input('Digite o novo equipamento:', key="equipamento")
    n_serie = st.text_input('Digite o numero de serie:', key="n_serie")
    detalhes = st.text_area(label='Detalhes', placeholder='Descreva sobre o defeito')

    opcoes = ['Cesar', 'Fabricio', 'Thiago']
    tecnicos = st.multiselect('Selecione um tecnico:', opcoes)

    data_selecionada = st.date_input('Selecione uma data')
    day = data_selecionada.day
    month = data_selecionada.month

    *_, col1 = st.columns(8)
    with col1:
        enviar = st.button('enviar')

    def carregar_dados():
        if os.path.exists(DATA_BASE):
            with open(DATA_BASE, 'r') as file:
                try:
                    return json.load(file)  
                except json.JSONDecodeError:
                    return []  
        else:
            return []  

    if enviar:
        
        dados_existentes = carregar_dados()

        
        novo_dado = {
            "unidade": unidade,
            "equipamento": equipamento, 
            "numero_serie": n_serie, 
            "detalhes": detalhes,
            "tecnicos": tecnicos,
            "data": day,
            "mes": month
        }


        if isinstance(dados_existentes, list):
            dados_existentes.append(novo_dado)
        else:
            dados_existentes = [novo_dado]  

        with open(DATA_BASE, 'w') as file:
            json.dump(dados_existentes, file, indent=2)

        st.success('Equipamento cadastrado!')

def inicio():
    st.title('Gestão de Equipamentos')
    st.header('CR MEDICAL & INDUSTRY')
    st.subheader('Odontologia')

def tabelas():
    st.write('Tabelas')

    with open(DATA_BASE, 'r') as file:
        data = json.load(file)
        df = pd.json_normalize(data, 'tecnicos', ['unidade', 'equipamento', 'numero_serie', 'detalhes', 'data', 'mes'], 
                       record_prefix='tecnico_')
        st.dataframe(df)
    

st.sidebar.title('Menu')
screens = st.sidebar.selectbox(
    'Abas disponiveis:',
    ['Tela inicial', 'Cadastro', 'Tabelas']
)

if screens == 'Tela inicial':
    inicio()
elif screens == 'Cadastro':
    cadastro()
elif screens == 'Tabelas':
    tabelas()
