import re
import json
import os
import requests
from bs4 import BeautifulSoup

def extract_markdown_tables(text):
    """Extracts markdown-style tables from text."""
    tables = []
    # Markdown tables usually have at least two rows and a separator line |---|
    lines = text.split('\n')
    current_table = []
    
    for line in lines:
        if '|' in line:
            current_table.append(line.strip())
        else:
            if current_table:
                # Validate if it looks like a table (has separator)
                if any(re.match(r'\|?[\s:-|]+\|', l) for l in current_table):
                    tables.append("\n".join(current_table))
                current_table = []
    if current_table:
        if any(re.match(r'\|?[\s:-|]+\|', l) for l in current_table):
            tables.append("\n".join(current_table))
            
    return tables

def get_cells(line):
    """Helper to extract cells from a markdown pipe line."""
    line = line.strip()
    if line.startswith('|'):
        line = line[1:]
    if line.endswith('|'):
        line = line[:-1]
    return [c.strip() for c in line.split('|')]

def parse_markdown_table(table_str):
    """Parses a single markdown table string into a list of dicts."""
    lines = table_str.strip().split('\n')
    # Filter out separator lines (e.g., |---|---| or | :--- | :---: |)
    data_lines = [l for l in lines if not re.match(r'^\|?\s*[:\-|\s]+\s*\|?$', l) or not any(c in l for c in ':-')]
    # Actually, a better way is to skip the line if it only contains | - : and whitespace
    data_lines = []
    for l in lines:
        if re.match(r'^[|\s\-:]+$', l.strip()):
            continue
        data_lines.append(l)
    
    if not data_lines:
        return []
    
    headers = get_cells(data_lines[0])
    rows = []
    for line in data_lines[1:]:
        cells = get_cells(line)
        if len(cells) >= len(headers):
            row_dict = {}
            for i, header in enumerate(headers):
                if i < len(cells):
                    row_dict[header] = cells[i]
            rows.append(row_dict)
    return rows

def extract_html_tables(text):
    """Extracts HTML tables using BeautifulSoup."""
    soup = BeautifulSoup(text, 'html.parser')
    tables = []
    for html_table in soup.find_all('table'):
        headers = []
        thead = html_table.find('thead')
        if thead:
            headers = [th.get_text(strip=True) for th in thead.find_all('th')]
        
        if not headers:
            # Try first row if no thead
            first_row = html_table.find('tr')
            if first_row:
                headers = [td.get_text(strip=True) for td in first_row.find_all(['td', 'th'])]
        
        rows = []
        tbody = html_table.find('tbody') or html_table
        for tr in tbody.find_all('tr'):
            cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
            if cells == headers:
                continue
            if len(cells) >= len(headers) and headers:
                row_dict = {}
                for i, header in enumerate(headers):
                    if i < len(cells):
                        row_dict[header] = cells[i]
                rows.append(row_dict)
        
        if rows:
            tables.append(rows)
    return tables

def is_benchmark_table(rows):
    """Heuristic to check if a table contains benchmark data."""
    if not rows:
        return False
    
    benchmark_tokens = [
        'benchmark', 'score', 'acc', 'mmlu', 'gsm8k', 'human_eval', 'gpqa', 'ifeval',
        'hle', 'aime', 'math', 'code', 'arc', 'hellaswag', 'mmlu-pro', 'drop'
    ]
    
    # Check headers
    first_row = rows[0]
    keys_str = " ".join(first_row.keys()).lower()
    if any(token in keys_str for token in benchmark_tokens):
        return True
    
    # Check values in more rows (up to 10)
    for row in rows[:10]:
        values_str = " ".join(str(v) for v in row.values()).lower()
        if any(token in values_str for token in benchmark_tokens):
            return True
            
    return False

def process_readme(file_path, owner=None, official_name=None):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    all_table_data = []
    
    # Extract MD tables
    md_tables = extract_markdown_tables(content)
    for mt in md_tables:
        parsed = parse_markdown_table(mt)
        if is_benchmark_table(parsed):
            # Identify benchmark column
            bench_col = None
            if parsed:
                headers = list(parsed[0].keys())
                # Priority for benchmark column names
                for candidate in ["Benchmark (Metric)", "Benchmark", "benchmark", "Evaluation Source"]:
                    if candidate in headers:
                        bench_col = candidate
                        break
                if not bench_col and "" in headers:
                    bench_col = ""
            
            # Add metadata to each row if provided
            for row in parsed:
                if bench_col is not None:
                    row['__benchmark'] = row.get(bench_col, "")
                if owner:
                    row['__owner'] = owner
                if official_name:
                    row['__official_name'] = official_name
            all_table_data.append(parsed)
            
    # Extract HTML tables
    html_tables = extract_html_tables(content)
    for ht in html_tables:
        if is_benchmark_table(ht):
            # Identify benchmark column
            bench_col = None
            if ht:
                headers = list(ht[0].keys())
                for candidate in ["Benchmark (Metric)", "Benchmark", "benchmark", "Evaluation Source"]:
                    if candidate in headers:
                        bench_col = candidate
                        break
                if not bench_col and "" in headers:
                    bench_col = ""

            # Add metadata to each row if provided
            for row in ht:
                if bench_col is not None:
                    row['__benchmark'] = row.get(bench_col, "")
                if owner:
                    row['__owner'] = owner
                if official_name:
                    row['__official_name'] = official_name
            all_table_data.append(ht)
            
    return all_table_data

if __name__ == "__main__":
    # Mapping of filename to source metadata
    source_metadata = {
        "deepseek_readme.md": {"owner": "DeepSeek-V3", "name": "DeepSeek-V3"},
        "qwen_readme.md": {"owner": "Qwen3.5-397B-A17B", "name": "Qwen3.5-397B-A17B"},
        "glm5_readme.md": {"owner": "GLM-5", "name": "GLM-5"},
        "minimax_readme.md": {"owner": "MiniMax-M2.5", "name": "MiniMax-M2.5"},
        "kimi_k2.5_readme.md": {"owner": "Kimi-K2.5", "name": "Kimi-K2.5"},
        "qwen3.5_122b_a10b_readme.md": {"owner": "Qwen3.5-122B-A10B", "name": "Qwen3.5-122B-A10B"},
        "qwen3.5_35b_a3b_readme.md": {"owner": "Qwen3.5-35B-A3B", "name": "Qwen3.5-35B-A3B"}
    }
    
    results = {}
    
    # Process all .md files in the directory
    for filename in os.listdir('.'):
        if filename.endswith('.md') and filename != 'README.md': # Exclude project README if it exists
            print(f"Processing {filename}...")
            meta = source_metadata.get(filename, {"owner": None, "name": filename})
            owner = meta["owner"]
            display_name = meta["name"]
            
            tables = process_readme(filename, owner=owner, official_name=display_name)
            results[display_name] = tables
            print(f"Found {len(tables)} benchmark tables in {filename} (Official: {display_name}, Owner: {owner})")

    with open('benchmarks.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    print("Results saved to benchmarks.json")

    with open('benchmarks.js', 'w', encoding='utf-8') as f:
        f.write(f"var rawData = {json.dumps(results, indent=2)};")
    print("Results saved to benchmarks.js")

