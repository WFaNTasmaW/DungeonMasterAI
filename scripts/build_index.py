from knowledge.loaders import (
    MonsterLoader,
    SpellLoader,
    ClassLoader,
)

from rag.embeddings import EmbeddingModel
from rag.indexer import Indexer
from rag.vector_store import VectorStore


def build_index():

    print("Loading data...")

    monsters = MonsterLoader().load()
    spells = SpellLoader().load()
    classes = ClassLoader().load()

    print(f"Monsters: {len(monsters)}")
    print(f"Spells: {len(spells)}")
    print(f"Classes: {len(classes)}")

    embedding_model = EmbeddingModel()
    vector_store = VectorStore()

    print("Cleaning old index...")

    vector_store.delete_all()

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    print("Indexing monsters...")

    for monster in monsters:

        document = Indexer.monster_to_document(monster)

        ids.append(monster.url)

        documents.append(document)

        embeddings.append(
            embedding_model.encode(document)
        )

        metadatas.append(
            {
                "type": "monster",
                "name": monster.name,
            }
        )

    print("Indexing spells...")

    for spell in spells:

        document = Indexer.spell_to_document(spell)

        ids.append(spell.url)

        documents.append(document)

        embeddings.append(
            embedding_model.encode(document)
        )

        metadatas.append(
            {
                "type": "spell",
                "name": spell.name,
            }
        )

    print("Indexing classes...")

    for character_class in classes:

        document = Indexer.class_to_document(character_class)

        ids.append(character_class.url)

        documents.append(document)

        embeddings.append(
            embedding_model.encode(document)
        )

        metadatas.append(
            {
                "type": "class",
                "name": character_class.name,
            }
        )

    print("Saving to ChromaDB...")

    vector_store.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print()

    print("=" * 50)
    print("Index successfully created!")
    print(f"Documents: {vector_store.count()}")
    print("=" * 50)


if __name__ == "__main__":
    build_index()