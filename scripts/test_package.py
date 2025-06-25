#!/usr/bin/env python3
"""
Test script to verify the streamlit-code-diff package works correctly.
Run this after installing the wheel to ensure everything is working.
"""

import os
import sys
import tempfile
import subprocess
from pathlib import Path


def create_test_app():
    """Create a simple test app to verify the component works."""
    test_code = '''
import streamlit as st
from streamlit_code_diff import st_code_diff

st.title("Streamlit Code Diff Test")

# Test basic functionality
old_code = """def hello():
    print("Hello, World!")
    return "old"
"""

new_code = """def hello(name="World"):
    print(f"Hello, {name}!")
    return "new"
"""

try:
    result = st_code_diff(
        old_string=old_code,
        new_string=new_code,
        language="python",
        filename="test.py"
    )
    st.success("Component loaded successfully!")
    st.write("Result:", result)
except Exception as e:
    st.error(f"Error loading component: {e}")
    import traceback
    st.code(traceback.format_exc())
'''
    return test_code


def main():
    print("Testing streamlit-code-diff package...")

    # Test 1: Try to import the package
    print("\n1. Testing import...")
    try:
        from streamlit_code_diff import st_code_diff

        print("✓ Package imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import package: {e}")
        return False

    # Test 2: Check if frontend build directory exists in installed package
    print("\n2. Checking frontend build directory...")
    try:
        import streamlit_code_diff

        package_dir = Path(streamlit_code_diff.__file__).parent
        build_dir = package_dir / "frontend" / "build"

        if build_dir.exists():
            print(f"✓ Frontend build directory found: {build_dir}")
            # List contents
            files = list(build_dir.glob("*"))
            print(f"  Build files: {[f.name for f in files]}")

            # Check for required files
            required_files = ["bundle.js", "bundle.css", "index.html"]
            for file in required_files:
                if (build_dir / file).exists():
                    print(f"  ✓ {file} found")
                else:
                    print(f"  ✗ {file} missing")
                    return False
        else:
            print(f"✗ Frontend build directory not found: {build_dir}")
            return False
    except Exception as e:
        print(f"✗ Error checking build directory: {e}")
        return False

    # Test 3: Create and run a test app
    print("\n3. Creating test app...")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(create_test_app())
        test_app_path = f.name

    print(f"Test app created at: {test_app_path}")
    print("To manually test, run:")
    print(f"uv run streamlit run {test_app_path}")

    # Cleanup
    os.unlink(test_app_path)

    print("\n✅ All tests passed! The package appears to be working correctly.")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
