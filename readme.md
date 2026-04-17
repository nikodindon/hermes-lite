# Hermes Lite – Multi‑Agent AI Router (OpenRouter Edition)

[![Version](https://img.shields.io/badge/version-0.2-brightgreen)](https://github.com/nikodindon/hermes-lite/releases/tag/v0.2)
**Stable MVP** – Multi-agent router utilisant uniquement des modèles gratuits OpenRouter.

## 🎯 Goal
A lightweight CLI tool that routes a user query to several **free** OpenRouter models, compares their answers, and synthesises the best response.

## 📂 Project Layout
```
hermes-lite/
│   readme.md               # <-- you are reading it now
│   requirements.txt        # Python dependencies
│   .env                    # OpenRouter API key (not version‑controlled)
│
├─ core/                     # Core orchestration logic
│   ├─ router.py            # Model selection based on intent
│   ├─ orchestrator.py      # Async parallel calls
│   ├─ aggregator.py        # Merge responses
│   ├─ benchmark.py         # Timing / token counting / scoring
│   ├─ benchmark_formatter.py # Pretty Rich tables
│   └─ memory.py            # Simple JSON memory (future work)
│
├─ agents/                   # Small agents handling specific steps
│   ├─ analyst.py           # Analyse the user prompt
│   ├─ critic.py            # Score a single response
│   └─ synthesizer.py       # (placeholder – can be extended)
│
├─ providers/                # API wrappers
│   └─ openrouter.py        # Calls OpenRouter chat/completions endpoint
│
├─ models/                   # Configuration of free models
│   └─ config.py            # List of free model IDs and defaults
│
├─ utils/                    # Helper utilities
│   └─ logger.py            # Rich‑based logger
│
├─ cli/                      # Command line entry point
│   └─ main.py              # Interactive REPL / one‑shot mode
│
└─ data/                     # Persistent data (memory, cache, …)
    └─ memory.json
```

## 📦 Installation
1. **Clone the repo** (you already have it):
   ```bash
   git clone https://github.com/nikodindon/hermes-lite.git
   cd hermes-lite
   ```
2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # on Windows
   # source .venv/bin/activate   # on Unix‑like systems
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Add your OpenRouter API key** (do **not** commit this file):
   ```bash
   echo OPENROUTER_API_KEY=your_key_here > .env
   ```
   The `.env` file is ignored by git via the default `.gitignore` that ships with the template.

## 💾 Memory (optional)
The project includes a simple persistent memory store. It is used automatically:
- After each successful query, the prompt, selected model and score are stored in `data/memory.json`.
- On startup, the preferred model is suggested based on past scores (`memory.get_preferred_model(...)`).
- To disable, simply remove or rename `data/memory.json`.

## 🚀 Quick start
### Install
```bash
pip install -r requirements.txt
```
### Commands
**Interactive REPL**
```bash
python -m cli.main
```
**One‑shot call**
```bash
python -m cli.main "Explain Kubernetes in simple terms" --bench
```
**Benchmark only**
```bash
python -m cli.main --bench
```
* `--bench` prints a colourful table with latency, token usage and a simple score for each model.

## 🛠️ How it works
1. **Analyst** – inspects the prompt and returns an `Intent` (simple, complex, code, …).
2. **Router** – chooses one or more free models according to the intent.
3. **Orchestrator** – fires concurrent HTTP calls to OpenRouter.
4. **Critic** – gives each raw response a lightweight score (clarity, precision, hallucination).
5. **Aggregator** – scores all responses and synthesises a final answer with justification.
6. **Benchmark** – records latency, token count and critic scores for comparison.
7. **BenchmarkFormatter** – prints a Rich table highlighting the winner.

## 📊 Benchmark example
```text
┌───────────────────────────────┬─────────┬───────┬───────┐
│ Model                           │ Latency │ Score │ Tokens│
├───────────────────────────────┼─────────┼───────┼───────┤
│ google/gemma-4-31b-it          │ 1.2s    │ 0.82  │ 320   │
│ google/gemma-4-26b-a4b-it      │ 0.9s    │ 0.79  │ 280   │
│ qwen/qwen3-coder               │ 1.5s    │ 0.91  │ 350   │
└───────────────────────────────┴─────────┴───────┴───────┘
Winner: qwen/qwen3-coder with score 0.91
```

## 🧪 Testing (future work)
Unit tests are not yet in the repository, but the structure is ready for `pytest`. Feel free to add tests under a `tests/` folder and run:
```bash
pytest
```

## 🤝 Contributing
1. Fork the repository.
2. Create a feature branch (`git checkout -b my‑feature`).
3. Make your changes, add tests if applicable.
4. Commit with a clear message (`git commit -m "Add X feature"`).
5. Push and open a Pull Request.

## 📜 License
MIT – feel free to adapt, extend and use it in your own projects.

---
*Enjoy exploring the free‑model universe with Hermes Lite!*
