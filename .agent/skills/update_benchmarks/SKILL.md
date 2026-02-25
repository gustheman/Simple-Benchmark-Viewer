# Skill: Updating Benchmarks (via HF Links)

This skill provides the necessary steps to update the LLM Benchmark Universe dashboard using Hugging Face model links as a parameter.

## Description
The project can automatically download data from Hugging Face URLs provided via the `/update_benchmarks [URL]` command, extract benchmark values, and normalize them for the web dashboard.

## Instructions

### 1. Trigger the workflow
Use the slash command with the Hugging Face URL:
```bash
/update_benchmarks https://huggingface.co/vendor/model-name
```

### 2. Automated Extraction
Once triggered, the agent will:
1.  **Extract raw README content** from the provided URL.
2.  **Save the content** as a `.md` file in the root directory.
3.  **Run the extraction script** to update `benchmarks.json`:
    ```bash
    python3 extract_benchmarks.py
    ```

### 3. Normalize and Research
The agent will then run the research script to canonicalize names and generate `benchmarks.js`:
```bash
python3 research_benchmarks.py
```
- **Fuzzy Matching**: If the script identifies a new benchmark, the agent may update the `NORMALIZATION_MAP` in `research_benchmarks.py` if manual mapping is required.

### 4. Deploy Updates
Finally, the agent will commit the changes and push to GitHub:
```bash
git add .
git commit -m "Update benchmarks for model from [URL]"
git push origin main
```
The site will be live at `https://gustheman.github.io/Simple-Benchmark-Viewer/` within minutes.
