# Getting Started

Once the theme is [installed](installation.md), switching a site over takes one
setting.

## Turn on the theme

In `zensical.toml`:

```toml
[project.theme]
name = "gradient"
logo = "img/logo.svg"      # optional
favicon = "img/logo.svg"   # optional
```

Using `mkdocs.yml` instead? The same works there:

```yaml
theme:
  name: gradient
```

The theme's stylesheet and script load automatically, so you don't need
`extra_css` or `extra_javascript` entries for them. Preview the result with:

```shell
uv run zensical serve
```

## Link to your repository

Set `repo_url` and the header shows a link to the repository in the top right,
with its star and fork counts. `repo_name` sets the label:

```toml
[project]
repo_name = "my-package"
repo_url = "https://github.com/me/my-package"
```

The icon follows the host: the GitHub logo by default, or the GitLab or
Bitbucket logo when `repo_url` points there. To use a different icon, set it
yourself:

```toml
[project.theme.icon]
repo = "fontawesome/brands/git-alt"
```

## Recommended Markdown extensions

The theme styles admonitions, tabs, code blocks and keyboard keys. Enable the
extensions that produce them:

```toml
[project.markdown_extensions.admonition]
[project.markdown_extensions.attr_list]
[project.markdown_extensions.md_in_html]
[project.markdown_extensions.toc]
permalink = true
[project.markdown_extensions.pymdownx.highlight]
anchor_linenums = true
[project.markdown_extensions.pymdownx.superfences]
[project.markdown_extensions.pymdownx.details]
[project.markdown_extensions.pymdownx.tabbed]
alternate_style = true
[project.markdown_extensions.tables]
[project.markdown_extensions.pymdownx.keys]
```

## Override the defaults

The theme sets `variant`, `font`, `palette` and `features`. Any of these you set
in your own `[project.theme]` replaces the theme's value as a whole. Setting
`features`, for example, replaces the full list rather than adding to it, so
copy the list from the theme's `mkdocs_theme.yml` and edit it:

```toml
[project.theme]
name = "gradient"
features = [
    "navigation.instant",
    "navigation.sections",
    "content.code.copy",
]
```

To restyle further, add your own `extra_css`. It loads after the theme's
stylesheet, so your rules win.

## Copy links

Any link with the `copy-install` class copies text to the clipboard and shows a
"Copied" toast:

```html
<a class="copy-install" data-copy="uv add my-package" href="#">uv add my-package</a>
```

It copies the `data-copy` value, or the link text when there's no `data-copy`.

## Extra classes

| Class | Effect |
| --- | --- |
| `table.params` | Wide parameter table with a solid header |
| `.badges` | Centers a row of badge images |
| `.version` | Accent-colored version label |
| `.banner` | Full-width image |
| `img[src$="#only-dark"]`, `#only-light` | Show an image in one scheme only |
