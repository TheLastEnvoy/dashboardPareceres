import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Carregar os dados do Excel
file_path = "pareceres_SO_31out2024.xlsx"
df = pd.read_excel(file_path)

# Definir título do aplicativo
st.title("Dashboard de Pareceres")

# Definir título da tabela com informações gerais sobre os pareceres
st.subheader("Relação de pareceres")

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

# Exibir tabela interativa
st.write(df)

# Exibir gráfico de barras para andamento
st.subheader("Gráfico de barras - andamento")
chart_data_andamento = df['Andamento'].value_counts()
st.bar_chart(chart_data_andamento)

# Gráfico de pizza
st.subheader("Gráfico de pizza - andamento")
pie_chart_data = df['Andamento'].value_counts()
fig = px.pie(names=pie_chart_data.index, values=pie_chart_data.values, title='Distribuição dos Andamentos')
st.plotly_chart(fig)

# Calcular o total de pareceres em elaboração e concluídos
pareceres_em_elaboracao = df[df['Andamento'] == 'Em Elaboração'].shape[0]
pareceres_concluidos = df[df['Andamento'] == 'Concluído'].shape[0]

# Definir o total a atingir
total_a_atingir = 5861

# Criar gráfico de barras empilhadas para mostrar o progresso
fig_progress = go.Figure()

fig_progress.add_trace(go.Bar(
    name='Em Elaboração',
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
    y=[total_a_atingir - (pareceres_em_elaboracao + pareceres_concluidos)],
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

# Calcular o total de pareceres para cada formato
total_por_formato = df['Formato'].value_counts()

# Calcular o total de pareceres
total_de_pareceres = total_por_formato.sum()

# Adicionar o total de pareceres ao DataFrame
total_por_formato = total_por_formato.reset_index()
total_por_formato.columns = ['Formato', 'Quantidade de Pareceres']
total_por_formato.loc[len(total_por_formato)] = ['Total', total_de_pareceres]

# Exibir quadro com os totais
st.subheader("Quantidade de pareceres por formato")
st.write(total_por_formato)
