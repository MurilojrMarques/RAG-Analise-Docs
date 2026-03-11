import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    logger.error("A variável de ambiente GROQ_API_KEY não foi encontrada.")
    raise RuntimeError("GROQ_API_KEY ausente. Configure o arquivo .env.")

CHROMA_DB_DIR = "./chroma_db"