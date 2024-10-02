import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

coffee_raw_df = pd.read_csv('data/clean_coffee_data.csv')

# Função para criar gráfico de radar
def create_radar_chart(df, cafe1, cafe2):
    row_1 = df[df['name'] == cafe1].iloc[0][['aroma', 'acid', 'body', 'flavor', 'aftertaste']]
    row_2 = df[df['name'] == cafe2].iloc[0][['aroma', 'acid', 'body', 'flavor', 'aftertaste']]

    # Criando o gráfico de radar usando go.Figure
    fig = go.Figure()

    # Adicionando a primeira linha com cor e preenchimento
    fig.add_trace(go.Scatterpolar(
        r=row_1.values,
        theta=row_1.index,
        fill='toself',
        name=cafe1,
        line_color='blue'
    ))

    # Adicionando a segunda linha com cor e preenchimento
    fig.add_trace(go.Scatterpolar(
        r=row_2.values,
        theta=row_2.index,
        fill='toself',
        name=cafe2,
        line_color='red'
    ))

    # Atualizando layout para mostrar a legenda e configurar o gráfico
    fig.update_layout(
        title=f'Comparação de Características: {cafe1} vs {cafe2}',
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 10])
        ),
        showlegend=True
    )

    return fig


st.title('Análise de Café - Streamlit App')

# Gráfico de Dispersão Preço vs Nota
st.header('Dispersão: Preço vs Nota (Rating)')
fig_scatter = px.scatter(
    coffee_raw_df, x='price_per_100g', y='rating',
    title='Dispersão: Preço vs Nota (Rating)',
    labels={'price_per_100g': 'Preço por 100g (USD)', 'rating': 'Nota (Rating)'}
)
st.plotly_chart(fig_scatter)

# Histograma das Notas
st.header('Histograma das Notas (Ratings)')
fig_hist = px.histogram(coffee_raw_df, x='rating', nbins=20, title='Histograma de Notas (Ratings)')
fig_hist.update_layout(
    xaxis_title='Nota (Rating)',
    yaxis_title='Contagem',
)
st.plotly_chart(fig_hist)

# Seleção de cafés para comparação
st.header('Comparação entre dois cafés')

cafe_1 = st.selectbox('Escolha o primeiro café:', coffee_raw_df['name'].unique())
cafe_2 = st.selectbox('Escolha o segundo café:', coffee_raw_df['name'].unique())

if cafe_1 and cafe_2:
    radar_fig = create_radar_chart(coffee_raw_df, cafe_1, cafe_2)
    st.plotly_chart(radar_fig)