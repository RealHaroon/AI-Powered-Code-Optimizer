# 🧠 AI Code Optimizer

> An End-to-End, full-stack AI-powered code optimization system that analyzes, rewrites, and explains your code using LLaMA 3.3 70B — with a live diff view, quality scoring, AI chat, and PDF export.







***

## ✨ Features

- ⚡ **AI-Powered Optimization** — Rewrites your code for performance, security, readability, and memory efficiency using LLaMA 3.3 70B via Groq
- 🔍 **Deep Static Analysis** — Detects errors, warnings, and info-level issues with line numbers and fix suggestions
- 🔴🟢 **Animated Diff View** — Line-by-line comparison of original vs optimized code (red = removed, green = added)
- 📊 **Quality Score** — 0–100 score based on severity-weighted issue count
- 💬 **AI Chat Assistant** — Ask follow-up questions about your code in natural language
- 📄 **PDF Export** — Download a full optimization report with metrics, issues, and diff
- 🌙 **Dark / Light Mode** — Full theme toggle with system preference detection
- 📱 **Fully Responsive** — Works on desktop and mobile

***

## 🎯 Supported Languages

| Language | Optimization | Analysis | Chat |
|----------|-------------|----------|------|
| Python | ✅ | ✅ | ✅ |
| JavaScript | ✅ | ✅ | ✅ |
| TypeScript | ✅ | ✅ | ✅ |
| Java | ✅ | ✅ | ✅ |
| C++ | ✅ | ✅ | ✅ |
| Go | ✅ | ✅ | ✅ |
| Rust | ✅ | ✅ | ✅ |

***

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Backend** | Python 3.10+, FastAPI |
| **AI Model** | LLaMA 3.3 70B Versatile (via Groq API) |
| **Diff Engine** | Python `difflib` SequenceMatcher |
| **Syntax Highlighting** | Highlight.js |
| **Fonts** | JetBrains Mono (code), Inter (UI) |
| **PDF Export** | JavaScript Blob API |
| **CORS** | FastAPI CORSMiddleware |

***

## 📁 Project Structure

```
ai-code-optimizer/
├── main.py              # FastAPI app — routes, CORS, endpoints
├── optimizer.py         # Core AI logic — optimize, analyze, chat, diff
├── requirements.txt     # Python dependencies
├── frontend/
│   └── code-optimizer.html   # Full single-page web app
└── README.md
```

***

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- A free [Groq API key](https://console.groq.com/keys) (takes 2 minutes)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-code-optimizer.git
cd ai-code-optimizer
```

### 2. Install Dependencies

```bash
pip install fastapi uvicorn groq python-multipart
```

### 3. Run the Backend

```bash
uvicorn main:app --reload --port 8000
```

### 4. Open the Frontend

Open `frontend/code-optimizer.html` in your browser — or serve it:

```bash
# Using Python's built-in server
cd frontend
python -m http.server 3000
# Then open http://localhost:3000/code-optimizer.html
```

### 5. Enter Your API Key

Paste your `gsk_...` Groq API key into the API key field in the app and you're ready.

***

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/optimize` | Optimize code and return diff + metrics |
| `POST` | `/api/analyze` | Analyze code and return issues list |
| `POST` | `/api/chat` | Chat with AI about your code |
| `GET` | `/docs` | Interactive Swagger UI |

### Example Request — Optimize

```bash
curl -X POST http://localhost:8000/api/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def find(arr):\n  for i in arr:\n    for j in arr:\n      if i==j: return i",
    "language": "python",
    "mode": "all",
    "api_key": "gsk_your_key_here"
  }'
```

### Example Response

```json
{
  "optimized_code": "def find(arr: list) -> int:\n    seen = set()\n    for item in arr:\n        if item in seen:\n            return item\n        seen.add(item)\n    return -1",
  "diff": [...],
  "metrics": {
    "original_lines": 4,
    "optimized_lines": 7,
    "original_complexity": "O(n²)",
    "optimized_complexity": "O(n)",
    "chars_reduction": 12.5
  }
}
```

***

## 🧪 Test Code Samples

Paste this into the app to see it in action:

```python
# Bad Python — has O(n²) complexity, SQL injection, hardcoded secret, resource leak

import os

password = "admin123"

def get_user(user_id):
    query = "SELECT * FROM users WHERE id = " + str(user_id)
    return query

def find_duplicates(arr):
    duplicates = []
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] == arr[j]:
                if arr[i] not in duplicates:
                    duplicates.append(arr[i])
    return duplicates

def read_file(filename):
    f = open(filename)
    data = f.read()
    return data

cmd = input("Enter command: ")
os.system(cmd)
```

**What the AI fixes:**
- `O(n²)` nested loops → `O(n)` using a set
- SQL string concatenation → parameterized query
- Hardcoded `password` → environment variable
- `open()` without `close()` → `with` statement
- `os.system(input())` → command injection warning

***

## ⚙️ Optimization Modes

| Mode | What It Does |
|------|-------------|
| **All** | Applies every optimization type |
| **Performance** | Time/space complexity, algorithm efficiency |
| **Security** | SQL injection, eval, secrets, input validation |
| **Readability** | Naming, type hints, docstrings, structure |
| **Memory** | Generators, avoid copies, reduce allocations |

***

## 📊 Metrics Tracked

- Original vs optimized line count
- Character reduction percentage
- Complexity estimate (O(1) → O(n³)+)
- Issue count by severity (errors / warnings / info)
- Quality score (0–100)

***

## 🔒 Security Note

Your Groq API key is never stored — it is sent only with each request and lives in memory only. For production use, move the API key to a backend `.env` file and never expose it in the frontend.

```bash
# .env
GROQ_API_KEY=gsk_your_key_here
```

***

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

***

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

***

## 👨‍💻 Author

Built as an exhibition-level final year project demonstrating full-stack AI integration.

***

## ⭐ Show Your Support

If this project helped you, please consider giving it a ⭐ on GitHub!
