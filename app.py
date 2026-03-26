import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Налаштування сторінки
st.set_page_config(page_title="Фінансовий аналіз", layout="wide")

# Заголовок
st.title("📊 Аналіз фінансових показників компаній")

# Завантаження CSV автоматично
df = pd.read_csv("data.csv")

# Перевірка даних
if df.empty:
    st.error("Файл порожній або не завантажився")
else:
    # Показ таблиці
    st.subheader("📄 Вхідні дані")
    st.dataframe(df, use_container_width=True)

    # --- ФІЛЬТРИ ---
    st.sidebar.header("🔎 Фільтри")

    year = st.sidebar.selectbox(
        "Оберіть рік",
        sorted(df["Year"].dropna().unique())
    )

    industry = st.sidebar.selectbox(
        "Оберіть галузь",
        sorted(df["Industry"].dropna().unique())
    )

    filtered_df = df[
        (df["Year"] == year) &
        (df["Industry"] == industry)
    ]

    # --- ВІДФІЛЬТРОВАНІ ДАНІ ---
    st.subheader("📌 Відфільтровані дані")

    if filtered_df.empty:
        st.warning("Немає даних для вибраних параметрів")
    else:
        st.dataframe(filtered_df, use_container_width=True)

    # --- ГРАФІК ДОХОДУ ---
    st.subheader("📈 Динаміка доходу компаній")

    fig, ax = plt.subplots()
    sns.lineplot(
        data=df,
        x="Year",
        y="Revenue",
        hue="Company",
        marker="o",
        ax=ax
    )
    ax.set_title("Зміна доходу по роках")
    st.pyplot(fig)

    # --- РОЗРАХУНКИ ---
    df["Liquidity"] = df["Assets"] / df["Liabilities"]
    df["Profitability"] = df["Profit"] / df["Revenue"]

    st.subheader("📊 Фінансові коефіцієнти")

    col1, col2 = st.columns(2)

    with col1:
        st.write("🔹 Ліквідність")
        st.dataframe(
            df[["Company", "Year", "Liquidity"]],
            use_container_width=True
        )

    with col2:
        st.write("🔹 Рентабельність")
        st.dataframe(
            df[["Company", "Year", "Profitability"]],
            use_container_width=True
        )

    # --- ГРАФІК ПРИБУТКУ ---
    st.subheader("📊 Прибуток компаній")

    if not filtered_df.empty:
        fig2, ax2 = plt.subplots()
        sns.barplot(
            data=filtered_df,
            x="Company",
            y="Profit",
            ax=ax2
        )
        st.pyplot(fig2)

    # --- МЕТРИКИ ---
    st.subheader("📌 Загальні показники")

    col3, col4 = st.columns(2)

    with col3:
        st.metric(
            "Середня рентабельність",
            round(df["Profitability"].mean(), 2)
        )

    with col4:
        st.metric(
            "Середня ліквідність",
            round(df["Liquidity"].mean(), 2)
        )
    st.info("⬆️ Завантаж CSV файл, щоб розпочати аналіз")
