# Skill: Updating Benchmarks

This skill provides the necessary steps to update the LLM Benchmark Universe dashboard with new model data.

## Description
The project uses a two-stage process to extract and normalize benchmark data from markdown files (usually model cards from Hugging Face).

## Instructions

### 1. Prepare Source Files
- Obtain the raw markdown content of the model card (README.md) from Hugging Face.
- Save it as a new `.md` file in the project root (e.g., `new_model_readme.md`).

### 2. Extract Raw Data
Run the extraction script. This script scans all `.md` files and generates `benchmarks.json`.
```bash
python3 extract_benchmarks.py
```
- **Verification**: Check `benchmarks.json` to ensure the new model's tables were found.

### 3. Normalize and Research
Run the research script to produce the final `benchmarks.js` used by the web interface.
```bash
python3 research_benchmarks.py
```
- **Handling New Benchmarks**: If the script logs "Unknown benchmark" for a desired metric, add a mapping to the `NORMALIZATION_MAP` dictionary in `research_benchmarks.py`.
- **Verification**: Open `index.html` locally and verify the new model appears and has correct data.

### 4. Deploy Updates
Commit the changes and push to GitHub.
```bash
git add .
git commit -m "Update benchmarks with [Model Name]"
git push origin main
```

## Troubleshooting
- **Missing Numbers**: Ensure the table in the source `.md` file is well-formatted. Extra characters like footnotes (*) are handled by the scripts, but broken pipe syntax (|) will cause extraction to fail.
- **Normalization Gaps**: The dashboard only shows benchmarks that are present in the `NORMALIZATION_MAP`.
