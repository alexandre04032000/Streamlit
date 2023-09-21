# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.15.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
import streamlit as st
import pandas as pd
import plotly.express as px
import re

assistidos_preventivos = pd.read_excel(r'assistidos.xlsx')
assistidos_preventivos22 = pd.read_excel(r'assistidos_2022.xlsx')
assistidos_sem_preventivos = pd.read_excel(r'preventivos.xlsx')
assistidos_sem_preventivos22 = pd.read_excel(r'preventivos_2022.xlsx')
automaticos = pd.read_excel(r'automaticos2.xlsx')


assistidos_sem_preventivos['Insignia_de_Ocorrencia__c'] = 'Continente Online'
assistidos_sem_preventivos22['Insignia_de_Ocorrencia__c'] = 'Continente Online'

dicionario = {
    'TrackingTrace': 'TrackingTrace Encomenda',
    'Cupões': 'Cupão',
    'Cupão': 'Cupão',
    'Cupao': 'Cupão',
    'entrega': 'Atraso entrega',
    'SACOS': 'CREDITO DE SACOS',
    'Descontos': 'Recuperação de Desconto',
    'bilhetes': 'Entrega Bilhetes',
    'Paga Mais': 'Nao Paga Mais',
    'Algarve': 'Residentes Algarve',
    'MULTISHIPPING': 'Taxa Multishiping',
    'Reagendamento central': 'Reagendamento central'
}

for indice, label in enumerate(assistidos_sem_preventivos['Subject']):
    for chave, valor in dicionario.items():
        if re.search(r'.*' + chave + r'.*', label, re.IGNORECASE):
            assistidos_sem_preventivos['Subject'][indice] = valor
            print(assistidos_sem_preventivos['Subject'][indice])
            
        
for indice, label in enumerate(assistidos_sem_preventivos22['Subject']):
    for chave, valor in dicionario.items():
        if re.search(r'.*' + chave + r'.*', label, re.IGNORECASE):
            assistidos_sem_preventivos22['Subject'][indice] = valor
            print(assistidos_sem_preventivos22['Subject'][indice])
            

aux5 = assistidos_sem_preventivos
aux8 = assistidos_sem_preventivos22
aux1 = assistidos_sem_preventivos.drop('expr0', axis=1)
result = assistidos_sem_preventivos.groupby(list(aux1.columns)).agg({'expr0': 'sum'})

aux1['Tipo'] = 'preventivos'
aux5['Tipo'] = 'preventivos'
aux8['Tipo'] = 'preventivos'

aux6 = assistidos_preventivos
aux9 = assistidos_preventivos22
aux2 = assistidos_preventivos.drop('expr0', axis=1)

result2 = assistidos_preventivos.groupby('Type').agg({'expr0': 'sum'})

aux2['Tipo'] = 'assistidos'
aux6['Tipo'] = 'assistidos'
aux9['Tipo'] = 'assistidos'
aux6['Subject'] = 'nada'
aux9['Subject'] = 'nada'


aux5 = aux5[['Subject','Nivel_I__c','Tipificação2','Tipificação3','Tipificação4','Insignia_de_Ocorrencia__c','Meio__c','Type','Tipo','Mês','expr0']]
aux6 = aux6[['Subject','Nivel_I__c','Tipificação2','Tipificação3','Tipificação4','Insignia_de_Ocorrencia__c','Meio__c','Type','Tipo','Mês','expr0']]

junto_df = pd.concat([aux5, aux6], ignore_index=True)
junto_df22 = pd.concat([aux8, aux9], ignore_index=True)

junto_df22["Ano"] = 2022
junto_df["Ano"] = 2023

final_junto = pd.concat([junto_df, junto_df22], ignore_index=True)

escolhas = ['Continente','Continente Online']

df = junto_df

titulos = ['Tipos de casos ao longo dos meses','Melhores avaliações','Dataframe']
tabs = st.tabs(titulos)

options = st.sidebar.multiselect(
            'Escolha os trimestres que quer visualizar',
            ['1ºTrimestre', '2ºTrimestre', '3ºTrimestre'],
            ['1ºTrimestre'])

if options == ['1ºTrimestre']:
    junto_df = junto_df[junto_df['Mês'].isin([1, 2, 3])]
    final_junto = final_junto[final_junto['Mês'].isin([1, 2, 3])]

if options == ['2ºTrimestre']:
    junto_df = junto_df[junto_df['Mês'].isin([4, 5, 6])]
    final_junto = final_junto[final_junto['Mês'].isin([4, 5, 6])]

if options == ['3ºTrimestre']:
    junto_df = junto_df[junto_df['Mês'].isin([7, 8, 9])]
    final_junto = final_junto[final_junto['Mês'].isin([7, 8, 9])]

# Verificar se os trimestres 1 e 2 estão selecionados
if '1ºTrimestre' in options and '2ºTrimestre' in options:
    junto_df = junto_df[junto_df['Mês'].isin([1, 2, 3, 4, 5, 6])]
    final_junto = final_junto[final_junto['Mês'].isin([1, 2, 3, 4, 5, 6])]

