from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pathlib import Path

import json
import re
import time


BASE_URL = "https://next.dnd.su"

ROOT_DIR = Path(__file__).resolve().parents[2]

OUTPUT_FILE = (
    ROOT_DIR
    / "knowledge"
    / "loot"
    / "mundane_items.json"
)

PROGRESS_FILE = (
    ROOT_DIR
    / "scripts"
    / "parse"
    / "equipment_progress.json"
)

def setup_driver():

    options = webdriver.ChromeOptions()

    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    options.add_argument(
        "--disable-blink-features=AutomationControlled"
    )

    options.add_argument(
        "user-agent=Mozilla/5.0"
    )

    service = Service(
        ChromeDriverManager().install()
    )

    return webdriver.Chrome(
        service=service,
        options=options,
    )

def clean_text(text):

    if not text:
        return ""

    text = text.replace("\xa0", " ")

    text = re.sub(r"\s+", " ", text)

    return text.strip()

def load_progress():

    if PROGRESS_FILE.exists():

        with open(
            PROGRESS_FILE,
            encoding="utf-8",
        ) as f:

            return json.load(f)

    return {

        "parsed_urls": [],

        "items": []

    }

def save_progress(progress):

    with open(
        PROGRESS_FILE,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            progress,
            f,
            ensure_ascii=False,
            indent=4,
        )

def save_items(items):

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            items,
            f,
            ensure_ascii=False,
            indent=4,
        )

def get_all_equipment_links(driver):

    print("Загружаем страницу со снаряжением...")

    driver.get(f"{BASE_URL}/equipment/")

    time.sleep(3)

    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);"
    )

    time.sleep(2)

    links = driver.find_elements(
        By.CSS_SELECTOR,
        'a[href*="/equipment/"]'
    )

    equipment_urls = []

    for link in links:

        href = link.get_attribute("href")

        if not href:
            continue

        if href == f"{BASE_URL}/equipment/":
            continue

        if "/equipment/" not in href:
            continue

        if href not in equipment_urls:

            equipment_urls.append(href)

    equipment_urls = sorted(equipment_urls)

    print(f"✓ Найдено предметов: {len(equipment_urls)}")

    return equipment_urls

def parse_equipment(driver, url):

    driver.get(url)

    time.sleep(1)

    item = {
        "url": url,
        "name": "",
        "category": "",
        "cost": "",
        "weight": "",
        "description": "",
    }

    try:

        card = driver.find_element(
            By.CSS_SELECTOR,
            "div.card.active",
        )

        try:

            title = card.find_element(
                By.CSS_SELECTOR,
                "h2.card-title"
            )

            name = clean_text(
                title.text.split("\n")[0]
            )

            # Убираем английское название
            name = re.sub(
                r"\s*\[.*?\]",
                "",
                name,
            ).strip()

            item["name"] = name

        except:
            pass

        # ---------- Параметры ----------

        params = card.find_elements(
            By.CSS_SELECTOR,
            "ul.params > li"
        )

        description = []

        for index, param in enumerate(params):

            text = clean_text(param.text)

            if not text:
                continue

            # Первая строка почти всегда категория
            if index == 0:

                item["category"] = text
                continue

            if text.startswith("Стоимость"):

                item["cost"] = (
                    text
                    .replace("Стоимость", "")
                    .replace(":", "")
                    .strip()
                )

                continue

            if text.startswith("Вес"):

                item["weight"] = (
                    text
                    .replace("Вес", "")
                    .replace(":", "")
                    .strip()
                )

                continue

            # Эти строки нам сейчас не нужны
            if text.startswith("Характеристика"):
                continue

            if text.startswith("Использование"):
                continue

            description.append(text)

        item["description"] = "\n".join(description)

        return item

    except Exception as e:

        print(f"Ошибка при парсинге {url}")
        print(e)

        return None
# -----------------------------------------------------


def main():

    print("Запускаем браузер...")

    driver = setup_driver()

    try:

        urls = get_all_equipment_links(driver)

        if not urls:

            print("Не удалось получить список предметов.")

            return

        progress = load_progress()

        parsed_urls = set(
            progress["parsed_urls"]
        )

        items = progress["items"]

        print(f"Всего найдено: {len(urls)}")
        print(f"Уже обработано: {len(parsed_urls)}")
        print()

        for index, url in enumerate(urls, start=1):

            if url in parsed_urls:
                continue

            print(f"[{index}/{len(urls)}] {url}")

            item = parse_equipment(
                driver,
                url,
            )

            if item:

                items.append(item)

                parsed_urls.add(url)

                print(f"✓ {item['name']}")

                if len(parsed_urls) % 10 == 0:

                    progress["parsed_urls"] = list(parsed_urls)
                    progress["items"] = items

                    save_progress(progress)
                    save_items(items)

                    print(
                        f"💾 Сохранено {len(items)} предметов"
                    )

            else:

                print("✗ Не удалось распарсить")

            time.sleep(0.5)

        progress["parsed_urls"] = list(parsed_urls)
        progress["items"] = items

        save_progress(progress)
        save_items(items)

        print("\n=========================")
        print("Парсинг завершён.")
        print(f"Предметов сохранено: {len(items)}")
        print(f"Файл: {OUTPUT_FILE}")
        print("=========================")

    finally:

        driver.quit()

if __name__ == "__main__":

    main()