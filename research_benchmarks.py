import json
import os
import re

# Pre-defined mapping for common benchmarks to save search time and ensure accuracy
COMMON_BENCHMARKS = {
    "MMLU (Acc.)": {
        "url": "https://arxiv.org/abs/2009.03300",
        "desc": "Massive Multitask Language Understanding: A benchmark covering 57 subjects across STEM, the humanities, the social sciences, and more."
    },
    "MMLU": {
        "url": "https://arxiv.org/abs/2009.03300",
        "desc": "Massive Multitask Language Understanding: A benchmark covering 57 subjects across STEM, the humanities, the social sciences, and more."
    },
    "HumanEval (Pass@1)": {
        "url": "https://github.com/openai/human-eval",
        "desc": "Released by OpenAI, evaluates the coding ability of models on 164 hand-written programming problems."
    },
    "HumanEval": {
        "url": "https://github.com/openai/human-eval",
        "desc": "Released by OpenAI, evaluates the coding ability of models on 164 hand-written programming problems."
    },
    "GSM8K (EM)": {
        "url": "https://arxiv.org/abs/2110.14168",
        "desc": "Grade School Math 8K: A dataset of 8.5K high quality grade school math word problems requiring multi-step reasoning."
    },
    "GSM8K": {
        "url": "https://arxiv.org/abs/2110.14168",
        "desc": "Grade School Math 8K: A dataset of 8.5K high quality grade school math word problems requiring multi-step reasoning."
    },
    "MATH (EM)": {
        "url": "https://arxiv.org/abs/2103.03874",
        "desc": "A new dataset of 12,500 challenging competition mathematics problems."
    },
    "MATH": {
        "url": "https://arxiv.org/abs/2103.03874",
        "desc": "A new dataset of 12,500 challenging competition mathematics problems."
    },
    "MBPP (Pass@1)": {
        "url": "https://arxiv.org/abs/2108.07732",
        "desc": "Mostly Basic Programming Problems: Contains 974 entry-level Python programming problems."
    },
    "GPQA": {
        "url": "https://arxiv.org/abs/2311.12022",
        "desc": "A graduate-level Google-proof Q&A benchmark which is very challenging even for domain experts."
    },
    "GPQA-Diamond": {
        "url": "https://arxiv.org/abs/2311.12022",
        "desc": "The most difficult subset of GPQA, containing questions that experts found particularly challenging."
    },
    "IFEval": {
        "url": "https://arxiv.org/abs/2311.07911",
        "desc": "Instruction Following Evaluation: Focuses on objective constraints (e.g., 'no more than 400 words', 'use specific format')."
    },
    "ARC-Challenge (Acc.)": {
        "url": "https://arxiv.org/abs/1803.05457",
        "desc": "AI2 Reasoning Challenge: A dataset of 7,787 genuine school-level, multiple-choice science questions."
    },
    "HellaSwag (Acc.)": {
        "url": "https://arxiv.org/abs/1905.07830",
        "desc": "A challenge for commonsense reasoning, where models must predict the most likely ending of a scenario."
    },
    "PIQA (Acc.)": {
        "url": "https://arxiv.org/abs/1911.11641",
        "desc": "Physical Interaction QA: A benchmark for testing models' understanding of physical commonsense."
    },
    "WinoGrande (Acc.)": {
        "url": "https://arxiv.org/abs/1907.10641",
        "desc": "A large-scale dataset for commonsense reasoning, designed to be more adversarial than the original Winograd Schema Challenge."
    },
    "RACE-High (Acc.)": {
        "url": "https://arxiv.org/abs/1704.04683",
        "desc": "ReAding Comprehension from Examinations: Dataset collected from English exams for middle and high school students in China."
    },
    "DROP (F1)": {
        "url": "https://arxiv.org/abs/1903.00164",
        "desc": "Discrete Reasoning Over Paragraphs: Requires models to perform numerical reasoning over text."
    },
    "C-Eval": {
        "url": "https://arxiv.org/abs/2305.08322",
        "desc": "A comprehensive Chinese evaluation suite for foundation models."
    },
    "CMMLU (Acc.)": {
        "url": "https://arxiv.org/abs/2306.09212",
        "desc": "A comprehensive Chinese multi-genre benchmark for evaluating LLMs."
    },
    "MGSM (EM)": {
        "url": "https://arxiv.org/abs/2210.03057",
        "desc": "Multilingual Grade School Math: A multilingual version of GSM8K."
    },
    "MMLU-Pro": {
        "url": "https://arxiv.org/abs/2406.01574",
        "desc": "An enhanced version of MMLU with more difficult questions and fewer shortcuts."
    },
    "MMMU": {
        "url": "https://arxiv.org/abs/2311.16212",
        "desc": "Massive Multi-discipline Multimodal Understanding: Evaluation on diverse tasks requiring both visual and textual reasoning."
    },
    "MathVista (mini)": {
        "url": "https://arxiv.org/abs/2310.02255",
        "desc": "A benchmark to combine visual and mathematical reasoning."
    },
    "VideoMME": {
        "url": "https://arxiv.org/abs/2405.21075",
        "desc": "A large-scale multi-modal benchmark for video understanding."
    },
    "BBH (EM)": {
        "url": "https://arxiv.org/abs/2210.09261",
        "desc": "BIG-Bench Hard: A subset of BIG-bench tasks where models previously performed poorly."
    },
    "Pile-test (BPB)": {
        "url": "https://arxiv.org/abs/2101.00027",
        "desc": "Bits Per Byte evaluation on the Pile dataset, measuring language modeling efficiency."
    },
    "SWE-bench Verified": {
        "url": "https://www.swebench.com/",
        "desc": "Evaluates models on their ability to fix real-world GitHub issues. 'Verified' uses a human-vetted subset."
    },
    "LiveCodeBench": {
        "url": "https://livecodebench.github.io/",
        "desc": "A contamination-free benchmark for code generation by continuously collecting new problems."
    },
    "AGIEval": {
        "url": "https://github.com/ruixiangcui/AGIEval",
        "desc": "A human-centric benchmark for evaluating foundation models in the context of human-level exams."
    },
    "BFCL": {
        "url": "https://gorilla.cs.berkeley.edu/leaderboard.html",
        "desc": "Berkeley Function Calling Leaderboard: Evaluates the function-calling capabilities of LLMs."
    },
    "AIME 2025": {
        "url": "https://www.maa.org/math-competitions/aime",
        "desc": "American Invitational Mathematics Examination: A high-school level competition math benchmark."
    },
    "HLE": {
        "url": "https://humaneval.github.io/hle",
        "desc": "Humanity's Last Exam: A benchmark designed to be extremely difficult for current AI models."
    },
    "WideSearch": {
        "url": "https://arxiv.org/abs/2508.07999",
        "desc": "Benchmarking Agentic Broad Info-Seeking: Evaluates agents on finding entangled info on the internet."
    },
    "Codeforces": {
        "url": "https://arxiv.org/abs/2501.01257",
        "desc": "CodeElo: Evaluates competition-level code generation using problems from Codeforces with human-comparable Elo ratings."
    },
    "OJBench": {
        "url": "https://github.com/He-Ren/OJBench",
        "desc": "A Competition Level Code Benchmark for LLMs with 232 programming competition problems."
    },
    "ZeroBench": {
        "url": "https://arxiv.org/abs/2502.09696",
        "desc": "An Impossible Visual Benchmark for Contemporary Large Multimodal Models."
    },
    "MathVision": {
        "url": "https://mathllm.github.io/mathvision/",
        "desc": "A dataset of 3,040 math problems with visual contexts from real math competitions."
    },
    "OmniDocBench 1.5": {
        "url": "https://github.com/opendatalab/OmniDocBench",
        "desc": "A comprehensive benchmark for document understanding and parsing."
    },
    "Terminal Bench 2.0": {
        "url": "https://www.tbench.ai/",
        "desc": "Evaluates AI agents' ability to operate a computer via terminal for real-world technical tasks."
    },
    "SWE-bench Pro": {
        "url": "https://github.com/scaleapi/SWE-bench_Pro-os",
        "desc": "Evaluates LLMs on long-horizon software engineering tasks across professional repositories."
    },
    "IMO-AnswerBench": {
        "url": "https://imobench.github.io/",
        "desc": "Part of IMO-Bench, evaluating LLMs on International Mathematical Olympiad level problems."
    },
    "DynaMath": {
        "url": "https://github.com/DynaMath/DynaMath",
        "desc": "A dynamic visual math benchmark evaluating the robustness of mathematical reasoning in VLMs."
    },
    "CharXiv": {
        "url": "https://charxiv.github.io",
        "desc": "A benchmark for character-based visual reasoning in multimodal models."
    },
    "OSWorld-Verified": {
        "url": "https://github.com/xlang-ai/OSWorld",
        "desc": "A scalable real computer environment for evaluating multimodal agents across operating systems."
    },
    "MMStar": {
        "url": "https://github.com/mmstar-benchmark/mmstar",
        "desc": "Evaluates whether Large Vision-Language Models are truly relying on visual capabilities."
    },
    "RealWorldQA": {
        "url": "https://huggingface.co/datasets/xai-org/RealworldQA",
        "desc": "Designed by xAI to evaluate real-world spatial understanding in multimodal models."
    },
    "MLVU": {
        "url": "https://github.com/JUNJIE99/MLVU",
        "desc": "Multi-task Long Video Understanding: Benchmarking models on diverse long-video tasks."
    },
    "OCRBench": {
        "url": "https://github.com/Yuliang-Liu/MultimodalOCR",
        "desc": "A comprehensive evaluation benchmark for Optical Character Recognition in multimodal models."
    },
    "FullStackBench": {
        "url": "https://github.com/bytedance/FullStackBench",
        "desc": "Evaluating LLMs as full-stack coders across 16 programming languages and 3,000 samples."
    },
    "VlmsAreBlind": {
        "url": "https://vlmsareblind.github.io",
        "desc": "BlindTest: Evaluates whether Vision-Language Models are \"blind\" to certain visual features."
    },
    "Seal-0": {
        "url": "https://arxiv.org/abs/2506.01062",
        "desc": "Part of SealQA, evaluating reasoning under noisy, conflicting, and ambiguous search results."
    },
    "VITA-Bench": {
        "url": "https://vitabench.github.io",
        "desc": "Benchmarking LLM agents with versatile interactive tasks in real-world applications."
    },
    "DeepPlanning": {
        "url": "https://arxiv.org/abs/2601.18137",
        "desc": "Benchmarking long-horizon agentic planning with verifiable constraints."
    },
    "TAU2-Bench": {
        "url": "https://github.com/sierra-research/tau2-bench",
        "desc": "Evaluating conversational agents in a dual-control environment."
    },
    "BrowseComp": {
        "url": "https://arxiv.org/abs/2504.12516",
        "desc": "OpenAI's benchmark for browsing agents to locate difficult-to-find information."
    },
    "BrowseComp-Zh": {
        "url": "https://arxiv.org/abs/2504.19314",
        "desc": "High-difficulty benchmark for evaluating LLM agents on the Chinese web."
    },
    "BabyVision": {
        "url": "https://github.com/UniPat-AI/BabyVision",
        "desc": "Visual Reasoning Beyond Language: Evaluates early visual development concepts in models."
    },
    "PolyMATH": {
        "url": "https://arxiv.org/abs/2504.18428",
        "desc": "Evaluating Mathematical Reasoning in Multilingual Contexts across 18 languages."
    },
    "WMT24++": {
        "url": "https://huggingface.co/datasets/google/wmt24pp",
        "desc": "Expanding the language coverage of WMT24 to 55 languages and dialects."
    },
    "WinoGrande (Acc.)": {
        "url": "https://arxiv.org/abs/1907.10641",
        "desc": "A large-scale dataset for commonsense reasoning, designed to be more adversarial than the original Winograd Schema Challenge."
    },
    "ARC-Easy (Acc.)": {
        "url": "https://arxiv.org/abs/1803.05457",
        "desc": "AI2 Reasoning Challenge: The easier subset of school-level multiple-choice science questions."
    },
    "TriviaQA (EM)": {
        "url": "https://arxiv.org/abs/1705.03551",
        "desc": "A large scale reading comprehension dataset which includes over 650K question-answer-evidence triples."
    }
}

