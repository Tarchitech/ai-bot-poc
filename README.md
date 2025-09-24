# AI Bot POC

This project contains multiple AI bot proof-of-concept implementations, demonstrating different AI application scenarios.

## 📁 Project Structure

```
ai-bot-poc/
├── .github/
│   ├── code-review/           # AI Code Review Bot
│   │   ├── code_review_bot.py
│   │   ├── local_review.py
│   │   ├── diff_analyzer.py
│   │   ├── review_prompts.py
│   │   ├── config.json
│   │   ├── requirements.txt
│   │   ├── env.example
│   │   ├── test_bot.py
│   │   ├── README_CODE_REVIEW_BOT.md
│   │   ├── README_CODE_REVIEW_BOT_EN.md
│   │   ├── WORKFLOW_GUIDE.md
│   │   ├── WORKFLOW_GUIDE_EN.md
│   │   └── demo_workflow.sh
│   └── workflows/
│       ├── ai-code-review.yml
│       └── local-review-check.yml
├── docs/                      # Document files
│   ├── 1.pdf
│   ├── 2.pdf
│   ├── 3.doc
│   ├── 3.pdf
│   ├── 4.doc
│   ├── 4.pdf
│   ├── 5.docx
│   └── 5.pdf
├── aibot.py                   # RAG Document Q&A Bot
├── code-review.sh             # Convenient code review script
├── QUICK_START.md             # Quick start guide (Chinese)
├── QUICK_START_EN.md          # Quick start guide (English)
└── README.md                  # This file
```

## 🤖 Included Bots

### 1. RAG Document Q&A Bot (`aibot.py`)

A Retrieval-Augmented Generation (RAG) based document Q&A bot that can answer questions about PDF document content.

**Features:**
- PDF document loading and parsing support
- Uses Google Gemini AI for Q&A
- Vector storage and semantic search
- Supports chunking for large documents

**Usage:**
```bash
python aibot.py
```

### 2. AI Code Review Bot (`.github/code-review/`)

An intelligent code review bot that automatically analyzes GitHub Pull Requests and provides review suggestions.

**Features:**
- Multi-language code review support
- Security vulnerability detection
- Performance analysis
- Code quality assessment
- GitHub Actions automatic integration
- Local review support

**Usage:**

**Quick Start (Recommended):**
```bash
# Use convenient script for local review (includes all changes by default)
# This includes: committed changes, staged changes, working directory changes, and untracked files
./code-review.sh main

# Specify output file
./code-review.sh main --output my_review.md

# JSON format output
./code-review.sh main --format json

# Only review committed changes (excludes uncommitted and untracked files)
./code-review.sh main --committed-only
```

**Direct Call:**
```bash
# Local review
python .github/code-review/local_review.py main

# Remote PR review
python .github/code-review/code_review_bot.py <PR_NUMBER>
```

**View Detailed Documentation:**
```bash
# English documentation
cat .github/code-review/README_CODE_REVIEW_BOT_EN.md
cat .github/code-review/WORKFLOW_GUIDE_EN.md
cat QUICK_START_EN.md

# Chinese documentation (legacy)
cat .github/code-review/README_CODE_REVIEW_BOT.md
cat .github/code-review/WORKFLOW_GUIDE.md
cat QUICK_START.md
```

## 🚀 Quick Start

### Requirements

- Python 3.8+
- Google AI API Key
- GitHub Personal Access Token (only required for code review bot)

### Install Dependencies

```bash
# Install RAG bot dependencies
pip install langchain langchain_community langchain-google-genai faiss-cpu pypdf

# Install code review bot dependencies
pip install -r .github/code-review/requirements.txt
```

### Configure Environment Variables

```bash
# Set Google AI API Key
export GOOGLE_API_KEY="your_google_ai_api_key_here"

# Additional requirements for code review bot
export GITHUB_TOKEN="your_github_token_here"
export REPO_OWNER="your_github_username"
export REPO_NAME="your_repository_name"
```

## 📚 Detailed Documentation

- **RAG Bot**: See comments in `aibot.py`
- **Code Review Bot**: See `.github/code-review/README_CODE_REVIEW_BOT_EN.md`
- **Workflow Guide**: See `.github/code-review/WORKFLOW_GUIDE_EN.md`
- **Quick Start**: See `QUICK_START_EN.md`

## 🔧 Development

### Testing

```bash
# Test code review bot
python .github/code-review/test_bot.py
```

### Contributing

Welcome to submit Issues and Pull Requests to improve these bots!

## 📄 License

This project is licensed under the MIT License.

---

**Note**: These are proof-of-concept projects. Please conduct thorough testing and evaluation before using in production environments.
