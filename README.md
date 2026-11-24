# zensical-gradient-theme

[![PyPI](https://img.shields.io/pypi/v/zensical-gradient-theme)](https://pypi.org/project/zensical-gradient-theme/)

A [Zensical](https://zensical.org) theme with animated rainbow-gradient accents
and purple light/dark color schemes. It started as the docs theme for
[rich-gradient](https://github.com/maxludden/rich-gradient) and works for any
Zensical (or Material-style) docs site.

What it gives you:

- `gradient-dark` and `gradient-light` color schemes, with a system / light /
  dark toggle
- Animated rainbow text on links, the active nav item and the site title, plus a
  rainbow rule under each `h1`. The animation stops when the reader asks for
  reduced motion.
- Calm, card-style API reference pages for
  [mkdocstrings](https://mkdocstrings.github.io/) output
- Inter and Roboto Mono fonts, the classic variant, and a sensible feature list
  (instant navigation, code copy, search suggestions and more)
- Copy-to-clipboard links with a toast

## Install

The theme is on [PyPI](https://pypi.org/project/zensical-gradient-theme/). Add
it to the dependency group that holds Zensical:

```shell
uv add --group docs zensical-gradient-theme
```

Or with pip:

```shell
pip install zensical-gradient-theme
```

To track unreleased changes, install from GitHub instead:

```shell
uv add --group docs "zensical-gradient-theme @ git+https://github.com/maxludden/zensical-gradient-theme"
```

## Use

In `zensical.toml`:

```toml
[project.theme]
name = "gradient"
logo = "img/logo.svg"      # optional
favicon = "img/logo.svg"   # optional
```

That's all: the theme's stylesheet and script load automatically, so you don't
need `extra_css` or `extra_javascript` entries for it. The same works in
`mkdocs.yml` with `theme: {name: gradient}`.

### Overriding defaults

The theme sets `variant`, `font`, `palette` and `features`. Any of these you set
in your own `[project.theme]` replaces the theme's value as a whole. For example,
setting `features` replaces the full list rather than adding to it. Copy the list
from `src/zensical_gradient_theme/templates/mkdocs_theme.yml` and edit it.

To restyle further, add your own `extra_css`. It loads after the theme's
stylesheet, so your rules win.

### Copy links

```html
<a class="copy-install" data-copy="uv add my-package" href="#">uv add my-package</a>
```

Clicking copies the `data-copy` text (or the link text, if there's no
`data-copy`) and shows a "Copied" toast.

### Extra classes

| Class | Effect |
| --- | --- |
| `table.params` | Wide parameter table with a solid header |
| `.badges` | Centers a row of badge images |
| `.version` | Accent-colored version label |
| `.banner` | Full-width image |
| `img[src$="#only-dark"]`, `#only-light` | Show an image in one scheme only |

## Development

```shell
uv sync
uv run pytest      # builds a fixture site with the theme and checks the output
uv run ruff check
uv run mypy
uv run zensical serve   # preview the demo site in docs/
```

### How the theme is found

Zensical loads installable themes from the `mkdocs.themes` entry-point group and
copies everything in the theme directory into the built site. The entry point
targets a small locator object whose `__file__` sits in `templates/`, so only
the templates and assets end up in sites, not the package's Python files.
`templates/mkdocs_theme.yml` is the one config file that does get copied.
