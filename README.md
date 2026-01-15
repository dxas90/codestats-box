# Code::Stats Box - Modern Python Edition

<p align='center'>
  <img src="art/codestats-box.png">
  <h3 align="center">codestats-box</h3>
  <p align="center">💻 Update a pinned gist to contain your Code::Stats stats</p>
</p>

---

Modern Python rewrite of [aksh1618/codestats-box-python](https://github.com/aksh1618/codestats-box-python) with:

- ✨ **Modern Python** (3.12+) with full type hints
- 📦 **uv** for fast dependency management
- 🏗️ **Proper package structure** with src layout
- 🔧 **Pydantic Settings** for configuration validation
- 📝 **Structured logging** with rich output
- 🔄 **Automatic retries** for API calls
- 🎨 **Clean architecture** with separation of concerns

> 📌 For more pinned-gist projects like this one, check out: <https://github.com/matchai/awesome-pinned-gists>

## 🚀 Quick Start

### Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) installed
- Code::Stats account ([Get one here](https://codestats.net/))

### Installation

1. **Install uv** (if not already installed):

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone and setup**:

   ```bash
   git clone https://github.com/yourusername/codestats-box
   cd codestats-box
   uv sync
   ```

3. **Configure environment variables**:

   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

## ⚙️ Configuration

Create a `.env` file with the following variables:

```bash
# Required
GH_TOKEN=ghp_your_github_token_here
GIST_ID=your_gist_id_here
CODE_STATS_USERNAME=your_codestats_username

# Optional (with defaults)
STATS_TYPE=level-xp
TOP_LANGUAGES_COUNT=10
LOG_LEVEL=INFO
```

### Required Setup

1. **Create a GitHub Gist**: <https://gist.github.com/>
2. **Create GitHub Token**: <https://github.com/settings/tokens/new>
   - Select scope: `gist`
3. **Get Gist ID**: From your gist URL
   - Example: `https://gist.github.com/username/`**`ce5221fc5f3739d2c81ce7db99f17519`**

### Stats Types

- **`level-xp`** (Default): Shows levels with XP, sorted by total XP

  ```text
  💻 My Code::Stats XP (Top Languages)
  Total XP :::::::::::::::::::::: lvl  26 (1,104,152 XP)
  Java :::::::::::::::::::::::::: lvl  19 (  580,523 XP)
  ```

- **`recent-xp`**: Shows recent activity with recent XP gains

  ```text
  💻 My Code::Stats XP (Recent Languages)
  Total XP ::::::::::::: lvl  26 (1,104,152 XP) (+1,874)
  Python ::::::::::::::: lvl   7 (   82,719 XP) (+1,789)
  ```

- **`xp`**: Shows only XP values without levels

  ```text
  💻 My Code::Stats XP (Top Languages)
  Total XP :::::::::::::::::::::::::::::::: 1,104,152 XP
  Java ::::::::::::::::::::::::::::::::::::   580,523 XP
  ```

## 🎯 Usage

### Local Execution

```bash
# Run with uv
uv run codestats-box

# Or activate virtual environment
source .venv/bin/activate
codestats-box
```

### Testing

```bash
# Test content only (no gist update)
uv run codestats-box test your_username level-xp

# Test with gist update
uv run codestats-box test your_username recent-xp your_gist_id your_token
```

### GitHub Actions

Update `.github/workflows/codestats.yml`:

```yaml
name: Update Code::Stats Gist

on:
  schedule:
    - cron: "0 */6 * * *"  # Every 6 hours
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v5
        with:
          enable-cache: true
          cache-dependency-glob: "uv.lock"

      - name: Set up Python
        run: uv python install 3.14

      - name: Install dependencies
        run: uv sync

      - name: Update gist
        env:
          GH_TOKEN: ${{ secrets.GH_TOKEN }}
          GIST_ID: ${{ secrets.GIST_ID }}
          CODE_STATS_USERNAME: ${{ secrets.CODE_STATS_USERNAME }}
          STATS_TYPE: level-xp
        run: uv run codestats-box
```

## 🛠️ Development

### Setup Development Environment

```bash
# Install with dev dependencies
uv sync --all-extras

# Run tests
uv run pytest

# Run type checking
uv run mypy src

# Run linting
uv run ruff check src

# Format code
uv run ruff format src
```

### Project Structure

```text
codestats-box/
├── src/
│   └── codestats_box/
│       ├── __init__.py
│       ├── api.py           # Code::Stats API client
│       ├── cli.py           # Command-line interface
│       ├── config.py        # Configuration management
│       ├── exceptions.py    # Custom exceptions
│       ├── formatter.py     # Content formatting
│       ├── gist.py          # GitHub Gist updater
│       ├── logging_config.py # Logging setup
│       ├── models.py        # Data models
│       └── utils.py         # Utility functions
├── tests/
├── pyproject.toml
├── uv.lock
└── README.md
```

## 🎨 Features

### Modern Python Practices

- **Type Safety**: Full type hints with mypy validation
- **Data Validation**: Pydantic models for configuration
- **Error Handling**: Custom exceptions with context
- **Logging**: Structured logging with contextual information
- **Retry Logic**: Automatic retries for transient failures

### Developer Experience

- **Fast Dependencies**: uv for blazing fast package management
- **Code Quality**: Ruff for linting and formatting
- **Testing**: pytest with coverage reporting
- **Type Checking**: mypy with strict mode

## 📝 Environment Variables Reference

| Variable | Required | Default | Description |
| -------- | -------- | ------- | ----------- |
| `GH_TOKEN` | ✅ | - | GitHub personal access token |
| `GIST_ID` | ✅ | - | GitHub Gist ID to update |
| `CODE_STATS_USERNAME` | ✅ | - | Code::Stats username |
| `STATS_TYPE` | ❌ | `level-xp` | Type of stats display |
| `TOP_LANGUAGES_COUNT` | ❌ | `10` | Number of languages to show |
| `MAX_LINE_LENGTH` | ❌ | `54` | Maximum line length for gist |
| `LOG_LEVEL` | ❌ | `INFO` | Logging level |
| `MAX_RETRIES` | ❌ | `3` | Max API retry attempts |

## 🔄 Migration from Old Version

If you're migrating from the original version:

1. **Dependencies**: Replace `pipenv` with `uv`

   ```bash
   rm Pipfile Pipfile.lock requirements.txt
   uv sync
   ```

2. **Code Structure**: Old single file → New package structure
   - Old: `codestats_box.py`
   - New: `src/codestats_box/` package

3. **Configuration**: Environment variables remain the same
   - Optional: Use `.env` file for local development

4. **GitHub Actions**: Update workflow to use uv
   - See example workflow above

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

## 🙏 Acknowledgments

- Original project: [aksh1618/codestats-box-python](https://github.com/aksh1618/codestats-box-python)
- Inspired by [matchai/awesome-pinned-gists](https://github.com/matchai/awesome-pinned-gists)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
