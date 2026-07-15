import json
import re
from pathlib import Path

import quickjs

SCRIPT_DIR = Path(__file__).parent

JS_FILE = SCRIPT_DIR / "tables.js"

OUTPUT_DIR = (
    SCRIPT_DIR.parents[1]
    / "knowledge"
    / "tables"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

def clean_text(text: str) -> str:

    if not text:
        return ""

    # <br> -> перенос строки
    text = re.sub(
        r"<br\s*/?>",
        "\n",
        text,
        flags=re.IGNORECASE
    )

    # удалить остальные HTML-теги
    text = re.sub(
        r"<[^>]+>",
        "",
        text
    )

    # HTML сущности
    html_entities = {
        "&nbsp;": " ",
        "&amp;": "&",
        "&quot;": "\"",
        "&#39;": "'",
        "&lt;": "<",
        "&gt;": ">"
    }

    for old, new in html_entities.items():
        text = text.replace(old, new)

    text = text.replace("\r", "")

    # убрать лишние пустые строки
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")

    # убрать лишние пробелы
    lines = [
        line.strip()
        for line in text.split("\n")
    ]

    text = "\n".join(lines)

    return text.strip()

def sanitize(name):

    bad = '\\/:*?"<>|'

    for c in bad:
        name = name.replace(c, "")

    return (
        name
        .replace("ё", "е")
        .replace(" ", "_")
        .lower()
    )

def extract_dice(table):

    for key in (
        "dice",
        "die",
        "dimension"
    ):

        if key in table:

            value = str(
                table[key]
            ).strip()

            if not value:
                return ""

            if value.upper().startswith("D"):
                return value.upper()

            return f"D{value}"

    return ""

def extract_roll(item):

    for key in (
        "roll",
        "value",
        "id",
        "index",
        "number"
    ):

        if key in item:

            return str(item[key]).strip()

    return ""

def extract_text(item):

    for key in (
        "text",
        "result",
        "description",
        "name"
    ):

        if key in item:

            return clean_text(
                str(item[key])
            )

    return ""

print()

print("Читаем JS...")

js = JS_FILE.read_text(
    encoding="utf-8"
)

ctx = quickjs.Context()

ctx.eval(js)

tables = json.loads(

    ctx.eval(
        "JSON.stringify(tablesData)"
    )

)

print(f"Найдено таблиц: {len(tables)}")

saved = 0

for table in tables:

    result = {

        "name": table.get(
            "tableName",
            "Без названия"
        ),

        "group": table.get(
            "groupName",
            ""
        ),

        "dice": extract_dice(table),

        "items": []

    }

    for item in table.get(
        "items",
        []
    ):

        result["items"].append(

            {

                "roll": extract_roll(item),

                "text": extract_text(item)

            }

        )

    filename = sanitize(
        result["name"]
    )

    with open(

        OUTPUT_DIR / f"{filename}.json",

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            result,

            f,

            ensure_ascii=False,

            indent=4

        )

    saved += 1

print()

print("=" * 50)

print("ГОТОВО")

print("=" * 50)

print(f"Таблиц сохранено : {saved}")

print(f"Папка            : {OUTPUT_DIR}")

print("=" * 50)