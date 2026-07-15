import streamlit as st
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

from services.item_service import ItemService


st.set_page_config(
    page_title="Magic Item Generator",
    page_icon="✨",
    layout="wide",
)

st.title("✨ Генератор магических предметов")

st.write(
    "Создайте уникальный магический предмет для своей кампании Dungeons & Dragons."
)

if "item_service" not in st.session_state:
    st.session_state.item_service = ItemService()

left, right = st.columns([1, 2])

with left:

    category = st.selectbox(
        "Категория",
        [
            "Любая",
            "Оружие",
            "Броня",
            "Зелье",
            "Кольцо",
            "Посох",
            "Жезл",
            "Чудесный предмет",
        ],
    )

    if category == "Любая":
        subcategory = "Любой"
    else:
        subcategory = st.selectbox(
            "Подтип",
            st.session_state.item_service.subcategories.get(
                category,
                ["Любой"],
            ),
        )

    rarity = st.selectbox(
        "Редкость",
        [
            "Обычная",
            "Необычная",
            "Редкая",
            "Очень редкая",
            "Легендарная",
            "Артефакт",
        ],
    )

    requires_attunement = st.selectbox(
        "Требуется настройка",
        [
            "Да",
            "Нет",
        ],
    )

    features = st.text_area(
        "Дополнительные пожелания",
        placeholder="Например: связано с молниями, подходит паладину, имеет проклятие...",
    )

    generate = st.button(
        "✨ Создать предмет",
        use_container_width=True,
    )


with right:

    if generate:

        with st.spinner("Создание магического предмета..."):

            item = st.session_state.item_service.generate(
                category,
                subcategory,
                rarity,
                requires_attunement,
                features,
            )

        st.title(item.name)

        col1, col2 = st.columns(2)

        with col1:

            st.write(f"**Категория:** {item.category}")
            st.write(f"**Подтип:** {item.subcategory}")
            st.write(f"**Редкость:** {item.rarity}")

        with col2:

            st.write(
                f"**Настройка:** {'Да' if item.requires_attunement else 'Нет'}"
            )

            st.write(f"**Стоимость:** {item.value}")

        st.divider()

        st.subheader("👁 Внешний вид")

        st.write(item.appearance)

        st.subheader("📜 Описание")

        st.write(item.description)

        st.subheader("✨ Магический эффект")

        st.write(item.effect)

        st.subheader("⚠ Ограничения")

        st.write(item.limitations)