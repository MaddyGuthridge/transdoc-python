# 🏳️‍⚧️🐍 Transdoc Python

A Transdoc handler for Python docstrings.

## Installation

```sh
pip install transdoc[python]
```

## Usage

Transdoc rules are applied to Python docstrings.

For example, given the following rule:

```py
def mdn_link(e: str) -> str:
    '''
    Return a Markdown-formatted link to MDN's documentation of an HTML element.
    '''
    return (
        f"[View `<{e}>` on MDN]"
        f"(https://developer.mozilla.org/en-US/docs/Web/HTML/Element/{e})"
    )
```

The following Python function's docstring would be transformed as follows:

```py
# Before
def make_link(text: str, href: str) -> str:
    '''
    Generate an HTML link.
    {{mdn_link[a]}}
    '''
    # Please don't write code this insecure in real life
    return f"<a href={href}>{text}</a>"

# After
def make_link(text: str, href: str) -> str:
    '''
    Generate an HTML link.
    [View `<a>` on MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a)
    '''
    # Please don't write code this insecure in real life
    return f"<a href={href}>{text}</a>"
```
