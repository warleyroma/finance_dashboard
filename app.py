import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------
# Configuração da página
# ---------------------------
st.set_page_config(
    page_title="Insurance Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------------------
# Estilo customizado (dark)
# ---------------------------
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
    }
    div[data-testid="metric-container"] {
        background-color: #111827;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #1f2937;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Carregamento dos dados
# ---------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/stedy/Machine-Learning-with-R-datasets/master/insurance.csv"
    return pd.read_csv(url)

df = load_data()

# ---------------------------
# Sidebar
# ---------------------------
st.sidebar.title("🔎 Filtros")

region = st.sidebar.multiselect(
    "Região",
    df["region"].unique(),
    df["region"].unique()
)

smoker = st.sidebar.multiselect(
    "Fumante",
    df["smoker"].unique(),
    df["smoker"].unique()
)

df = df[
    (df["region"].isin(region)) &
    (df["smoker"].isin(smoker))
]

# ---------------------------
# Título
# ---------------------------
st.title("💼 Medical Insurance Analytics")
st.caption("Dashboard interativo inspirado em layouts SaaS modernos")

# ---------------------------
# KPIs
# ---------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Custo Médio", f"${df.charges.mean():,.0f}")
col2.metric("📈 Custo Máximo", f"${df.charges.max():,.0f}")
col3.metric("🚬 % Fumantes", f"{(df.smoker.eq('yes').mean()*100):.1f}%")
col4.metric("👥 Registros", df.shape[0])

st.divider()

# ---------------------------
# Linha principal (inspirado no layout)
# ---------------------------
line = px.line(
    df.sort_values("age"),
    x="age",
    y="charges",
    color="smoker",
    title="Charges por Idade",
    template="plotly_dark"
)

st.plotly_chart(line, use_container_width=True)

# ---------------------------
# Gráficos inferiores
# ---------------------------
col_left, col_right = st.columns(2)

with col_left:
    scatter = px.scatter(
        df,
        x="bmi",
        y="charges",
        color="smoker",
        title="BMI vs Charges",
        template="plotly_dark"
    )
    st.plotly_chart(scatter, use_container_width=True)

with col_right:
    donut = px.pie(
        df,
        names="smoker",
        hole=0.6,
        title="Proporção de Fumantes",
        template="plotly_dark"
    )
    st.plotly_chart(donut, use_container_width=True)

# ---------------------------
# Bar chart por região
# ---------------------------
bar = px.bar(
    df,
    x="region",
    y="charges",
    color="region",
    title="Custo Médio por Região",
    template="plotly_dark"
)

st.plotly_chart(bar, use_container_width=True)

# ---------------------------
# Insights
# ---------------------------
st.subheader("🔍 Insights Principais")
st.markdown("""
- Fumantes geram custos significativamente mais altos.
- BMI elevado está fortemente correlacionado ao aumento dos charges.
- A idade impacta o custo de forma progressiva.
- A região tem impacto menor quando comparada a hábitos de saúde.
""")
