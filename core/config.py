from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "knowledge" / "data"
CHROMA_DB_PATH = BASE_DIR / "chroma_db"

MONSTERS_PATH = DATA_DIR / "monsters.json"
SPELLS_PATH = DATA_DIR / "spells.json"
CLASSES_PATH = DATA_DIR / "classes.json"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "llama-3.3-70b-versatile"
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "paraphrase-multilingual-MiniLM-L12-v2"
)