NORMALIZATION_MAP = {
    "MMLU (Acc.)": "MMLU",
    "MMLU-Pro (Acc.)": "MMLU-Pro",
    "HumanEval (Pass@1)": "HumanEval",
    "MBPP (Pass@1)": "MBPP",
    "GSM8K (EM)": "GSM8K",
    "MATH (EM)": "MATH",
    "MGSM (EM)": "MGSM",
    "GPQA-D": "GPQA-Diamond",
    "AIME25": "AIME 2025",
    "AIME26": "AIME 2026",
    "AIME 2026 I": "AIME 2026",
    "AIME 2026 II": "AIME 2026",
    "C-Eval (Acc.)": "C-Eval",
    "CMMLU (Acc.)": "CMMLU",
    "HMMT Feb 25": "HMMT 2025 (Feb)",
    "HMMT Nov 25": "HMMT 2025 (Nov)",
    "HMMT Nov. 2025": "HMMT 2025 (Nov)",
    "HMMT Nov 25": "HMMT 2025 (Nov)",
    "Longbench v2": "LongBench v2",
    "Longbench v1": "LongBench v1",
    "Mathvista(mini)": "MathVista (mini)",
    "Mathvista (mini)": "MathVista (mini)",
    "Mathvision": "MathVision",
    "OmniDocBench1.5": "OmniDocBench 1.5",
    "Terminal Bench 2": "Terminal Bench 2.0",
    "Terminal-Bench 2.0 (Terminus 2)": "Terminal Bench 2.0",
    "Terminal-Bench 2.0 (Claude Code)": "Terminal Bench 2.0",
    "SWE-bench Verified": "SWE-bench Verified",
    "SWE-Bench Verified": "SWE-bench Verified",
    "SWE-bench Multilingual": "SWE-bench Multilingual",
    "SWE-Bench Multilingual": "SWE-bench Multilingual",
    "SWE-Bench Pro": "SWE-bench Pro",
    "IFEval": "IFEval",
    "MAXIFE": "IFEval", # MAXIFE is often IFEval with specific settings or variant
    "MMMLU": "MMLU",
    "AGIEval (Acc.)": "AGIEval",
    "ARC-Challenge (Acc.)": "ARC-Challenge",
    "ARC-Easy (Acc.)": "ARC-Easy",
    "HellaSwag (Acc.)": "HellaSwag",
    "PIQA (Acc.)": "PIQA",
    "WinoGrande (Acc.)": "WinoGrande",
    "C3 (Acc.)": "C3",
    "CCPM (Acc.)": "CCPM",
    "RACE-High (Acc.)": "RACE-High",
    "RACE-Middle (Acc.)": "RACE-Middle",
    "TriviaQA (EM)": "TriviaQA",
    "NaturalQuestions (EM)": "Natural Questions",
    "MMMLU-non-English (Acc.)": "MMMLU (non-English)",
    "BrowseComp-zh": "BrowseComp-Zh",
    "LiveCodeBench (v6)": "LiveCodeBench",
    "LiveCodeBench v6": "LiveCodeBench",
    "LiveCodeBench-Base (Pass@1)": "LiveCodeBench",
    "HLE w/ tool": "HLE (w/ Tools)",
    "HLE (w/ Tools)": "HLE (w/ Tools)",
    "HLE w/o tools": "HLE",
    "IMOAnswerBench": "IMO-AnswerBench",
    "Mathvista(mini)": "MathVista (mini)",
    "Mathvista (mini)": "MathVista (mini)",
    "Mathvision": "MathVision",
    "ZeroBench": "ZeroBench",
    "ZEROBench": "ZeroBench",
    "ZEROBench_sub": "ZeroBench",
    "DynaMath": "DynaMath",
    "DynaMath (Acc.)": "DynaMath",
    "CharXiv (RQ)": "CharXiv",
    "CharXiv(RQ)": "CharXiv",
    "ScreenSpot Pro": "ScreenSpot Pro",
    "OSWorld-Verified": "OSWorld-Verified",
    "HLE w/ CoT": "HLE",
    "MultiChallenge": "Multi-Challenge",
    "AA-LCR": "AA-LCR",
    "VideoMME(w sub.)": "VideoMME",
    "Codeforces": "Codeforces",
    "CodeForces": "Codeforces",
    "OJBench": "OJBench",
    "ZeroBench": "ZeroBench",
    "ZEROBench": "ZeroBench",
    "ZEROBench_sub": "ZeroBench",
    "Mathvista(mini)": "MathVista (mini)",
    "VlmsAreBlind": "VlmsAreBlind",
    "WideSearch": "WideSearch",
    "Seal-0": "Seal-0",
    "VITA-Bench": "VITA-Bench",
    "DeepPlanning": "DeepPlanning",
    "TAU2-Bench": "TAU2-Bench",
    "Browsecomp": "BrowseComp",
    "Browsecomp-zh": "BrowseComp-Zh",
    "BrowseComp-zh": "BrowseComp-Zh",
    "BabyVision": "BabyVision",
    "FullStackBench en": "FullStackBench (EN)",
    "FullStackBench zh": "FullStackBench (ZH)",
    "Global PIQA": "Global PIQA",
    "PolyMATH": "PolyMATH",
    "WMT24++": "WMT24++",
    "MMLU-ProX": "MMLU-ProX",
    "NOVA-63": "NOVA-63",
    "MMStar": "MMStar",
    "RealWorldQA": "RealWorldQA",
    "MMLongBench-Doc": "MMLongBench-Doc",
    "CC-OCR": "CC-OCR",
    "AI2D_TEST": "AI2D",
    "ERQA": "ERQA",
    "CountBench": "CountBench",
    "RefCOCO(avg)": "RefCOCO",
    "ODInW13": "ODInW13",
    "EmbSpatialBench": "EmbSpatialBench",
    "RefSpatialBench": "RefSpatialBench",
    "Hypersim": "Hypersim",
    "SUNRGBD": "SUNRGBD",
    "Nuscene": "NuScenes",
    "VideoMME(w/o sub.)": "VideoMME",
    "VideoMMMU": "VideoMMMU",
    "MLVU": "MLVU",
    "MVBench": "MVBench",
    "LVBench": "LVBench",
    "MMVU": "MMVU",
    "AndroidWorld": "AndroidWorld",
    "TIR-Bench": "TIR-Bench",
    "V*": "V*",
    "SLAKE": "SLAKE",
    "PMC-VQA": "PMC-VQA",
    "MedXpertQA-MM": "MedXpertQA-MM",
}

