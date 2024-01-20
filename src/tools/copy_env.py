import os
import shutil

BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

shutil.copy(f"{BACKEND_DIR}/src/config/.env.example", f"{BACKEND_DIR}/src/config/.env")
