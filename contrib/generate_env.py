from pathlib import Path
from django.core.management.utils import get_random_secret_key

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_VARIABLES = f"""SECRET_KEY={get_random_secret_key()}
DEBUG=True
ALLOWED_HOSTS=*
"""

file = open(f"{BASE_DIR}/concord/.env", "w")
file.write(ENV_VARIABLES)
