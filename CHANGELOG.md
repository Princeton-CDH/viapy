# CHANGELOG

## 0.5

- Now supports Python 3.10 through 3.14; drops support for Python 3.9
- Now supports Django 5.2 and 6.0; drops support for Django 3.2 through 5.0
- Adopt a new set of ruff linter rules
- Add GitHub Action for ruff lint and format checks
- Add GitHub Action to check for changelog updates
- Add GitHub Action for publishing documentation to GitHub Pages
- Add pre-commit hooks for development
- Switch to using uv for package development
- Switch project organization to src layout
- Switch from os.path to pathlib
- Switch from rst to md for documentation format

## 0.4

- Updates for new VIAF /search API endpoint response
- bugfix: VIAF entity request needs Accept header

## 0.3

- Handle negative years when parsing birth and death dates
- Now tested on python 3.9 through 3.12
- Now tested against Django 3.2 through 5.0
- Migrate continuous integration to GitHub Actions

## 0.2

- Now supports Django versions 1.11 through 3.0.

## 0.1.4

- Fix Travis-CI build for building with and without Django.

## 0.1.3

- Fix GitHub repository name in sphinx documentation config file.

## 0.1.2

- Update sphinx configuration to support building documentation on readthedocs.org

## 0.1.1

- Document permissions.

## 0.1

Initial release.

- Basic support for VIAP API use: autocomplete, SRU search, information
  about a single VIAF entity.
- Basic Django integration (optional); django-autocomplete-light lookup
  view and a VIAF url widget.
