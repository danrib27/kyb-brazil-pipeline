# AGENTS.md

Context and rules for AI coding agents working in this repository.

## Project

Know-Your-Business (KYB) pipeline that flags risky Brazilian government
suppliers by cross-referencing three kinds of public data:

- **Company registry**: the open data on companies registered with a
  CNPJ (Cadastro Nacional da Pessoa Jurídica), published by the Receita
  Federal. It covers companies, establishments and the partners and
  administrators of each company (QSA, Quadro de Sócios e
  Administradores).
- **Public procurement**: government contracts and bids, for example
  from the PNCP (Portal Nacional de Contratações Públicas) and the
  Portal da Transparência.
- **Sanctions lists**: the lists maintained by the CGU
  (Controladoria-Geral da União), such as the CEIS (Cadastro Nacional
  de Empresas Inidôneas e Suspensas) and the CNEP (Cadastro Nacional de
  Empresas Punidas).

The project is at an early stage. Most of the layout below is planned
and not built yet.

## Layout

- `src/kyb_brazil_pipeline/`: the Python package, in the src layout,
  built with `uv_build`. The `kyb-brazil-pipeline` command line entry
  point is the function `kyb_brazil_pipeline:main`.
- `tests/`: automated tests.
- `infra/`: infrastructure as code.
- `docs/`: project documentation.

## Tooling

- Python `>=3.10`. The local development version is pinned in
  `.python-version`.
- Dependencies and the virtual environment are managed with **uv**. Do
  not use `pip install` directly.
  - `uv sync`: install or update the environment.
  - `uv add <package>` or `uv add --dev <package>`: add a dependency.
  - `uv run kyb-brazil-pipeline`: run the command line entry point.
  - `uv run pytest`: run the tests (once pytest is added).
- Commit `uv.lock` together with any dependency change.

## Rules

These rules apply to every change, made by a human or by an agent.

### Line length

- No line may be longer than **79 columns**. This applies to code,
  configuration, SQL and documentation, including this file.

### Documentation to update with every change

- **`CHANGELOG.md`**: every change must be recorded there, with no
  exceptions. Add the entry under the `Unreleased` section, in the
  matching category (`Added`, `Changed`, `Fixed`, `Removed`).
- **`CONTRIBUTING.md`**: update it only when the change affects how
  people contribute, for example the setup steps, the workflow or the
  rules in this file.
- **`README.md`**: update it only when the change affects what the
  project does or how it is installed and used.
- **`schemas.yml`** (dbt): update it only when the change adds, removes
  or alters a dbt model, a column or a test.

### Writing documentation

- Every piece of documentation must be thorough and descriptive. The
  reader is a human developer who may not know the context, so clarity
  comes first.
- Avoid abbreviations and shortcuts. Write terms out in full. When an
  acronym is unavoidable, such as CNPJ, spell it out the first time it
  appears in each document.
- Explain why something is done, not only what is done.

### Testing before committing

- Every change must be made and tested locally before it is committed.
  At minimum, run the test suite and the affected command or pipeline
  step, and confirm that they succeed.
- Do not commit code that has not been run.

## Data conventions

- Store CNPJs normalized as 14 digits with no punctuation, as strings,
  so that leading zeros are kept. The root CNPJ (`cnpj_basico`) is the
  first 8 digits and identifies the company across all of its
  establishments.
- Never commit data files, credentials or `.env` files. `data/`,
  `*.csv`, `*.parquet` and similar paths are listed in `.gitignore`.
  Small test fixtures need an explicit `!` exception in `.gitignore`.
- The source data is public, but the partner data (QSA) contains
  personal information, such as names and partially masked CPFs
  (Cadastro de Pessoas Físicas). Do not log it and do not use it in
  examples or documentation.
