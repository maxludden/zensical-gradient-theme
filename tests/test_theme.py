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


def test_each_scheme_restates_admonition_colors() -> None:
    # The base theme computes admonition colors on :root from its light
    # defaults; without these, admonitions render white in dark mode.
    import re

    css = (zgt.get_theme_dir() / "assets/stylesheets/gradient.css").read_text()
    for scheme in ("gradient-dark", "gradient-light"):
        block = re.search(
            rf'\[data-md-color-scheme="{scheme}"\] \{{(.*?)\}}', css, re.S
        )
        assert block is not None
        assert "--md-admonition-bg-color" in block.group(1)
        assert "--md-admonition-fg-color" in block.group(1)


ADMONITION_TYPES = {
    "abstract": ("summary", "tldr"),
    "info": ("todo",),
    "tip": ("hint", "important"),
    "success": ("check", "done"),
    "question": ("help", "faq"),
    "warning": ("caution", "attention"),
    "failure": ("fail", "missing"),
    "danger": ("error",),
    "bug": (),
    "example": (),
    "quote": ("cite",),
}


def test_each_admonition_type_has_its_own_gradient() -> None:
    # Every built-in type and alias sets its three gradient stops, and the
    # rainbow fallback excludes exactly those types.
    import re

    css = (zgt.get_theme_dir() / "assets/stylesheets/gradient.css").read_text()
    stops: dict[str, tuple[str, ...]] = {}
    rules = re.findall(r"([^{}]+)\{([^{}]*--gradient-stop-1[^{}]*)\}", css)
    for selectors, body in rules:
        names = re.findall(r"\(\.admonition, details\)\.([a-z]+)", selectors)
        values = tuple(re.findall(r"--gradient-stop-\d:\s*([^;]+);", body))
        for name in names:
            stops[name] = values

    all_names = {n for t, aliases in ADMONITION_TYPES.items() for n in (t, *aliases)}
    assert set(stops) == all_names
    primaries = {stops[t] for t in ADMONITION_TYPES}
    assert len(primaries) == len(ADMONITION_TYPES), "two types share a gradient"
    for t, aliases in ADMONITION_TYPES.items():
        for alias in aliases:
            assert stops[alias] == stops[t]

    fallback = re.search(r":not\(([^)]*)\)\s*\{\s*--gradient-admonition", css)
    assert fallback is not None
    excluded = {n.strip(" .\n") for n in fallback.group(1).split(",")}
    assert excluded == all_names


@pytest.mark.parametrize(
    ("extra", "icon_path"),
    [
        ('repo_url = "https://github.com/me/demo"\n', "M216.5 362.5"),
        ('repo_url = "https://gitlab.com/me/demo"\n', "m504 204.6"),
        ('repo_url = "https://git.example.com/me/demo"\n', "M216.5 362.5"),
    ],
    ids=["github", "gitlab", "other-host-defaults-to-github"],
)
def test_repo_icon_follows_host(tmp_path: Path, extra: str, icon_path: str) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "index.md").write_text("# Home\n")
    (tmp_path / "zensical.toml").write_text(
        f'[project]\nsite_name = "Demo"\n{extra}\n[project.theme]\nname = "gradient"\n'
    )
    subprocess.run(
        [sys.executable, "-m", "zensical", "build", "--clean"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )
    html = (tmp_path / "site" / "index.html").read_text()
    source = html[html.index('class="md-source"') :]
    source = source[: source.index("</a>")]
    assert icon_path in source
