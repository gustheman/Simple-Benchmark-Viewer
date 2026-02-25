---
description: How to update the LLM Benchmark Viewer with new models using Hugging Face links
---

Follow these steps to add a new model's benchmarks to the dashboard directly from a Hugging Face URL.

1.  **Obtain the Hugging Face Model URL** (e.g., `https://huggingface.co/Qwen/Qwen3.5-35B-A3B`).
2.  **Download and process the content**:
    // turbo
    ```bash
    # Step: download the README and save it to the project root
    # Step: run the extraction script
    python3 extract_benchmarks.py
    ```
3.  **Run the research script** to normalize names and update the dashboard data:
    // turbo
    ```bash
    python3 research_benchmarks.py
    ```
4.  **Check for normalization warnings** in the terminal output. If a benchmark name isn't recognized, add it to the `NORMALIZATION_MAP` in `research_benchmarks.py`.
5.  **Verify the changes in your browser** (the local `index.html`).
6.  **Commit and push the new data**:
    ```bash
    git add .
    git commit -m "Add benchmarks for [Model Name]"
    git push origin main
    ```
