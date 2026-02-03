import matplotlib
matplotlib.use("Agg")


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------
# Configuração da página
# ---------------------------
st.set_page_config(
    page_title="Medical Insurance Dashboard",
    layout="wide"
)

# ---------------------------
# Carregamento dos dados
# ---------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/stedy/Machine-Learning-with-R-datasets/master/insurance.csv"
    return pd.read_csv(url)

df = load_data()

# 🔍 Checkpoint visual (debug)
st.success("Dados carregados com sucesso 🚀")
st.write(df.head())

# ---------------------------
# Título
# ---------------------------
st.title("📊 Medical Insurance Cost Dashboard")
st.markdown("Análise exploratória dos fatores que influenciam o custo de seguro saúde.")

# ---------------------------
# Sidebar - Filtros
# ---------------------------
st.sidebar.header("🔎 Filtros")

selected_region = st.sidebar.multiselect(
    "Região",
    options=df["region"].unique(),
    default=df["region"].unique()
)

selected_smoker = st.sidebar.multiselect(
    "Fumante",
    options=df["smoker"].unique(),
    default=df["smoker"].unique()
)

age_range = st.sidebar.slider(
    "Faixa etária",
    int(df["age"].min()),
    int(df["age"].max()),
    (18, 65)
)

df_filtered = df[
    (df["region"].isin(selected_region)) &
    (df["smoker"].isin(selected_smoker)) &
    (df["age"].between(age_range[0], age_range[1]))
]

# ---------------------------
# KPIs
# ---------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Custo Médio", f"${df_filtered['charges'].mean():,.2f}")
col2.metric("📈 Custo Máximo", f"${df_filtered['charges'].max():,.2f}")
col3.metric("👥 Total de Registros", df_filtered.shape[0])
col4.metric("👶 Média de Filhos", round(df_filtered["children"].mean(), 2))

st.divider()

# ---------------------------
# Gráficos
# ---------------------------
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🚬 Custo por Fumante")
    fig, ax = plt.subplots()
    sns.boxplot(data=df_filtered, x="smoker", y="charges", ax=ax)
    st.pyplot(fig)

with col_right:
    st.subheader("⚖️ BMI vs Charges")
    fig, ax = plt.subplots()
    sns.scatterplot(
        data=df_filtered,
        x="bmi",
        y="charges",
        hue="smoker",
        ax=ax
    )
    st.pyplot(fig)

st.subheader("🌎 Custo Médio por Região")
fig, ax = plt.subplots()
sns.barplot(
    data=df_filtered,
    x="region",
    y="charges",
    ax=ax
)
st.pyplot(fig)

st.divider()

# ---------------------------
# Storytelling
# ---------------------------
st.subheader("🔍 Principais Insights")

st.markdown("""
- Fumantes apresentam custos significativamente maiores de seguro.
- O aumento do BMI está fortemente associado ao aumento do custo.
- A região tem impacto menor quando comparada a hábitos de saúde.
- Idade influencia progressivamente o valor do seguro.
""")
