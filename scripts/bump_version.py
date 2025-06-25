#!/usr/bin/env python3
"""
Version Bumping Script for streamlit-code-diff

This script helps bump the version in pyproject.toml following semantic versioning.
"""

import re
import sys
import argparse
from pathlib import Path


def get_current_version():
    """Get the current version from pyproject.toml"""
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        raise FileNotFoundError("pyproject.toml not found in current directory")

    content = pyproject_path.read_text()
    version_match = re.search(r'version = "([^"]+)"', content)
    if not version_match:
        raise ValueError("Version not found in pyproject.toml")

    return version_match.group(1)


def parse_version(version_str):
    """Parse a semantic version string into major, minor, patch"""
    match = re.match(r"(\d+)\.(\d+)\.(\d+)", version_str)
    if not match:
        raise ValueError(f"Invalid version format: {version_str}")

    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def bump_version(current_version, bump_type):
    """Bump the version based on the bump type"""
    major, minor, patch = parse_version(current_version)

    if bump_type == "major":
        return f"{major + 1}.0.0"
    elif bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    elif bump_type == "patch":
        return f"{major}.{minor}.{patch + 1}"
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")


def update_version_in_file(new_version):
    """Update the version in pyproject.toml"""
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()

    new_content = re.sub(r'version = "[^"]+"', f'version = "{new_version}"', content)

    pyproject_path.write_text(new_content)


def main():
    parser = argparse.ArgumentParser(
        description="Bump version in pyproject.toml",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/bump_version.py patch    # 0.1.0 -> 0.1.1
  python scripts/bump_version.py minor    # 0.1.0 -> 0.2.0
  python scripts/bump_version.py major    # 0.1.0 -> 1.0.0
  python scripts/bump_version.py 0.2.5    # Set specific version

Semantic Versioning Guide:
  patch - Bug fixes, no new features
  minor - New features, backward compatible
  major - Breaking changes
        """,
    )

    parser.add_argument(
        "version",
        help="Version bump type (patch/minor/major) or specific version (e.g., 1.2.3)",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without making changes",
    )

    args = parser.parse_args()

    try:
        current_version = get_current_version()
        print(f"Current version: {current_version}")

        # Check if it's a bump type or specific version
        if args.version in ["major", "minor", "patch"]:
            new_version = bump_version(current_version, args.version)
        else:
            # Validate the specific version format
            parse_version(args.version)  # This will raise if invalid
            new_version = args.version

        print(f"New version: {new_version}")

        if args.dry_run:
            print("(Dry run - no changes made)")
            return

        # Ask for confirmation
        response = input("Update version? [y/N]: ")
        if response.lower() not in ["y", "yes"]:
            print("Cancelled")
            return

        update_version_in_file(new_version)
        print(f"✅ Version updated to {new_version}")
        print()
        print("Next steps:")
        print("1. Review the changes: git diff pyproject.toml")
        print(
            "2. Commit and push: git add pyproject.toml && git commit -m 'Bump version to {}'".format(
                new_version
            )
        )
        print("3. Push to main: git push origin main")
        print("4. GitHub Actions will automatically publish to PyPI")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
