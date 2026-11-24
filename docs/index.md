# Gradient theme

Links like [this one](https://zensical.org) and the active nav item shimmer with
an animated rainbow. Inline code inside a link, like [`zensical build`](https://zensical.org),
turns rainbow on hover.

!!! note
    Note admonitions use the gradient-bars icon.

```python
from rich_gradient import Text

print(Text("Hello, gradient!", colors=["#f00", "#00f"]))
```

| Option | Default |
| --- | --- |
| `variant` | `classic` |
| `palette` | `gradient-dark` / `gradient-light` |

<a class="copy-install" data-copy="uv add zensical-gradient-theme" href="#">Copy the install command</a>
