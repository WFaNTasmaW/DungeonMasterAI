import json
from pathlib import Path

import streamlit as st

from services.table_service import TableService


st.set_page_config(
    page_title="Таблицы",
    page_icon="📚",
    layout="wide"
)

service = TableService()

FAVORITES_FILE = (
    Path(__file__).parents[2]
    / "knowledge"
    / "favorites.json"
)


def load_favorites():

    FAVORITES_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if not FAVORITES_FILE.exists():

        with open(
            FAVORITES_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                [],
                f,
                ensure_ascii=False,
                indent=4
            )

        return []

    with open(
        FAVORITES_FILE,
        encoding="utf-8"
    ) as f:

        return json.load(f)


def save_favorites(favorites):

    with open(
        FAVORITES_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            favorites,
            f,
            ensure_ascii=False,
            indent=4
        )


favorites = load_favorites()


if "selected_table" not in st.session_state:

    tables = service.get_tables()

    if tables:

        st.session_state.selected_table = tables[0].name

    else:

        st.session_state.selected_table = None


if "last_roll" not in st.session_state:

    st.session_state.last_roll = None


if "last_item" not in st.session_state:

    st.session_state.last_item = None


if "last_table" not in st.session_state:

    st.session_state.last_table = None


st.markdown("""
<style>

.block-container{
    padding-top:2rem;
}

.table-card{
    border:1px solid #30363d;
    border-radius:10px;
    padding:15px;
    margin-bottom:10px;
    background:#1b1d22;
}

.result-card{
    border:2px solid #4a90e2;
    border-radius:12px;
    padding:20px;
    background:#18283b;
    margin-bottom:20px;
}

.result-roll{
    font-size:42px;
    font-weight:bold;
    text-align:center;
}

.highlight{
    border-left:6px solid #4a90e2;
    background:#223347;
}

</style>
""", unsafe_allow_html=True)


st.title("📚 Таблицы")

left, right = st.columns(
    [1, 3],
    gap="large"
)
with left:

    search = st.text_input(
        "🔍 Поиск",
        placeholder="Название таблицы..."
    )

    st.markdown("### ⭐ Избранное")

    if favorites:

        for name in favorites:

            if st.button(
                name,
                key=f"fav_{name}",
                use_container_width=True
            ):

                st.session_state.selected_table = name

                st.session_state.last_item = None

                st.rerun()

    else:

        st.caption("Нет избранных таблиц")

    st.divider()

    st.markdown("### 📚 Все таблицы")

    tables = service.search(search) if search else service.get_tables()

    for table in tables:

        selected = (
            table.name
            == st.session_state.selected_table
        )

        col1, col2 = st.columns(
            [6, 1]
        )

        with col1:

            label = table.name

            if selected:

                label = "▶ " + label

            if st.button(
                label,
                key=f"table_{table.name}",
                use_container_width=True
            ):

                st.session_state.selected_table = table.name

                st.session_state.last_item = None

                st.rerun()

        with col2:

            if table.name in favorites:

                if st.button(
                    "⭐",
                    key=f"star_{table.name}"
                ):

                    favorites.remove(table.name)

                    save_favorites(favorites)

                    st.rerun()

            else:

                if st.button(
                    "☆",
                    key=f"empty_{table.name}"
                ):

                    favorites.append(table.name)

                    save_favorites(favorites)

                    st.rerun()
with right:

    if st.session_state.selected_table is None:

        st.info("Выберите таблицу слева.")

    else:

        table = service.get(
            st.session_state.selected_table
        )

        st.subheader(table.name)

        if table.group:
            st.caption(table.group)

        col1, col2 = st.columns([1, 1])

        with col1:

            if table.dice:

                st.info(f"🎲 {table.dice}")

            else:

                st.info("Без броска")

        with col2:

            if st.button(
                "🎲 Новый результат",
                use_container_width=True
            ):

                result = service.random_result(
                    table.name
                )

                st.session_state.last_roll = result["roll"]

                st.session_state.last_item = result["item"]

                st.session_state.last_table = result["table"]

                st.rerun()

        st.write("")

        if (
                st.session_state.last_table
                and
                st.session_state.last_table.name == table.name
                and
                st.session_state.last_item is not None
                and
                st.session_state.last_roll is not None
        ):
            item = st.session_state.last_item

            st.markdown(
                f"""
                <div class="result-card">
                    <h4 style="margin-top:0; margin-bottom:15px;">🎲 Выпало</h4>
                    <div style="font-size: 16px;">
                        {st.session_state.last_roll}<br> {item.text}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.info(
                "Нажмите «🎲 Новый результат»."
            )

        st.divider()

        st.subheader("Таблица")
        for item in table.items:

            selected = False

            if (
                    st.session_state.last_item is not None
                    and
                    st.session_state.last_item.roll == item.roll
                    and
                    st.session_state.last_item.text == item.text
            ):
                selected = True

            css = "table-card"
            if selected:
                css += " highlight"

            # ВАЖНО: Первая строка f-строки начинается сразу с <div>, без пробелов!
            st.markdown(
                f"""<div class="{css}">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                <span style="font-size: 18px;">🎲</span>
                <span style="font-weight: 600; font-size: 18px;">{item.roll}</span>
            </div>
            <div style="font-size: 15px; line-height: 1.5; color: #e6edf3;">
                {item.text}
            </div>
        </div>""",
                unsafe_allow_html=True
            )