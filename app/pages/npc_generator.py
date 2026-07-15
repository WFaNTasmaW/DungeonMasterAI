import streamlit as st
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

from services.npc_service import NPCService


st.set_page_config(
    page_title="NPC Generator",
    page_icon="🎭",
    layout="wide",
)

st.title("🎭 Генератор NPC")

st.write(
    "Создайте уникального NPC для своей кампании D&D."
)

if "npc_service" not in st.session_state:
    st.session_state.npc_service = NPCService()


left, right = st.columns([1, 2])


with left:

    race = st.selectbox(
        "Раса",
        [
            "Любая",
            "Человек",
            "Эльф",
            "Полуэльф",
            "Дварф",
            "Полурослик",
            "Гном",
            "Полуорк",
            "Тифлинг",
            "Драконорождённый",
            "Табакси",
            "Голиаф",
            "Аасимар",
        ],
    )

    character_class = st.selectbox(
        "Класс",
        [
            "Любой",
            "Воин",
            "Волшебник",
            "Колдун",
            "Чародей",
            "Жрец",
            "Плут",
            "Следопыт",
            "Бард",
            "Паладин",
            "Друид",
            "Монах",
            "Варвар",
            "Изобретатель",
        ],
    )

    gender = st.selectbox(
        "Пол",
        [
            "Любой",
            "Мужчина",
            "Женщина",
        ],
    )

    age = st.selectbox(
        "Возраст",
        [
            "Любой",
            "Ребёнок",
            "Молодой",
            "Взрослый",
            "Пожилой",
        ],
    )

    alignment = st.selectbox(
        "Мировоззрение",
        [
            "Любое",
            "Законопослушный Добрый",
            "Нейтральный Добрый",
            "Хаотичный Добрый",
            "Законопослушный Нейтральный",
            "Истинно Нейтральный",
            "Хаотичный Нейтральный",
            "Законопослушный Злой",
            "Нейтральный Злой",
            "Хаотичный Злой",
        ],
    )

    role = st.selectbox(
        "Роль",
        [
            "Любая",
            "Торговец",
            "Трактирщик",
            "Стражник",
            "Кузнец",
            "Маг",
            "Священник",
            "Охотник",
            "Наёмник",
            "Бандит",
            "Алхимик",
            "Благородный",
            "Путешественник",
            "Моряк",
        ],
    )

    features = st.text_area(
        "Особенности",
        placeholder="Например: носит маску, хромает, боится магии...",
    )

    generate = st.button(
        "🎲 Сгенерировать NPC",
        use_container_width=True,
    )


with right:

    if generate:

        with st.spinner("Создание NPC..."):

            npc, image = st.session_state.npc_service.generate(
                race,
                character_class,
                gender,
                age,
                alignment,
                role,
                features,
            )

        image_col1, image_col2, image_col3 = st.columns([1, 2, 1])

        with image_col2:
            st.image(
                image,
                width=450,
            )

        st.title(npc.name)

        col1, col2 = st.columns(2)

        with col1:

            st.write(f"**Раса:** {npc.race}")
            st.write(f"**Класс:** {npc.character_class}")
            st.write(f"**Пол:** {npc.gender}")
            st.write(f"**Возраст:** {npc.age}")

        with col2:

            st.write(f"**Мировоззрение:** {npc.alignment}")
            st.write(f"**Роль:** {npc.role}")

        st.divider()

        st.subheader("Внешность")

        st.write(npc.appearance)

        st.subheader("Характер")

        st.write(npc.personality)

        st.subheader("Мотивация")

        st.write(npc.motivation)

        st.subheader("Манера речи")

        st.write(npc.speech)

        st.subheader("Инвентарь")

        for item in npc.inventory:

            st.write(f"• {item}")