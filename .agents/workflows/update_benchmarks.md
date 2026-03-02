---
description: /update_benchmarks [Hugging Face URL] - Add a new model from a Hugging Face link
---

# Update Benchmarks from Hugging Face

// turbo-all

This workflow adds a new model's benchmark data to the dashboard from a Hugging Face model page.

**Before starting**, read the skill instructions at `.agents/skills/extract_hf_benchmarks/SKILL.md` and follow them exactly.

## Steps

1. Parse the Hugging Face URL provided by the user to extract org and model name
2. Fetch the raw README.md from `https://huggingface.co/{org}/{model}/resolve/main/README.md`
   - If `read_url_content` fails or truncates the content, fall back to `curl -L` to download
3. Save the README to the project root as `{model_slug}_readme.md`
4. Ask the user for the display name (or infer from the model name)
5. Add source metadata entry to `extract_benchmarks.py`
6. Run the extraction pipeline:
```bash
source venv/bin/activate && python extract_benchmarks.py && python research_benchmarks.py
```
7. Verify the model appears in `benchmarks.json`
8. Commit and push:
```bash
git add -A && git commit -m "Add {model_name} benchmarks" && git push
```
