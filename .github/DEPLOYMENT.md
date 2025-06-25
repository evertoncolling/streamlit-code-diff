# Automated Deployment Setup

This document explains how to set up automated deployment for the `streamlit-code-diff` package using GitHub Actions.

## Overview

The project uses several GitHub Actions workflows:

1. **`ci.yml`** - Continuous Integration: Tests the package on multiple Python versions for every PR
2. **`publish.yml`** - Automated Publishing: Builds and publishes to PyPI when version is bumped, creates GitHub releases
3. **`manual-release.yml`** - Manual GitHub Release: Create releases manually without PyPI publishing
4. **`changelog.yml`** - Changelog Generation: Automatically generate changelogs from commit history

## Setup Instructions

### 1. Create PyPI API Tokens

#### For Production PyPI:
1. Go to [PyPI Account Settings](https://pypi.org/manage/account/)
2. Scroll to "API tokens" section
3. Click "Add API token"
4. Set:
   - Token name: `streamlit-code-diff-github-actions`
   - Scope: `Entire account` (or limit to specific project after first publish)
5. Copy the token (starts with `pypi-`)

#### For Test PyPI (Optional but Recommended):
1. Go to [Test PyPI Account Settings](https://test.pypi.org/manage/account/)
2. Follow the same process as above
3. Copy the token

### 2. Configure GitHub Repository Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** and add:

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `PYPI_API_TOKEN` | `pypi-AgE...` | Your PyPI API token |
| `TEST_PYPI_API_TOKEN` | `pypi-AgE...` | Your Test PyPI API token (optional) |

### 3. How the Automated Publishing Works

#### Version Detection
The workflow automatically detects version changes by:
1. Monitoring pushes to `main` branch that modify `pyproject.toml`
2. Comparing the version in the current commit vs. previous commit
3. Only proceeding if the version has changed

#### Build Process
When a version change is detected:
1. **Frontend Build**: Installs npm dependencies and builds the Vue.js component
2. **Python Build**: Uses `uv build` to create wheel and source distributions
3. **Testing**: Installs the built package to verify it works
4. **Publishing**: 
   - First publishes to Test PyPI (non-blocking)
   - Then publishes to production PyPI
5. **Release**: Creates a Git tag and GitHub release

## Usage

### Publishing a New Version

1. **Update the version** in `pyproject.toml`:
   ```toml
   [project]
   name = "streamlit-code-diff"
   version = "0.2.0"  # Bump this version
   ```

2. **Commit and push to main**:
   ```bash
   git add pyproject.toml
   git commit -m "Bump version to 0.2.0"
   git push origin main
   ```

3. **Monitor the workflow**:
   - Go to **Actions** tab in your GitHub repository
   - Watch the "Build and Publish to PyPI" workflow
   - Check for any errors in the logs

4. **Verify publication**:
   - Check [PyPI](https://pypi.org/project/streamlit-code-diff/)
   - Install the new version: `pip install streamlit-code-diff==0.2.0`

### Manual Publishing (if needed)

You can also trigger the publish workflow manually:
1. Go to **Actions** tab
2. Select "Build and Publish to PyPI"
3. Click "Run workflow"
4. Select the branch and click "Run workflow"

### Creating Manual Releases

To create a GitHub release without publishing to PyPI:
1. Go to **Actions** tab
2. Select "Manual GitHub Release"
3. Click "Run workflow"
4. Fill in:
   - **Tag name**: e.g., `v0.2.0`
   - **Release name**: e.g., `Release v0.2.0`
   - **Release notes**: Your changelog (supports Markdown)
   - **Pre-release**: Check if it's a beta/alpha release
   - **Draft**: Check to create as draft first

### Generating Changelogs

To automatically generate changelog from commit history:
1. Go to **Actions** tab
2. Select "Generate Changelog"
3. Click "Run workflow"
4. Fill in (all optional):
   - **From tag**: Starting tag (leave empty for last tag)
   - **To tag**: Ending tag (leave empty for HEAD)
   - **Output file**: Filename (default: CHANGELOG.md)
5. The workflow will create a PR with the generated changelog

## Development Workflow

### For Contributors

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Make your changes** (code, tests, documentation)

3. **Create a Pull Request**:
   - The CI workflow will automatically run
   - Tests will run on Python 3.8, 3.9, 3.10, 3.11, and 3.12
   - Frontend will be built and tested

4. **After PR is approved and merged**:
   - If you want to publish: bump the version in `pyproject.toml`
   - The publish workflow will automatically trigger

### Version Numbering

Follow [Semantic Versioning](https://semver.org/):
- **Patch** (0.1.0 → 0.1.1): Bug fixes
- **Minor** (0.1.0 → 0.2.0): New features, backward compatible
- **Major** (0.1.0 → 1.0.0): Breaking changes

## Troubleshooting

### Common Issues

1. **"Package already exists" error**:
   - You're trying to publish a version that already exists
   - Bump the version number in `pyproject.toml`

2. **"Authentication failed" error**:
   - Check that your PyPI API tokens are correctly set in GitHub secrets
   - Ensure tokens have the correct scope

3. **Frontend build fails**:
   - Check that `package.json` and `package-lock.json` are up to date
   - Verify Node.js dependencies are correct
   - Ensure the `build/` directory is created with bundle.js, bundle.css, and index.html

4. **Python build fails**:
   - Check that `pyproject.toml` is valid
   - Ensure all Python dependencies are correctly specified
   - For Python 3.13+: Ensure numpy>=1.26.0 (due to distutils removal)
   - Verify hatchling `artifacts` configuration includes frontend/build files

5. **"No such component directory" error after installation**:
   - Frontend build files weren't included in the wheel
   - Check wheel contents: `python -m zipfile -l dist/*.whl | grep build`
   - Ensure MANIFEST.in includes the build directory
   - Use the automated build script: `uv run python scripts/build_and_package.py`

### Debugging

1. **Check workflow logs**:
   - Go to Actions → Select failed workflow → Check logs

2. **Test locally**:
   ```bash
   # Run the same commands as the workflow
   cd src/streamlit_code_diff/frontend
   npm ci && npm run build
   cd ../../..
   uv build --wheel
   uv pip install dist/*.whl --force-reinstall
   ```

3. **Manual verification**:
   ```bash
   python -c "from streamlit_code_diff import st_code_diff; print('OK')"
   ```

## Security Notes

- API tokens are stored as encrypted secrets in GitHub
- Tokens are only accessible to the repository workflows
- Consider using project-scoped tokens for better security
- Regularly rotate your API tokens 