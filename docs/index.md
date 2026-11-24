![Zensical Gradient Theme Banner](img/zensical-gradient-theme-banner-light.svg#only-light)
![Zensical Gradient Theme Banner](img/zensical-gradient-theme-banner-dark.svg#only-dark)

# Zensical Gradient Theme

Gradient Theme is an installable [Zensical](https://zensical.org) theme that
adds animated rainbow gradients to your docs. Links, the site title, the rule
under each page title and every admonition shimmer over purple light and dark
color schemes. Install it from PyPI and set `name = "gradient"`; no extra CSS or
JavaScript is needed.

Links like [this one](https://zensical.org) and the active nav item shimmer with an animated rainbow. Inline code inside a link, like [`zensical build`](https://zensical.org), turns rainbow on hover.

## Admonitions

Every admonition gets an animated gradient border, a tinted title and a gradient-filled icon. Each type has its own gradient around its usual color, so you can tell them apart at a glance. Notes use the full rainbow and the gradient-bars icon.

!!! note
    The full rainbow, with the gradient-bars icon.

!!! abstract
    Sky blue to aqua.

!!! info
    Cyan to blue.

!!! tip
    Teal to mint.

!!! success
    Green to lime.

!!! question
    Lime to chartreuse.

!!! warning
    Amber to orange.

!!! failure
    Coral to pink.

!!! danger
    Crimson to ember.

!!! bug
    Magenta to violet.

!!! example
    Violet to lavender.

!!! quote
    Silver.

??? tip "A collapsible block"
    Collapsible blocks use their type's gradient too. Custom types without their own colors get the rainbow.

## Code and tables

```python
from rich_gradient import Text

print(Text("Hello, gradient!", colors=["#f00", "#00f"]))
```

| Option | Default |
| --- | --- |
| `variant` | `classic` |
| `palette` | `gradient-dark` / `gradient-light` |

Press ++ctrl+k++ or <kbd>⌘</kbd> <kbd>K</kbd> to search.

<a class="copy-install" data-copy="uv add zensical-gradient-theme" href="#">Copy the install command</a>
