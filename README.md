# LLM Benchmark Universe 🌌

[**Live Dashboard**](https://gustheman.github.io/Simple-Benchmark-Viewer/)

A unified dashboard for comparing frontier AI models across language and vision benchmarks. This project extracts, normalizes, and visualizes benchmark data from official Hugging Face model cards to provide a clear, side-by-side comparison of model capabilities.

## 🚀 Features

- **Unified Comparison**: View and filter benchmarks across multiple models in a single table.
- **Source Transparency**: Access the raw benchmark tables extracted directly from model readmes.
- **Comprehensive Data**: Includes deep extraction of knowledge, reasoning, coding, agentic, and multimodal benchmarks.
- **Fast & Static**: Built with Vanilla HTML/CSS/JS for maximum speed and easy deployment.

## 📦 Project Structure

- `index.html`: The main dashboard interface.
- `style.css`: Modern, dark-themed responsive UI.
- `benchmarks.js`: The central data store (generated from extraction scripts).
- `extract_benchmarks.py`: Scrapes and parses markdown/HTML tables from local readme files.
- `research_benchmarks.py`: Normalizes benchmark names and adds metadata (descriptions, URLs).

## 🛠️ How to Update Data

You can manually update the benchmarks following these steps, or use the automated **Skills** and **Workflows** provided (see below).

1.  **Add/Update Readmes**: Place the Hugging Face model card content in `.md` files (e.g., `qwen_readme.md`).
2.  **Extract Data**:
    ```bash
    python3 extract_benchmarks.py
    ```
3.  **Normalize & Generate JS**:
    ```bash
    python3 research_benchmarks.py
    ```
4.  **Open Dashboard**: Open `index.html` in any browser.

### 🤖 Agent Automation
This repository includes a pre-defined **Skill** and **Workflow** for AI agents:
- **Skill**: `.agent/skills/update_benchmarks/SKILL.md`
- **Workflow**: `.agent/workflows/update_benchmarks.md`

## 📄 License

MIT
