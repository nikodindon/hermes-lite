# Hermes Lite – Multi‑Agent AI Router (OpenRouter Edition)

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

## 🚀 Quick start
Run the interactive REPL:
```bash
python -m cli.main
```
Or make a one‑shot call:
```bash
python -m cli.main "Explain Kubernetes in simple terms" --bench
```
* `--bench` prints a colourful table with latency, token usage and a simple score for each model.

## 🛠️ How it works
1. **Analyst** – inspects the prompt and returns an `Intent` (simple, complex, code, …).
2. **Router** – chooses one or more free models according to the intent.
3. **Orchestrator** – fires concurrent HTTP calls to OpenRouter.
4. **Critic** – gives each raw response a lightweight score (length, token count, etc.).
5. **Aggregator** – picks the most “central” answer (median length heuristic).
6. **Benchmark** – records latency, token count and the critic score for each model.
7. **BenchmarkFormatter** – prints a Rich table and highlights the winner.

## 📊 Benchmark example
```text
┌───────────────────────────────┬─────────────┬───────┬───────┐
│ Model                           │ Latency (s) │ Tokens│ Score │
├───────────────────────────────┼─────────────┼───────┼───────┤
│ meta-llama/llama-3-8b-instruct │ 1.21        │ 312   │ 0.9   │
│ mistralai/mistral-7b-instruct  │ 0.95        │ 298   │ 0.8   │
│ google/gemma-7b-it              │ 1.48        │ 340   │ 0.85  │
└───────────────────────────────┴─────────────┴───────┴───────┘
Winner: meta-llama/llama-3-8b-instruct with score 0.9
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
