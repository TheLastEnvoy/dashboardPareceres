import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Carregar os dados do Excel
file_path = "pareceres_SO_31out2024.xlsx"
df = pd.read_excel(file_path)

# Definir título do aplicativo
st.title("Dashboard de Pareceres")

# Filtros laterais
assentamentos = ['Todos'] + sorted(list(df['Assentamento'].unique()))
formatos = ['Todos'] + sorted(list(df['Formato'].unique()))
andamentos = ['Todos'] + sorted(list(df['Andamento'].unique()))

selected_assentamento = st.sidebar.selectbox("Selecione um assentamento:", assentamentos, key="assentamento")
selected_formato = st.sidebar.selectbox("Selecione um formato:", formatos, key="formato")
selected_andamento = st.sidebar.selectbox("Selecione um andamento:", andamentos, key="andamento")

# Filtrar por assentamento
if selected_assentamento != "Todos":
    df = df[df['Assentamento'] == selected_assentamento]

# Filtrar por formato
if selected_formato != "Todos":
    df = df[df['Formato'] == selected_formato]

# Filtrar por andamento
if selected_andamento != "Todos":
    df = df[df['Andamento'] == selected_andamento]

# Calcular o total de pareceres em elaboração e concluídos
pareceres_em_elaboracao = df[df['Andamento'] == 'Em elaboração'].shape[0]
pareceres_concluidos = df[df['Andamento'] == 'Concluído'].shape[0]

# Definir o total a atingir
total_a_atingir = 5861

# Criar gráfico de barras empilhadas para mostrar o progresso
fig_progress = go.Figure()

fig_progress.add_trace(go.Bar(
    name='Em elaboração',
    x=['Pareceres'],
    y=[pareceres_em_elaboracao],
    marker_color='orange'
))

fig_progress.add_trace(go.Bar(
    name='Concluídos',
    x=['Pareceres'],
    y=[pareceres_concluidos],
    marker_color='green'
))

fig_progress.add_trace(go.Bar(
    name='Faltando',
    x=['Pareceres'],
    y=[max(0, total_a_atingir - (pareceres_em_elaboracao + pareceres_concluidos))],
    marker_color='lightgrey'
))

# Atualizar layout do gráfico
fig_progress.update_layout(
    barmode='stack',
    title='Progresso dos Pareceres',
    xaxis_title='Status',
    yaxis_title='Quantidade',
    legend_title='Legenda'
)

# Exibir gráfico de progresso
st.plotly_chart(fig_progress)

# Gráfico de pizza para assentamentos
st.subheader("Gráfico de pizza - Assentamentos")
assentamento_data = df['Assentamento'].value_counts()
fig_assentamento = px.pie(
    names=assentamento_data.index,
    values=assentamento_data.values,
    title='Distribuição dos Pareceres por Assentamento'
)
st.plotly_chart(fig_assentamento)

# Exibir tabela interativa
st.subheader("Relação de pareceres")
st.write(df)

# Exibir gráfico de barras para andamento
st.subheader("Gráfico de barras - andamento")
chart_data_andamento = df['Andamento'].value_counts()
st.bar_chart(chart_data_andamento)

# Calcular o total de pareceres para cada formato e andamento
total_por_formato_andamento = df.groupby(['Formato', 'Andamento']).size().reset_index(name='Quantidade de Pareceres')

# Exibir quadro com os totais por formato e andamento
st.subheader("Quantidade de pareceres por formato e andamento")
st.write(total_por_formato_andamento)
