from data_importer import DataImporter


def main():

    importer = DataImporter()

    importer.download_collection(
        "equipment"
    )


if __name__ == "__main__":
    main()