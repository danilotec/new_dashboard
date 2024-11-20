import streamlit as st
import json, os
import pandas as pd

DATA_BASE = 'data_base.json'

def cadastro():
    st.subheader('Cadastro de Equipamentos!')
    col1, col2, col3 = st.columns(3)
    opcoes = ['Cesar', 'Fabricio', 'Thiago']

    with col1:
        unidade = st.text_input('Unidade:', key="unidade")
        tecnicos = st.multiselect('Selecione um tecnico:', opcoes, placeholder='Selecione uma opção')
    with col2:    
        equipamento = st.text_input('Equipamento:', key="equipamento")
        visita = st.multiselect('Tipo de Visita:', ['Preventiva', 'Corretiva'], placeholder='Selecione um opção')
    with col3:
        n_serie = st.text_input('Numero de serie:', key="n_serie")
        data_selecionada = st.date_input('Selecione uma data')

    detalhes = st.text_area(label='Detalhes:', placeholder='Descreva o defeito')
    enviar = st.button('Enviar')
    
    day = data_selecionada.day
    month = data_selecionada.month


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
            "tipo": visita,
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
    st.subheader('Tabelas')

    with open(DATA_BASE, 'r') as file:
        data = json.load(file)
        df = pd.json_normalize(data, 'tecnicos', ['unidade', 'equipamento', 'numero_serie', 'tipo', 'detalhes', 'data', 'mes'], 
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
