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
# Sidebar - Tema
# ---------------------------
st.sidebar.title("⚙️ Configurações")

theme = st.sidebar.radio(
    "Tema",
    ["🌙 Dark", "☀️ Light"],
    horizontal=True
)

PLOTLY_THEME = "plotly_dark" if theme == "🌙 Dark" else "plotly_white"

# ---------------------------
# CSS dinâmico por tema
# ---------------------------
if theme == "🌙 Dark":
    st.markdown("""
    <style>
        .stApp {
            background-color: #0f172a;
            color: #e5e7eb;
        }
        div[data-testid="metric-container"] {
            background-color: #111827;
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #1f2937;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        .stApp {
            background-color: #f8fafc;
            color: #0f172a;
        }
        div[data-testid="metric-container"] {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #e5e7eb;
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
# Sidebar - Filtros
# ---------------------------
st.sidebar.divider()
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
st.caption("Dashboard interativo com alternância de tema (Dark / Light)")

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
# Gráfico principal
# ---------------------------
line = px.line(
    df.sort_values("age"),
    x="age",
    y="charges",
    color="smoker",
    title="Charges por Idade",
    template=PLOTLY_THEME
)
st.plotly_chart(line, use_container_width=True)

# ---------------------------
# Gráficos secundários
# ---------------------------
col_left, col_right = st.columns(2)

with col_left:
    scatter = px.scatter(
        df,
        x="bmi",
        y="charges",
        color="smoker",
        title="BMI vs Charges",
        template=PLOTLY_THEME
    )
    st.plotly_chart(scatter, use_container_width=True)

with col_right:
    donut = px.pie(
        df,
        names="smoker",
        hole=0.6,
        title="Proporção de Fumantes",
        template=PLOTLY_THEME
    )
    st.plotly_chart(donut, use_container_width=True)

# ---------------------------
# Bar chart
# ---------------------------
bar = px.bar(
    df,
    x="region",
    y="charges",
    color="region",
    title="Custo Médio por Região",
    template=PLOTLY_THEME
)
st.plotly_chart(bar, use_container_width=True)

# ---------------------------
# Insights
# ---------------------------
st.subheader("🔍 Insights Principais")
st.markdown("""
- Fumantes apresentam custos significativamente maiores.
- BMI elevado está fortemente associado a maiores charges.
- A idade influencia progressivamente o valor do seguro.
- A região tem impacto menor comparado a hábitos de saúde.
""")
