import json
import time
from pathlib import Path

import requests


class DataImporter:

    BASE_URL = "https://www.dnd5eapi.co/api/2014"

    def __init__(self):

        self.session = requests.Session()

        self.download_dir = (
            Path(__file__).parents[1]
            / "downloads"
        )

        self.download_dir.mkdir(exist_ok=True)

    def fetch(self, url):

        response = self.session.get(
            url,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    def download_collection(
        self,
        endpoint,
        filename=None,
    ):

        print(f"\n========== {endpoint.upper()} ==========")

        url = f"{self.BASE_URL}/{endpoint}"

        data = self.fetch(url)

        results = data.get("results", [])

        print(f"Найдено объектов: {len(results)}")

        objects = []

        for index, item in enumerate(results, start=1):

            detail = self.fetch(
                f"https://www.dnd5eapi.co{item['url']}"
            )

            objects.append(detail)

            print(
                f"[{index}/{len(results)}] {item['name']}"
            )

            time.sleep(0.05)

        if filename is None:
            filename = endpoint

        output = self.download_dir / f"{filename}.json"

        with open(
            output,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                objects,
                f,
                ensure_ascii=False,
                indent=4,
            )

        print(f"\nСохранено -> {output}")