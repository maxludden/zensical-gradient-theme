# Installation

The Gradient Theme is published on
[PyPI](https://pypi.org) as
[`zensical-gradient-theme`](https://pypi.org/project/zensical-gradient-theme/). It needs Python 3.11 or newer and pulls in
[Zensical](https://zensical.org) as a dependency.

## With [uv](https://docs.astral.sh/uv/)

Add the theme to the dependency group that holds your docs tooling:

```shell
uv add --group docs zensical-gradient-theme
```

## With [pip](https://pypi.org/project/pip/)

```shell
pip install zensical-gradient-theme
```

## From GitHub

To try unreleased changes, install straight from the repository:

```shell
uv add --group docs "zensical-gradient-theme @ git+https://github.com/maxludden/zensical-gradient-theme"
```

## Check the install

The package registers a theme named `gradient`. Confirm it's visible to your
environment:

```shell
uv run python -c "from importlib.metadata import entry_points; print([e.name for e in entry_points(group='mkdocs.themes')])"
```

`gradient` should appear in the list. Next, head to
[Getting Started](getting-started.md) to turn it on.
