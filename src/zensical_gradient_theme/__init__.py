"""Gradient: an installable Zensical theme with animated rainbow accents.

Zensical discovers installable themes through the ``mkdocs.themes`` entry-point
group and uses the directory containing the loaded object's ``__file__`` as the
theme directory. Every file in that directory is copied into the built site, so
the entry point targets :data:`theme`, a small locator whose ``__file__`` sits
inside ``templates/``. That keeps this module (and its ``__pycache__``) out of
users' sites.
"""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

__all__ = ["THEME_NAME", "get_theme_dir", "theme"]

#: Name to use as ``theme.name`` in ``zensical.toml`` / ``mkdocs.yml``.
THEME_NAME = "gradient"

_TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"

#: Entry-point target. Zensical calls ``os.path.dirname(theme.__file__)``.
theme = SimpleNamespace(__file__=str(_TEMPLATES_DIR / "main.html"))


def get_theme_dir() -> Path:
    """Return the directory holding the theme's templates and assets.

    Returns:
        Absolute path to the ``templates`` directory shipped with the package.
    """
    return _TEMPLATES_DIR
