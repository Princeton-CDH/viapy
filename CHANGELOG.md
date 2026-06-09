# CHANGELOG

## 0.6.0

### Development

- Fix GitHub Action for publishing package to PyPi
- Pin python version for development to 3.12 with `.python-version` file
- Add 7-day cooldown for uv
- Fix GitHub Action for publishing package to PyPi

#### Security

- Add pre-commit hook for zizmor a security-focused static analysis tool for GitHub Actions
- Pin GitHub repository references to full commit hashes for pre-commit and GitHub Actions
- Update permissionsfor GitHub Actions

#### Dependabot

- Add Dependabot version updates for uv
- Reduce Dependabot version updates to monthly and add 7-day cooldowns
- Configure Dependabot so all version updates will be grouped into one PR that targets the develop branch

## 0.5.0

- Now supports Python 3.10 through 3.14; drops support for Python 3.9
- Now supports Django 5.2 and 6.0; drops support for Django 3.2 through 5.0
- Switch project organization to src layout
- Update package to use pathlib instead of os.path

### Documentation

- Update readthedocs support and related documentation
- Switch from rst to md for documentation format
- Add GitHub Action for checking documentation coverage

### Development

- Switch to using uv for package development
- Adopt git-flow-next for git-flow branching conventions
- Add pre-commit hooks for development
- Adopt a new set of ruff linter rules
- Adopt Dependabot version updates for GitHub Actions and pre-commit
- Add GitHub Action for Ruff lint and format checks
- Add GitHub Action to check for changelog updates
- Add GitHub Action to check that pull requests align with git-flow workflow
- Add custom GitHub issue template for software releases
- Add custom config for codecov to create separate checks for the core package and tests

## 0.4.0

- Updates for new VIAF /search API endpoint response
- bugfix: VIAF entity request needs Accept header

## 0.3.0

- Handle negative years when parsing birth and death dates
- Now tested on python 3.9 through 3.12
- Now tested against Django 3.2 through 5.0
- Migrate continuous integration to GitHub Actions

## 0.2.0

- Now supports Django versions 1.11 through 3.0.

## 0.1.4

- Fix Travis-CI build for building with and without Django.

## 0.1.3

- Fix GitHub repository name in sphinx documentation config file.

## 0.1.2

- Update sphinx configuration to support building documentation on readthedocs.org

## 0.1.1

- Document permissions.

## 0.1.0

Initial release.

- Basic support for VIAP API use: autocomplete, SRU search, information
  about a single VIAF entity.
- Basic Django integration (optional); django-autocomplete-light lookup
  view and a VIAF url widget.
