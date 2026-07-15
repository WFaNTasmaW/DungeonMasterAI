import streamlit as st

from services.loot_service import LootService

st.set_page_config(
    page_title="Генератор добычи",
    page_icon="💰",
)

st.title("💰 Генератор добычи")

st.write(
    """
Сгенерируйте сокровища для приключения.

Количество и ценность добычи зависят от диапазона опасности,
а дополнительные пожелания помогут немного изменить характер награды.
"""
)

danger = st.selectbox(

    "Диапазон опасности",

    [

        "1-4",

        "5-10",

        "11-16",

        "17+",

    ]

)

features = st.text_area(

    "Дополнительные пожелания",

    placeholder="Например: древний храм, логово дракона, сокровищница дворфа...",

)

if st.button("🎲 Сгенерировать добычу"):

    service = LootService()

    loot = service.generate(

        danger=danger,

        features=features,

    )

    st.divider()

    if loot.coins:

        st.subheader("🪙 Монеты")

        for coin in loot.coins:

            st.write(f"• {coin}")

    if loot.mundane_items:

        st.subheader("🎒 Обычные предметы")

        for item in loot.mundane_items:

            with st.expander(item["name"]):

                st.write(f"**Категория:** {item['category']}")

                st.write(f"**Стоимость:** {item['cost']}")

                st.write(f"**Вес:** {item['weight']}")

                if item["description"]:

                    st.write(item["description"])

    if loot.gems:

        st.subheader("💎 Драгоценные камни")

        for gem in loot.gems:

            with st.expander(gem["name"]):

                st.write(f"**Стоимость:** {gem['value']} зм")

                st.write(gem["description"])

    if loot.magic_items:

        st.subheader("✨ Магические предметы")

        for item in loot.magic_items:

            st.write(f"• {item['name']}")