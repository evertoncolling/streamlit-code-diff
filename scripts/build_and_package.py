#!/usr/bin/env python3
"""
Build script for streamlit-code-diff component.
This script ensures the frontend is built before packaging.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run a command and handle errors."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {' '.join(cmd)}")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        sys.exit(1)
    return result


def main():
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    frontend_dir = project_root / "src" / "streamlit_code_diff" / "frontend"

    print("Building Streamlit Code Diff Component...")

    # Step 1: Install frontend dependencies
    print("\n1. Installing frontend dependencies...")
    run_command(["npm", "install"], cwd=frontend_dir)

    # Step 2: Build frontend
    print("\n2. Building frontend...")
    run_command(["npm", "run", "build"], cwd=frontend_dir)

    # Step 3: Verify build directory exists
    build_dir = frontend_dir / "build"
    if not build_dir.exists():
        print(f"Error: Build directory not found at {build_dir}")
        sys.exit(1)

    print(f"✓ Frontend built successfully at {build_dir}")

    # Step 4: Clean previous builds
    print("\n3. Cleaning previous builds...")
    dist_dir = project_root / "dist"
    if dist_dir.exists():
        import shutil

        shutil.rmtree(dist_dir)
        print("✓ Cleaned dist directory")

        # Step 5: Build the wheel
    print("\n4. Building Python wheel...")
    run_command(["uv", "build", "--wheel"], cwd=project_root)

    print("\n✅ Build completed successfully!")
    print(f"Wheel files are in: {project_root / 'dist'}")
    print("\nTo test your package locally:")
    print("uv pip install dist/*.whl")


if __name__ == "__main__":
    main()
