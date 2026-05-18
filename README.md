# viapy

<!-- % sphinx-start-marker-do-not-remove
% -->

*VIAF via Python*

Python module for interacting with [VIAF](https://viaf.org) (the Virtual International
Authority File) data and APIs.

**viapy** provides optional Django integration; this currently includes a
django-autocomplete-light lookup view and a VIAF url widget.

[![unit tests](https://github.com/Princeton-CDH/viapy/actions/workflows/unit_tests.yml/badge.svg)](https://github.com/Princeton-CDH/viapy/actions/workflows/unit_tests.yml)
[![codecov](https://codecov.io/gh/Princeton-CDH/viapy/branch/master/graph/badge.svg)](https://codecov.io/gh/Princeton-CDH/viapy/branch/master)
[![CodeFactor](https://www.codefactor.io/repository/github/princeton-cdh/viapy/badge)](https://www.codefactor.io/repository/github/princeton-cdh/viapy)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/viapy)](https://pypi.org/project/viapy/)
[![PyPI - Django Version](https://img.shields.io/pypi/djversions/viapy)](https://pypi.org/project/viapy/)

## Installation

Use pip to install from GitHub. Use a branch or tag name, e.g.
`@develop` or `@1.0` if you want to install a specific tagged release or branch:

```sh
pip install git+https://github.com/Princeton-CDH/viapy.git@develop#egg=viapy
```

## Configuration for use with Django

Using `viapy` with Django requires additional configuration. Add `viapy` to
installed applications along with the needed django-autocomplete-light
modules:

```python
INSTALLED_APPS = (
    ...
    'dal',
    'dal_select2',
    'viapy',
    ...
)
```

Include the viapy urls at the desired base url with the namespace:

```python
urlpatterns = [
    ...
    path(r'viaf/', include('viapy.urls', namespace='viaf')),
    ...
]
```

## Development instructions

This project uses git flow branching conventions via [git-flow-next](https://github.com/gittower/git-flow-next).

> [!NOTE]
> Make sure you are using the correct version of git flow.
> The original [git-flow](https://github.com/nvie/gitflow) and its successor [git-flow-avh](https://github.com/petervanderdoes/gitflow-avh) are no longer maintained.
> While `git-flow-next` is backwards compatible, this project assumes the workflow and features of `git-flow-next`.

For development, we assume the usage of [uv](https://docs.astral.sh/uv/).
`uv` is compatible with the use of `pip` for python package management
and a tool of your choice for creating python virtual environments
(e.g., `mamba`, `venv`).

### Initial setup and installation

Install `uv` if it's not installed.
It can be installed via PyPi, Homebrew, or a standalone installer.
See uv's [installation documentation](https://docs.astral.sh/uv/getting-started/installation)
for more details.

To explicitly sync the project's dependencies, including optional dependencies
for development and testing, to your local environment run:

```sh
uv sync
```

Note that `uv` performs syncing and locking automatically (e.g., any time
`uv run` is invoked). By default, syncing will remove any packages not
specifically specified in the `pyproject.toml`.

#### Initialize and configure git-flow in your local repository

Install `git-flow-next` if it's not installed.
It can be installed via Homebrew or manual installation.
See `git-flow-next`'s [installation documentation](https://git-flow.sh/docs/installation/) for more details.

To initialize git-flow run:

```sh
git flow init --preset=classic --defaults
```

This package uses custom configurations options for git-flow including the use of custom git-flow hooks which are defined in `gitflow-hooks`.
Run the provided `setup_gitflow.sh` script to update git-flow's configuration.

```sh
sh setup_gitflow.sh
```

These configuration options are set in the local git config (`.git/config`).

To display an overview of the current git-flow configuration, branch structure, and workflow status run:

```sh
git flow overview
```

#### Install pre-commit hooks

Anyone who wants to contribute to this codebase should install the configured pre-commit hooks.

To install pre-commit run:

```sh
uv tool install pre-commit --with pre-commit-uv
```

To install the configure pre-commit hooks run:

```sh
pre-commit install
```

This will configure a pre-commit hooks to automatically lint and format python code with [ruff](https://github.com/astral-sh/ruff) and [black](https://github.com/psf/black).

To run pre-commit explicitly run:

```sh
pre-commit run --all-files
```

### Unit Testing

Unit tests are set up to be run with [pytest](https://docs.pytest.org/).

- Copy sample test settings and add a **SECRET_KEY**:

  ```sh
  cp ci/testsettings.py testsettings.py
  ```

- To run the tests, run:

  ```sh
  uv run pytest
  ```

### Documentation

Documentation is generated using [sphinx](https://www.sphinx-doc.org/).

Then build the documentation using the customized make file in the `docs`
directory:

```sh
cd sphinx-docs
uv run make html
```

When building documentation for a production release, use `make docs` to
update the published documentation on GitHub Pages.

To check documentation coverage, run:

```sh
uv make html -b coverage
```

This will create a file under `_build/coverage/python.txt` listing any Python classes or methods
that are not documented. Note that sphinx can only report on code coverage for files that are
included in the documentation. If a new Python file is created but not included in the sphinx
documentation, it will be omitted.

## License

**viapy** is distributed under the Apache 2.0 License.

©2024-2026 Trustees of Princeton University. Permission granted via
Princeton Docket #18-3449-1 for distribution online under a standard Open Source
license. Ownership rights transferred to Rebecca Koeser provided software
is distributed online via open source.
