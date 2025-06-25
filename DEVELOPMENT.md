# Development Guide

This guide explains how to develop, build, and extend the `streamlit-code-diff` component.

## Architecture

The component consists of:

- **Python Package** (`src/streamlit_code_diff/`): Streamlit component API
- **Vue.js Frontend** (`src/streamlit_code_diff/frontend/`): TypeScript/Vue.js component using v-code-diff
- **Build System**: Uses `uv`/`hatchling` for Python packaging and `npm`/`vite` for frontend

### Key Build Configuration

The package uses hatchling with special configuration to include frontend build artifacts:

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/streamlit_code_diff"]
artifacts = ["src/streamlit_code_diff/frontend/build/*"]
```

This ensures the compiled frontend files (`bundle.js`, `bundle.css`, `index.html`) are included in the wheel.

## Development Setup

### Prerequisites

- Python 3.9+ (3.13+ requires numpy>=1.26.0 due to distutils removal)
- Node.js 16+
- uv (for Python package management)

### Initial Setup

```bash
# Clone the repository
git clone https://github.com/evertoncolling/streamlit-code-diff.git
cd streamlit-code-diff

# Install Python dependencies
uv sync

# Install frontend dependencies
cd src/streamlit_code_diff/frontend
npm install
```

### Development Workflow

#### Frontend Development

```bash
cd src/streamlit_code_diff/frontend

# Start development server
npm run dev

# Build for production
npm run build

# Type checking
npm run type-check
```

#### Testing the Component

```bash
# Build frontend first
cd src/streamlit_code_diff/frontend
npm run build

# Go back to root and test
cd ../../..
uv run streamlit run example_app.py
```

## Automated CI/CD

The project includes automated GitHub Actions workflows for continuous integration and deployment.

### Continuous Integration (CI)

- **Workflow**: `.github/workflows/ci.yml`
- **Triggers**: Pull requests and pushes to main (except version-only changes)
- **Tests**: Python 3.8-3.12 compatibility, frontend build, package installation

### Automated Publishing

- **Workflow**: `.github/workflows/publish.yml`
- **Triggers**: Version bumps in `pyproject.toml` pushed to main
- **Process**: Builds frontend → Builds Python package → Publishes to PyPI → Creates GitHub release

### Quick Version Bump

Use the helper script to bump versions easily:

```bash
# Bump patch version (0.1.0 → 0.1.1)
uv run python scripts/bump_version.py patch

# Bump minor version (0.1.0 → 0.2.0)
uv run python scripts/bump_version.py minor

# Bump major version (0.1.0 → 1.0.0)
uv run python scripts/bump_version.py major

# Set specific version
uv run python scripts/bump_version.py 1.2.3

# Dry run to see what would change
uv run python scripts/bump_version.py patch --dry-run
```

### Manual Build and Publish

If you need to build and publish manually:

```bash
# Option 1: Use the automated build script (recommended)
uv run python scripts/build_and_package.py

# Option 2: Manual steps
cd src/streamlit_code_diff/frontend && npm run build
cd ../../.. && uv build --wheel
uv publish dist/*  # Requires PyPI API token
```

#### Testing Your Package

After building, test your package locally:

```bash
# Install the wheel locally
uv pip install dist/*.whl

# Run the test script to verify everything works
uv run python scripts/test_package.py

# Or test manually in a new Python environment
uv run python -c "from streamlit_code_diff import st_code_diff; print('Package works!')"
```

#### Common Issues and Troubleshooting

**Problem**: "No such component directory" error when using installed package

**Solution**: This means the frontend build directory wasn't included in the wheel. Make sure:
1. Frontend is built: `cd src/streamlit_code_diff/frontend && npm run build`
2. Build directory exists: `ls src/streamlit_code_diff/frontend/build/`
3. MANIFEST.in includes the build directory
4. hatchling `artifacts` configuration is correct in pyproject.toml
5. Use the build script: `uv run python scripts/build_and_package.py`

**Problem**: Package installs but component doesn't render

**Solution**: 
1. Check if all frontend files are present: `uv run python scripts/test_package.py`
2. Verify bundle.js, bundle.css, and index.html are in the installed package
3. Make sure the component declaration path is correct in `__init__.py`
4. Test wheel contents: `python -m zipfile -l dist/*.whl | grep build`

See [`.github/DEPLOYMENT.md`](.github/DEPLOYMENT.md) for complete setup instructions.