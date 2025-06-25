# Development Guide

This guide explains how to develop, build, and extend the `streamlit-code-diff` component.

## Architecture

The component consists of:

- **Python Package** (`src/streamlit_code_diff/`): Streamlit component API
- **Vue.js Frontend** (`src/streamlit_code_diff/frontend/`): TypeScript/Vue.js component using v-code-diff
- **Build System**: Uses `uv` for Python packaging and `npm`/`vite` for frontend

## Development Setup

### Prerequisites

- Python 3.8+
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
python scripts/bump_version.py patch

# Bump minor version (0.1.0 → 0.2.0)
python scripts/bump_version.py minor

# Bump major version (0.1.0 → 1.0.0)
python scripts/bump_version.py major

# Set specific version
python scripts/bump_version.py 1.2.3

# Dry run to see what would change
python scripts/bump_version.py patch --dry-run
```

### Manual Build and Publish

If you need to build and publish manually:

```bash
cd src/streamlit_code_diff/frontend && npm run build
cd ../../.. && uv build
uv publish dist/*  # Requires PyPI API token
```

See [`.github/DEPLOYMENT.md`](.github/DEPLOYMENT.md) for complete setup instructions.