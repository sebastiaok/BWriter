from __future__ import annotations

from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None


def load_project_env(base_dir: Path) -> None:
    if load_dotenv is None:
        return
    env_path = base_dir / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=False)
