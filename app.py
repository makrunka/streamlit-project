import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Заголовок
st.title("📊 Аналіз фінансових показників компаній")

# Завантаження файлу
uploaded_file = st.file_uploader("📂 Завантаж CSV файл", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Вхідні дані")
    st.dataframe(df)

    # Бокова панель (фільтри)
    st.sidebar.header("🔎 Фільтри")

    year = st.sidebar.selectbox("Оберіть рік", sorted(df["Year"].unique()))
    industry = st.sidebar.selectbox("Оберіть галузь", df["Industry"].unique())

    filtered_df = df[(df["Year"] == year) & (df["Industry"] == industry)]

    st.subheader("📌 Відфільтровані дані")
    st.dataframe(filtered_df)

    # Графік доходу
    st.subheader("📈 Динаміка доходу компаній")

    fig, ax = plt.subplots()
    sns.lineplot(data=df, x="Year", y="Revenue", hue="Company", marker="o", ax=ax)
    ax.set_title("Зміна доходу по роках")
    st.pyplot(fig)

    # Розрахунок коефіцієнтів
    df["Liquidity"] = df["Assets"] / df["Liabilities"]
    df["Profitability"] = df["Profit"] / df["Revenue"]

    st.subheader("📊 Фінансові коефіцієнти")

    col1, col2 = st.columns(2)

    with col1:
        st.write("🔹 Ліквідність")
        st.dataframe(df[["Company", "Year", "Liquidity"]])

    with col2:
        st.write("🔹 Рентабельність")
        st.dataframe(df[["Company", "Year", "Profitability"]])

    # Додатковий графік
    st.subheader("📊 Прибуток компаній")

    fig2, ax2 = plt.subplots()
    sns.barplot(data=filtered_df, x="Company", y="Profit", ax=ax2)
    st.pyplot(fig2)

    # Метрики
    st.subheader("📌 Загальні показники")

    st.metric("Середня рентабельність", round(df["Profitability"].mean(), 2))
    st.metric("Середня ліквідність", round(df["Liquidity"].mean(), 2))

else:
    st.info("⬆️ Завантаж CSV файл, щоб розпочати аналіз")