---
description: How to update the LLM Benchmark Viewer with new models
---

Follow these steps to add a new model's benchmarks to the dashboard.

1.  **Download the model README** from Hugging Face and save it to the root of the project with a descriptive name like `new_model_readme.md`.
2.  **Ensure you have a Python environment set up** with `requests` and `beautifulsoup4` installed.
3.  **Run the extraction script** to update `benchmarks.json`:
    // turbo
    ```bash
    python3 extract_benchmarks.py
    ```
4.  **Verify the new model's data** appears correctly in the generated `benchmarks.json` file.
5.  **Run the research script** to normalize names and update the dashboard data:
    // turbo
    ```bash
    python3 research_benchmarks.py
    ```
6.  **Check for normalization warnings** in the terminal output. If a benchmark name isn't recognized, you may need to add it to the `NORMALIZATION_MAP` in `research_benchmarks.py`.
7.  **Verify the changes in your browser** by opening `index.html`.
8.  **Commit and push the new data**:
    ```bash
    git add .
    git commit -m "Add benchmarks for [Model Name]"
    git push origin main
    ```
