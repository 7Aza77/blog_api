import os
from pathlib import Path

from decouple import Config, RepositoryEnv
from django.core.wsgi import get_wsgi_application

DEFAULT_ENV_ID: str = "local"
BASE_DIR: Path = Path(__file__).resolve().parent.parent
ENV_FILE: Path = BASE_DIR / "settings" / ".env"

if ENV_FILE.exists():
    _env_config: Config = Config(RepositoryEnv(str(ENV_FILE)))
    _env_id: str = _env_config("BLOG_ENV_ID", default=DEFAULT_ENV_ID)
else:
    _env_id = os.environ.get("BLOG_ENV_ID", DEFAULT_ENV_ID)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"settings.env.{_env_id}")

application = get_wsgi_application()
