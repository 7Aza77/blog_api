#!/usr/bin/env python
import os
import sys
from pathlib import Path

from decouple import Config, RepositoryEnv

DEFAULT_ENV_ID: str = "local"


def main() -> None:
    base_dir: Path = Path(__file__).resolve().parent
    env_file: Path = base_dir / "settings" / ".env"

    if env_file.exists():
        env_config: Config = Config(RepositoryEnv(str(env_file)))
        env_id: str = env_config("BLOG_ENV_ID", default=DEFAULT_ENV_ID)
    else:
        env_id = os.environ.get("BLOG_ENV_ID", DEFAULT_ENV_ID)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"settings.env.{env_id}")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
