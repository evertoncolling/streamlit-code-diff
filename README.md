# 🔍 Streamlit Code Diff

[![PyPI version](https://img.shields.io/pypi/v/streamlit-code-diff.svg)](https://pypi.org/project/streamlit-code-diff/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

A simple Streamlit component for code diff visualization using [v-code-diff](https://github.com/Shimada666/v-code-diff). Great for displaying code changes, git diffs, and side-by-side comparisons.

## Features
- **Automatic Theme Detection** - Adapts to Streamlit's light/dark theme
- **Multi-Language Support** - Syntax highlighting for 10+ programming languages
- **Customizable Display** - Side-by-side or line-by-line diff formats
- **Granular Diff Styles** - Word-level or character-level difference highlighting

<img width="1728" alt="image" src="https://github.com/user-attachments/assets/a30056f0-4ba4-4dc5-914e-be2e81c93bf3" />

## Installation

```bash
pip install streamlit-code-diff
```

## Quick Start

```python
import streamlit as st
from streamlit_code_diff import st_code_diff

old_code = """def hello():
    print("Hello")"""

new_code = """def hello(name="World"):
    print(f"Hello, {name}!")"""

# Display the diff
result = st_code_diff(
    old_string=old_code,
    new_string=new_code,
    language="python"
)

st.write(f"Changes detected: {result['isChanged']}")
```

## Parameters Reference

### `st_code_diff()`

Display a code diff visualization.

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `old_string` | `str` | **Required** | Original code content |
| `new_string` | `str` | **Required** | Modified code content |
| `language` | `str` | `"plaintext"` | Programming language for syntax highlighting |
| `output_format` | `"line-by-line"` \| `"side-by-side"` | `"side-by-side"` | Display format |
| `diff_style` | `"word"` \| `"char"` | `"word"` | Granularity of diff highlighting |
| `context` | `int` | `5` | Number of context lines around changes |
| `filename` | `str` \| `None` | `None` | Original filename to display |
| `new_filename` | `str` \| `None` | `None` | New filename to display |
| `theme` | `"light"` \| `"dark"` \| `None` | `None` | Force theme (auto-detects if None) |
| `trim` | `bool` | `True` | Remove leading/trailing whitespace |
| `no_diff_line_feed` | `bool` | `True` | Ignore line ending differences |
| `height` | `str` \| `None` | `None` | Maximum height (e.g., "300px", "50vh") |
| `force_inline_comparison` | `bool` | `False` | Force inline comparison (word/char level) |
| `hide_header` | `bool` | `False` | Hide header bar |
| `hide_stat` | `bool` | `False` | Hide statistical part in header bar |
| `ignore_matching_lines` | `str` \| `None` | `None` | Pattern to ignore matching lines (regex) |
| `key` | `str` \| `None` | `None` | Unique component key |

#### Returns

Returns a dictionary with diff statistics:

```python
{
    "isChanged": bool,    # Whether differences were detected
    "addNum": int,        # Number of added lines
    "delNum": int         # Number of deleted lines
}
```

## Supported Languages

The component supports syntax highlighting for:

- `plaintext` (default)
- `python`
- `javascript` / `js`
- `typescript` / `ts`
- `json`
- `yaml` / `yml`
- `java`
- `bash` / `shell`
- `sql`
- `html`
- `xml`
- `css`
- `markdown` / `md`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [v-code-diff](https://github.com/Shimada666/v-code-diff) - The core diff visualization library
- [Streamlit](https://streamlit.io/) - The amazing framework that makes this possible
- [highlight.js](https://highlightjs.org/) - Syntax highlighting support
