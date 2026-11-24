"""Build a small site with the installed theme and check the output."""

from __future__ import annotations

import subprocess
import sys
from importlib.metadata import entry_points
from pathlib import Path

import pytest

import zensical_gradient_theme as zgt


def test_entry_point_resolves_to_templates_dir() -> None:
    (ep,) = [e for e in entry_points(group="mkdocs.themes") if e.name == zgt.THEME_NAME]
    loaded = ep.load()
    assert Path(loaded.__file__).parent == zgt.get_theme_dir()


def test_theme_dir_contains_only_theme_files() -> None:
    theme_dir = zgt.get_theme_dir()
    assert (theme_dir / "mkdocs_theme.yml").is_file()
    assert (theme_dir / "main.html").is_file()
    assert not list(theme_dir.rglob("*.py")), "python files would be copied into sites"


@pytest.fixture(scope="module")
def built_site(tmp_path_factory: pytest.TempPathFactory) -> Path:
    root = tmp_path_factory.mktemp("site")
    (root / "docs" / "guide").mkdir(parents=True)
    (root / "docs" / "index.md").write_text("# Home\n\n[Guide](guide/index.md)\n")
    (root / "docs" / "guide" / "index.md").write_text("# Guide\n\n!!! note\n    Hi.\n")
    (root / "zensical.toml").write_text(
        '[project]\nsite_name = "Demo"\n\n[project.theme]\nname = "gradient"\n'
    )
    subprocess.run(
        [sys.executable, "-m", "zensical", "build", "--clean"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    return root / "site"


def test_assets_are_copied(built_site: Path) -> None:
    assert (built_site / "assets/stylesheets/gradient.css").is_file()
    assert (built_site / "assets/javascripts/gradient.js").is_file()


def test_no_python_files_leak_into_site(built_site: Path) -> None:
    leaked = [
        p
        for p in built_site.rglob("*")
        if p.suffix in {".py", ".pyc"} or p.name == "__pycache__"
    ]
    assert leaked == []


def test_root_page_links_assets_and_scheme(built_site: Path) -> None:
    html = (built_site / "index.html").read_text()
    assert 'href="./assets/stylesheets/gradient.css"' in html
    assert 'src="./assets/javascripts/gradient.js"' in html
    assert 'data-md-color-scheme="gradient-dark"' in html


def test_nested_page_uses_relative_asset_urls(built_site: Path) -> None:
    html = (built_site / "guide/index.html").read_text()
    assert 'href="../assets/stylesheets/gradient.css"' in html
    assert 'src="../assets/javascripts/gradient.js"' in html


def test_theme_defaults_are_applied(built_site: Path) -> None:
    html = (built_site / "index.html").read_text()
    assert "navigation.instant" in html
    assert "Roboto+Mono" in html or "Roboto Mono" in html
