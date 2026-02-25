# Skill: Updating Benchmarks (via HF Links)

This skill provides the necessary steps to update the LLM Benchmark Universe dashboard using Hugging Face model links.

## Description
The project can automatically download data from Hugging Face URLs, extract benchmark values, and normalize them for the web dashboard.

## Instructions

### 1. Identify the Model URL
- Get the URL of the Hugging Face model (e.g., `https://huggingface.co/vendor/model-name`).

### 2. Download and Extract
Download the README content (using `read_url_content` or a similar tool) and save it as a `.md` file in the root directory. Then run the extraction script:
```bash
python3 extract_benchmarks.py
```

### 3. Normalize and Research
Run the research script to canonicalize names and generate `benchmarks.js`:
```bash
python3 research_benchmarks.py
```
- **Fuzzy Matching**: If the script identifies a new benchmark, update the `NORMALIZATION_MAP` in `research_benchmarks.py` if manual mapping is required.

### 4. Deploy Updates
Commit the changes and push to GitHub:
```bash
git add .
git commit -m "Update benchmarks with [Model Name]"
git push origin main
```
The site will be live at `https://gustheman.github.io/Simple-Benchmark-Viewer/` within minutes.
