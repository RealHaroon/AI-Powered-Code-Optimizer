from groq import Groq
import difflib
import re
import json

# ── Prompts ───────────────────────────────────────────────────────────────────

SYSTEM_OPTIMIZE = """You are an expert code optimizer and software engineer.
When given code, you must:
1. Fix performance issues (e.g., O(n²) → O(n), unnecessary loops)
2. Fix security vulnerabilities (SQL injection, eval, hardcoded secrets)
3. Improve readability (naming, type hints, docstrings)
4. Apply language best practices (Pythonic code, modern JS, etc.)
5. Remove dead/redundant code

Return ONLY the optimized code with no explanation, no markdown fences.
"""

SYSTEM_ANALYZE = """You are a senior code reviewer. Analyze this code and return a JSON array of issues.
Each issue must have:
- "title": short issue name
- "severity": "error" | "warning" | "info"
- "line": estimated line number (integer)
- "description": one sentence explanation
- "fix": one sentence fix suggestion

Return ONLY a valid JSON array. No markdown, no extra text.
Example: [{"title":"SQL Injection","severity":"error","line":5,"description":"...","fix":"..."}]
"""

SYSTEM_CHAT = """You are an expert code assistant. Answer the developer's question clearly and concisely.
If relevant, reference the code context provided.
Use markdown for code blocks if needed."""

MODE_INSTRUCTIONS = {
    "all":         "Apply ALL optimizations: performance, security, readability, memory.",
    "performance": "Focus ONLY on performance: time/space complexity, algorithm efficiency.",
    "readability": "Focus ONLY on readability: naming, structure, comments, type hints.",
    "security":    "Focus ONLY on security: injection, eval, secrets, input validation.",
    "memory":      "Focus ONLY on memory: avoid copies, use generators, reduce allocations.",
}

MODEL = "llama-3.3-70b-versatile"  # Free, fast, excellent for code

# ── Helpers ───────────────────────────────────────────────────────────────────

def _client(api_key: str) -> Groq:
    return Groq(api_key=api_key)

def _clean_fences(text: str) -> str:
    text = re.sub(r'^```[\w]*\n?', '', text.strip())
    text = re.sub(r'\n?```$', '', text)
    return text.strip()

def _chat(api_key: str, system: str, user: str) -> str:
    client = _client(api_key)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()

# ── Core Functions ────────────────────────────────────────────────────────────

def optimize_code(code: str, language: str, mode: str, api_key: str) -> dict:
    user_prompt = (
        f"Language: {language}\n"
        f"Optimization mode: {MODE_INSTRUCTIONS.get(mode, MODE_INSTRUCTIONS['all'])}\n\n"
        f"Code to optimize:\n{code}"
    )
    optimized = _clean_fences(_chat(api_key, SYSTEM_OPTIMIZE, user_prompt))
    diff    = generate_diff(code, optimized)
    metrics = calculate_metrics(code, optimized)

    return {
        "optimized_code": optimized,
        "diff":           diff,
        "metrics":        metrics,
        "language":       language,
        "mode":           mode,
    }


def analyze_code(code: str, language: str, api_key: str) -> dict:
    user_prompt = f"Language: {language}\nCode:\n{code}"
    raw = _clean_fences(_chat(api_key, SYSTEM_ANALYZE, user_prompt))

    try:
        issues = json.loads(raw)
        if not isinstance(issues, list):
            issues = []
    except Exception:
        issues = []

    score = max(20, 100 - sum(
        15 if i.get("severity") == "error"   else
        8  if i.get("severity") == "warning" else 3
        for i in issues
    ))

    return {
        "issues":   issues,
        "score":    score,
        "total":    len(issues),
        "errors":   sum(1 for i in issues if i.get("severity") == "error"),
        "warnings": sum(1 for i in issues if i.get("severity") == "warning"),
        "infos":    sum(1 for i in issues if i.get("severity") == "info"),
    }


def chat_with_ai(message: str, code_context: str, api_key: str) -> str:
    user_prompt = (
        f"Code context:\n{code_context or '(none provided)'}\n\n"
        f"Developer question: {message}"
    )
    return _chat(api_key, SYSTEM_CHAT, user_prompt)


# ── Diff & Metrics ────────────────────────────────────────────────────────────

def generate_diff(original: str, optimized: str) -> list:
    orig_lines = original.splitlines(keepends=True)
    opt_lines  = optimized.splitlines(keepends=True)
    diff_lines = []
    matcher    = difflib.SequenceMatcher(None, orig_lines, opt_lines)

    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == "equal":
            for line in orig_lines[i1:i2]:
                diff_lines.append({"type": "context", "content": line.rstrip()})
        elif op in ("replace", "delete"):
            for line in orig_lines[i1:i2]:
                diff_lines.append({"type": "removed", "content": line.rstrip()})
            if op == "replace":
                for line in opt_lines[j1:j2]:
                    diff_lines.append({"type": "added", "content": line.rstrip()})
        elif op == "insert":
            for line in opt_lines[j1:j2]:
                diff_lines.append({"type": "added", "content": line.rstrip()})

    return diff_lines


def calculate_metrics(original: str, optimized: str) -> dict:
    orig_lines = original.strip().splitlines()
    opt_lines  = optimized.strip().splitlines()
    orig_chars = len(original)
    opt_chars  = len(optimized)

    return {
        "original_lines":       len(orig_lines),
        "optimized_lines":      len(opt_lines),
        "lines_delta":          len(opt_lines) - len(orig_lines),
        "original_chars":       orig_chars,
        "optimized_chars":      opt_chars,
        "chars_reduction":      round((1 - opt_chars / max(orig_chars, 1)) * 100, 1),
        "original_complexity":  _estimate_complexity(original),
        "optimized_complexity": _estimate_complexity(optimized),
    }


def _estimate_complexity(code: str) -> str:
    nested = max_nested = 0
    for line in code.splitlines():
        s = line.lstrip()
        if s.startswith(("for ", "while ")):
            nested += 1
            max_nested = max(max_nested, nested)
        elif s.startswith(("return", "def ", "class ", "func ", "fn ")):
            nested = max(0, nested - 1)
    if max_nested >= 3: return "O(n³)+"
    if max_nested == 2: return "O(n²)"
    if max_nested == 1: return "O(n)"
    return "O(1)/O(n)"