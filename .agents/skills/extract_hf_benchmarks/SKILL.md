---
name: Extract HF Benchmarks
description: Extract benchmark scores from a Hugging Face model page by fetching its raw README.md and processing it through the project's Python extraction pipeline.
---

# Extract Benchmarks from Hugging Face Model Pages

This skill describes how to add a new model's benchmark data to the LLM Benchmark Universe dashboard from a Hugging Face model page URL.

## Overview

Every Hugging Face model page has a README.md that typically contains benchmark tables (in markdown or HTML format). This skill treats that README as the source of truth for benchmark extraction.

## Prerequisites

- Python virtual environment at `venv/` in the project root (activate with `source venv/bin/activate`)
- Dependencies: `beautifulsoup4`, `requests` (already installed in venv)

## Step-by-Step Procedure

### 1. Parse the Hugging Face URL

Given a URL like `https://huggingface.co/deepseek-ai/DeepSeek-V3`, extract:
- **org**: `deepseek-ai`
- **model**: `DeepSeek-V3`

The URL may also include trailing paths like `/tree/main` — strip those.

### 2. Fetch the Raw README.md

Construct the raw README URL:
```
https://huggingface.co/{org}/{model}/resolve/main/README.md
```

Use `read_url_content` to fetch this URL. The content will be the model's README in markdown format.

> [!IMPORTANT]
> Use `/resolve/main/README.md` (not `/raw/main/`). The `resolve` endpoint returns the actual file content.

### 3. Save the README Locally

Save the fetched content to the project root as:
```
{model_slug}_readme.md
```

Where `model_slug` is a lowercase, underscore-separated version of the model name (e.g., `DeepSeek-V3` → `deepseek_v3`).

> [!TIP]
> Check existing files for naming conventions: `deepseek_readme.md`, `qwen_readme.md`, `glm5_readme.md`, etc.

### 4. Determine the Model Display Name

Ask the user what the model should be called in the dashboard (e.g., "DeepSeek-V3", "Qwen3.5-397B-A17B"). This becomes both the `owner` and `name` in the source metadata.

### 5. Update `extract_benchmarks.py`

Add a new entry to the `source_metadata` dictionary in the `if __name__ == "__main__":` block:

```python
source_metadata = {
    # ... existing entries ...
    "{model_slug}_readme.md": {"owner": "{DisplayName}", "name": "{DisplayName}"},
}
```

### 6. Run the Extraction Pipeline

Execute both scripts in sequence from the project root:

```bash
cd /Users/lgusm/projects/benchmarks_comparison
source venv/bin/activate
python extract_benchmarks.py
python research_benchmarks.py
```

**`extract_benchmarks.py`** will:
- Read all `*_readme.md` files
- Parse markdown and HTML tables
- Identify benchmark tables via heuristics
- Output `benchmarks.json` and `benchmarks.js`

**`research_benchmarks.py`** will:
- Normalize benchmark names (e.g., "MMLU (Acc.)" → "MMLU")
- Add metadata (URLs, descriptions) for known benchmarks
- Update `benchmarks.json` and `benchmarks.js` with normalized data

### 7. Verify the Results

After running the scripts:

1. Check the terminal output for `Found X benchmark tables in {filename}`
2. Verify the model appears in `benchmarks.json` by searching for the display name
3. Optionally open `index.html` in a browser to see the dashboard

> [!WARNING]
> If 0 benchmark tables are found, the README may use a non-standard table format. Inspect the saved README manually and check if tables are embedded in HTML `<details>` tags or use unusual formatting.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| 0 tables found | Check if README uses `<details>` tags hiding tables; expand and re-save |
| Benchmark names look wrong | Add entries to `NORMALIZATION_MAP` in `research_benchmarks.py` |
| Model not showing on dashboard | Verify `benchmarks.js` contains the model data; hard-refresh the browser |
| `read_url_content` returns truncated content | Use `curl` via `run_command` to download the file instead |

## Fallback: Direct Download via curl

If `read_url_content` doesn't capture the full README, use:

```bash
curl -L "https://huggingface.co/{org}/{model}/resolve/main/README.md" -o /Users/lgusm/projects/benchmarks_comparison/{model_slug}_readme.md
```