def normalize_name(name):
    if not name: return name
    
    # Exact match in map
    if name in NORMALIZATION_MAP:
        return NORMALIZATION_MAP[name]
    
    # CASE insensitive and whitespace cleanup
    clean_name = name.strip()
    for variant, canonical in NORMALIZATION_MAP.items():
        if clean_name.lower() == variant.lower():
            return canonical
            
    # Automated cleaning for common suffixes if not in map
    clean_name = re.sub(r'\s*\((Acc\.|Acc|Pass@\d+|EM|F1|Average|Avg|mini|mini-set|val)\)', '', clean_name, flags=re.IGNORECASE)
    clean_name = re.sub(r'\s+v\d+(\.\d+)*$', '', clean_name, flags=re.IGNORECASE) # strip v1.1 etc if not in map
    
    # Re-check map after automated cleaning
    if clean_name in NORMALIZATION_MAP:
        return NORMALIZATION_MAP[clean_name]

    return clean_name

def research_benchmarks():
    if not os.path.exists('benchmarks.json'):
        print("benchmarks.json not found")
        return

    with open('benchmarks.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Collect unique benchmarks
    benchmarks = set()
    for source in data:
        if source == "__benchmark_metadata": continue
        for table in data[source]:
            for row in table:
                b_name = row.get('__benchmark')
                if b_name:
                    benchmarks.add(b_name)

    metadata = data.get('__benchmark_metadata', {})
    normalized_metadata = {}

    for b in sorted(list(benchmarks)):
        # Normalize the benchmark name first
        norm_b = normalize_name(b)
        
        # Check if we already have info for this canonical name
        if norm_b in normalized_metadata and normalized_metadata[norm_b].get('url'):
            continue

        # Check pre-defined and fuzzy matches for the canonical name
        info = {"url": None, "desc": None}
        if norm_b in COMMON_BENCHMARKS:
            info = COMMON_BENCHMARKS[norm_b]
        else:
            base_name = norm_b.split(' (')[0].split(' - ')[0].split(' v')[0].strip()
            if base_name in COMMON_BENCHMARKS:
                info = COMMON_BENCHMARKS[base_name]
            elif norm_b in metadata:
                info = metadata[norm_b]
            elif b in metadata:
                info = metadata[b]
        
        normalized_metadata[norm_b] = info

    data['__benchmark_metadata'] = normalized_metadata

    # Apply normalization to all records
    for source in data:
        if source == "__benchmark_metadata": continue
        for table in data[source]:
            for row in table:
                if "__benchmark" in row:
                    row["__benchmark"] = normalize_name(row["__benchmark"])

    with open('benchmarks.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"Updated benchmarks.json with metadata for {len(metadata)} benchmarks")

    with open('benchmarks.js', 'w', encoding='utf-8') as f:
        f.write(f"var rawData = {json.dumps(data, indent=2)};")
    print(f"Updated benchmarks.js with metadata for {len(metadata)} benchmarks")

if __name__ == "__main__":
    research_benchmarks()