# Verificar se os trimestres 1 e 3 estão selecionados
if '1ºTrimestre' in options and '3ºTrimestre' in options:
    junto_df = junto_df[junto_df['Mês'].isin([1, 2, 3, 7, 8, 9])]
    final_junto = final_junto[final_junto['Mês'].isin([1, 2, 3, 7, 8, 9])]

# Verificar se todos os trimestres estão selecionados
if '1ºTrimestre' in options and '2ºTrimestre' in options and '3ºTrimestre' in options:
    junto_df = junto_df[junto_df['Mês'].isin([1, 2, 3, 4, 5, 6, 7, 8, 9])]
    final_junto = final_junto[final_junto['Mês'].isin([1, 2, 3, 4, 5, 6, 7, 8, 9])]
    
with tabs[0]:
    

    st.subheader('Escolher os filtros')
    tipo = st.selectbox("Escolha o Tipo:", df["Tipo"].unique())
    
    marca = st.selectbox("Escolha a marca desejada:", escolhas)
    
    st.subheader('Gráfico dos casos totais por mês')

    # Filtrar o DataFrame pelo tipo selecionado
    #filtered_df ------->2023
    #final_junto ------->2023 e 2022
    filtered_df = df[df["Tipo"] == tipo]
    final_junto = final_junto[final_junto['Tipo'] == tipo]

    if(marca == 'Continente Online'):
        filtered_df = filtered_df[filtered_df['Insignia_de_Ocorrencia__c'] == 'Continente Online']
        final_junto = final_junto[final_junto['Insignia_de_Ocorrencia__c'] == 'Continente Online']
    else:
        conditions = ['Apps', 'Cartão Continente', 'Cartão Universo', 'Ficha de Cliente Cartão Continente', 'Ficha de Cliente Portador']
        filtered_df = filtered_df[filtered_df['Tipificação2'].isin(conditions)]
        final_junto = final_junto[final_junto['Tipificação2'].isin(conditions)]

    # Gráfico de barras para o count de ocorrências
    fig = px.histogram(
        final_junto,
        x="Mês",
        y="expr0",
        color="Ano",
        barmode='group',
        title=f"Ocorrências por Mês para o Tipo: {tipo}",
        labels={"Mês": "Mês", "expr0": "Número de Ocorrências"},
    )
    st.plotly_chart(fig)
        
#st.subheader('Gráfico com os 5 temas com mais casos')
#tipificacao2_counts =  filtered_df['Tipificação2'].value_counts()
#top_tipificacao2 = tipificacao2_counts.nlargest(5)

# Filtrar o DataFrame para incluir apenas as top 5 Tipificação2
#filtered_df = filtered_df[filtered_df['Tipificação2'].isin(top_tipificacao2.index)]

#fig = px.bar(
#    filtered_df,
#    x='Tipificação2',
#    y='expr0',
#    title='Top 5 Tipificação2 com mais casos',
#    labels={'Tipificação2': 'Tipificação2', 'expr0': 'Número de Ocorrências'},
#)

# Agora, exibir o gráfico na segunda aba (tab2)
#tab1, tab2 = st.columns([2, 3])
agg_functions = {
    'expr0': 'sum'
}

with tabs[1]:
    st.title("📈 Gráficos")
    
    st.subheader('Gráfico com os 5 temas com mais casos')
    maior = filtered_df
    maior = maior.groupby(['Tipificação2']).agg(agg_functions).reset_index()
    df = maior
    top_5 = df.nlargest(5, 'expr0')
    others_total = df['expr0'].sum() - top_5['expr0'].sum()
    other_row = {'Tipificação2': 'Outros', 'expr0': others_total}
    final_df = pd.concat([top_5, pd.DataFrame([other_row])], ignore_index=True)

    fig = px.bar(
        final_df,
        x='Tipificação2',
        y='expr0',
        title='Top 5 Tipificação2 com mais casos',
        labels={'Tipificação2': 'Tipificação2', 'expr0': 'Número de Ocorrências'},
    )
    st.plotly_chart(fig)
    
    if tipo == 'preventivos':
            st.subheader('Gráfico com as principais subjects em 2022 e 2023')
            aux = final_junto
            aux = aux[aux['expr0'] > 3000]
            fig = px.histogram(
                aux,
                x="Subject",
                y="expr0",
                color="Ano",
                barmode='group',
                title=f"Top Subjects para os casos do tipo assistidos em 2022 e em 2023",
                labels={"Mês": "Mês", "expr0": "Número de Ocorrências"},
            )
            st.plotly_chart(fig)
        
with tabs[2]:
    kapa = junto_df
    st.title("🗃 Tabelas")
    # Tabela para exibir o DataFrame Original
    st.write("DataFrame Original:")
    options2 = st.sidebar.multiselect(
            'Escolha os trimestres que quer visualizar',
            kapa.columns,
            ['Mês'])
    kapa = kapa[options2]
    st.write(kapa)
    

#st.title('Hello Alexandre')
