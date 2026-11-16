from pathlib import Path

from decouple import Config, RepositoryEnv

BASE_DIR: Path = Path(__file__).resolve().parent.parent
ENV_FILE: Path = BASE_DIR / "settings" / ".env"

if ENV_FILE.exists():
    _config: Config = Config(RepositoryEnv(str(ENV_FILE)))
else:
    from decouple import config as _default_config

    _config = _default_config

ENV_ID: str = _config("BLOG_ENV_ID", default="local")
SECRET_KEY: str = _config("BLOG_SECRET_KEY", default="django-insecure-default-change-me")
DEBUG: bool = _config("BLOG_DEBUG", default=False, cast=bool)
ALLOWED_HOSTS: list[str] = [
    host.strip()
    for host in _config("BLOG_ALLOWED_HOSTS", default="127.0.0.1,localhost").split(",")
    if host.strip()
]

DB_NAME: str = _config("BLOG_DB_NAME", default="blog_api")
DB_USER: str = _config("BLOG_DB_USER", default="postgres")
DB_PASSWORD: str = _config("BLOG_DB_PASSWORD", default="postgres")
DB_HOST: str = _config("BLOG_DB_HOST", default="localhost")
DB_PORT: str = _config("BLOG_DB_PORT", default="5432")
