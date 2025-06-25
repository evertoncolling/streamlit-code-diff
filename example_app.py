"""
Streamlit Code Diff Component - Example Application

This example demonstrates all the features of the streamlit-code-diff component.
"""

import streamlit as st
from streamlit_code_diff import st_code_diff

# Configure page
st.set_page_config(
    page_title="Streamlit Code Diff Demo",
    page_icon=":material/difference:",
    layout="wide",
)

st.title(":material/difference: Streamlit Code Diff Demo")
st.caption(
    "**Beautiful code diff visualization in Streamlit using [v-code-diff](https://github.com/Shimada666/v-code-diff)**"
)

# Sample code for demonstration
old_python_code = """def hello_world():
    print("Hello, World!")
    return "old version"

def calculate_sum(a, b):
    return a + b

class Calculator:
    def add(self, x, y):
        return x + y"""

new_python_code = '''def hello_world(name="World"):
    """Greet someone by name."""
    print(f"Hello, {name}!")
    return f"Hello, {name}!"

def calculate_sum(a, b, c=0):
    """Calculate sum of two or three numbers."""
    return a + b + c

def goodbye():
    print("Goodbye!")

class Calculator:
    def __init__(self):
        self.history = []

    def add(self, x, y):
        result = x + y
        self.history.append(f"{x} + {y} = {result}")
        return result

    def multiply(self, x, y):
        result = x * y
        self.history.append(f"{x} * {y} = {result}")
        return result'''

# Configuration options
with st.sidebar:
    st.header(":material/settings: Configuration options")

    selected_language = st.selectbox(
        "Language",
        [
            "python",
            "javascript",
            "json",
            "yaml",
            "java",
            "bash",
            "sql",
            "html",
            "xml",
            "plaintext",
        ],
        index=0,
    )

    output_format = st.radio("Output Format", ["side-by-side", "line-by-line"], index=0)

    diff_style = st.radio("Diff Style", ["word", "char"], index=0)

    context_lines = st.slider("Context Lines", min_value=1, max_value=10, value=5)

    trim_whitespace = st.checkbox("Trim Whitespace", value=True)
    ignore_line_endings = st.checkbox("Ignore Line Endings", value=True)
    component_height = st.text_input("Height (CSS)", placeholder="e.g., 400px, 50vh")

    force_inline = st.checkbox("Force Inline Comparison", value=True)
    hide_header = st.checkbox("Hide Header", value=False)
    hide_stat = st.checkbox("Hide Statistics", value=False)
    ignore_pattern = st.text_input(
        "Ignore Pattern (regex)", placeholder="e.g., (debug|timestamp)"
    )

# Custom code input
st.subheader("Try Your Own Code")

col1, col2 = st.columns(2)

with col1:
    st.write("**Original Code:**")
    custom_old_code = st.text_area(
        "Enter original code", value=old_python_code, height=200, key="old_code"
    )

with col2:
    st.write("**Modified Code:**")
    custom_new_code = st.text_area(
        "Enter modified code", value=new_python_code, height=200, key="new_code"
    )

# Custom diff
st.subheader("Your Custom Diff")
custom_result = st_code_diff(
    old_string=custom_old_code,
    new_string=custom_new_code,
    language=selected_language,
    output_format=output_format,
    diff_style=diff_style,
    context=context_lines,
    trim=trim_whitespace,
    no_diff_line_feed=ignore_line_endings,
    height=component_height if component_height else None,
    force_inline_comparison=force_inline,
    hide_header=hide_header,
    hide_stat=hide_stat,
    ignore_matching_lines=ignore_pattern if ignore_pattern else None,
    key="custom_diff",
)

st.json(custom_result)
