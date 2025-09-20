from dotenv import load_dotenv

# Charge automatiquement les variables définies dans le fichier .env à la racine du projet
load_dotenv()

from .main import app  # noqa: F401
