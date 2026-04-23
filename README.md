# Structured Generation With Small Models

Small experiment for extracting structured invoice data from images with a local OpenAI-compatible model server, then validating and evaluating the result with Pydantic schemas.

The project compares several OCR / structured-generation steps:

- `baseline`: plain chat completion followed by Pydantic parsing.
- `step_1`: JSON schema response format with the baseline schema.
- `step_2`: refined schema and prompt.
- `step_3`: adds `thinking` fields used as scratchpads.
- `step_4`: validates the extracted invoice with stricter Pydantic validators.
- `step_5`: uses `instructor` retries with the stricter schema.

## Requirements

- Python `3.12+`
- [`uv`](https://docs.astral.sh/uv/)
- A local OpenAI-compatible server, for example LM Studio, serving a vision-capable model.

## Install

Install dependencies from `pyproject.toml` and `uv.lock`:

```bash
uv sync
```

If you do not have `uv` installed yet:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Configure

The OCR runner expects two environment variables:

```bash
export LM_STUDIO_SERVER_URL="http://localhost:1234/v1"
export DATA_FOLDER="data"
```

`DATA_FOLDER` should contain invoice images as `.jpg` files. For evaluation, each image should have a matching `.json` file with the same stem:

```text
data/
  invoice_1.jpg
  invoice_1.json
  invoice_2.jpg
  invoice_2.json
```

## Run The CLI

The Typer app is defined in `main.py`. Show available commands with:

```bash
uv run python main.py --help
```

Run an extraction step:

```bash
uv run python main.py run-baseline
uv run python main.py run-step-1
uv run python main.py run-step-2
uv run python main.py run-step-3
uv run python main.py run-step-4
uv run python main.py run-step-5
```

Steps `2` through `5` can also evaluate the extracted invoices against the matching JSON ground truth:

```bash
uv run python main.py run-step-2 --eval
uv run python main.py run-step-3 --eval
uv run python main.py run-step-4 --eval
uv run python main.py run-step-5 --eval
```

`step_5` supports retry and debug options:

```bash
uv run python main.py run-step-5 --n-retries 5 --debug
```

## Project Layout

```text
main.py          Typer CLI entrypoint
ocr.py           OCR runners and extraction strategies
evaluate.py      Evaluation helpers and evaluator classes
schemas/         Pydantic invoice schemas for each step
prompts/         Prompts and JSON schema response formats
data/            Example invoice images and expected JSON files
```

## Development Checks

Compile the main modules:

```bash
uv run python -m py_compile main.py ocr.py evaluate.py
```

Run the CLI help as a quick smoke test:

```bash
uv run python main.py --help
```
