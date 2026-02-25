---
description: /update_benchmarks [Hugging Face URL] - Add a new model from a Hugging Face link
---

Follow these steps to add a new model's benchmarks to the dashboard directly from a Hugging Face URL.

1.  **Extract the raw README content** from the provided `{{URL}}`.
2.  **Save the content** as a `.md` file in the root directory (e.g., based on the model name).
3.  **Process and Extract**:
    // turbo
    ```bash
    python3 extract_benchmarks.py
    ```
4.  **Normalize and Research**:
    // turbo
    ```bash
    python3 research_benchmarks.py
    ```
5.  **Verify the results** in the local `index.html`.
6.  **Commit and push**:
    ```bash
    git add .
    git commit -m "Add benchmarks for model from {{URL}}"
    git push origin main
    ```
