import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configurações da página
st.set_page_config(page_title="Coffee Data Comp", page_icon="☕", layout="wide")

# Carregamento dos dados
coffee_raw_df = pd.read_csv('data/clean_coffee_data.csv')
coffee_raw_df.dropna(inplace=True)
coffee_raw_df['countries_separated'] = coffee_raw_df['origin_country'].apply(lambda x: x.split(';') if x else [])
df_countries_uni = coffee_raw_df.explode('countries_separated')
coffee_raw_df.dropna(inplace=True)
#print(coffee_raw_df.info())

st.sidebar.title('☕ Coffee Data Comp')

# Filtrando por país de origem
origin_country_filter = st.sidebar.selectbox(
    'Filtrar por País de Origem:', 
    ['Todos'] + sorted(list(df_countries_uni['countries_separated'].unique()))
)

if origin_country_filter != 'Todos':
    coffee_filtered_df = coffee_raw_df[coffee_raw_df['origin_country'].str.lower().str.contains(origin_country_filter.lower())]
else:
    coffee_filtered_df = coffee_raw_df

st.title('☕ Análise de Café - Streamlit App')

# Função para criar gráfico de redes
def create_radar_chart(df, cafe1, cafe2):
    row_1 = df[df['name'] == cafe1].iloc[0][['aroma', 'acid', 'body', 'flavor', 'aftertaste']]
    row_2 = df[df['name'] == cafe2].iloc[0][['aroma', 'acid', 'body', 'flavor', 'aftertaste']]

    # Criando o gráfico de redes usando go.Figure
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=row_1.values,
        theta=row_1.index,
        fill='toself',
        #fillcolor='rgba(0, 0, 255, 0.1)',
        name=cafe1,
        line_color='blue',
    ))

    fig.add_trace(go.Scatterpolar(
        r=row_2.values,
        theta=row_2.index,
        fill='toself',
        name=cafe2,
        line_color='red',
        #fillcolor='rgba(255, 0, 0, 0.1)',
    ))

    fig.update_layout(
        title=f'Comparação de Características: {cafe1} vs {cafe2}',
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 10])
        ),
        showlegend=True
    )

    return fig


# Colocando o gráfico de dispersão e histograma em abas
tab1, tab2 = st.tabs(['📊 Dispersão Preço vs Nota', '📈 Histograma das Notas'])

with tab1:
    # Gráfico de Dispersão Preço vs Nota
    st.header('Dispersão: Preço vs Nota (Rating)')
    fig_scatter = px.scatter(
        coffee_filtered_df, x='price_per_100g', y='rating',
        title='Dispersão: Preço vs Nota (Rating)',
        labels={'price_per_100g': 'Preço por 100g (USD)', 'rating': 'Nota (Rating)'}
    )
    st.plotly_chart(fig_scatter)

with tab2:
    # Histograma das Notas
    st.header('Histograma das Notas (Ratings)')
    fig_hist = px.histogram(coffee_filtered_df, x='rating', nbins=20, title='Histograma de Notas (Ratings)')
    fig_hist.update_layout(
        xaxis_title='Nota (Rating)',
        yaxis_title='Contagem',
    )
    st.plotly_chart(fig_hist)

# Seleção de cafés para comparação
st.header('Comparação entre dois cafés')

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    cafe_1 = st.selectbox('Escolha o primeiro café:', coffee_filtered_df['name'].unique())

    if cafe_1:
        cafe1_info = coffee_filtered_df[coffee_filtered_df['name'] == cafe_1].iloc[0]
        st.markdown(f"**Roaster:** {cafe1_info['roaster']}")
        st.markdown(f"**Rating:** {cafe1_info['rating']}")
        st.markdown(f"**Preço/100g:** USD {cafe1_info['price_per_100g']:.2f}")

with col3:
    cafe_2 = st.selectbox('Escolha o segundo café:', coffee_filtered_df['name'].unique())

    if cafe_2:
        cafe2_info = coffee_filtered_df[coffee_filtered_df['name'] == cafe_2].iloc[0]
        st.markdown(f"**Roaster:** {cafe2_info['roaster']}")
        st.markdown(f"**Rating:** {cafe2_info['rating']}")
        st.markdown(f"**Preço/100g:** USD {cafe2_info['price_per_100g']:.2f}")

if cafe_1 and cafe_2:
    with col2:
        radar_fig = create_radar_chart(coffee_filtered_df, cafe_1, cafe_2)
        st.plotly_chart(radar_fig)
