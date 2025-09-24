# 📚 Documentation Index

This file provides an overview of all available documentation for the AI Bot POC project.

## 🌍 Language Versions

All documentation is available in both English and Chinese versions:

- **English**: Primary language, most up-to-date
- **Chinese**: Legacy versions, maintained for reference

## 📋 Documentation Structure

### Main Documentation

| Document | English | Chinese | Description |
|----------|---------|---------|-------------|
| **Project Overview** | `README.md` | - | Main project documentation (English only) |
| **Quick Start** | `QUICK_START_EN.md` | `QUICK_START.md` | Getting started guide |
| **Code Review Bot** | `.github/code-review/README_CODE_REVIEW_BOT_EN.md` | `.github/code-review/README_CODE_REVIEW_BOT.md` | Detailed bot documentation |
| **Workflow Guide** | `.github/code-review/WORKFLOW_GUIDE_EN.md` | `.github/code-review/WORKFLOW_GUIDE.md` | Complete workflow instructions |

### Code Documentation

| File | Language | Description |
|------|----------|-------------|
| `aibot.py` | English | RAG Document Q&A Bot with inline comments |
| `.github/code-review/code_review_bot.py` | English | Remote PR review bot |
| `.github/code-review/local_review.py` | English | Local branch review script |
| `.github/code-review/diff_analyzer.py` | English | Advanced diff analysis module |
| `.github/code-review/review_prompts.py` | English | Review prompt management |
| `.github/code-review/test_bot.py` | English | Test suite |

### Configuration Files

| File | Description |
|------|-------------|
| `.github/code-review/config.json` | Review rules and AI settings |
| `.github/code-review/env.example` | Environment variables template |
| `.github/code-review/requirements.txt` | Python dependencies |

### Scripts and Workflows

| File | Description |
|------|-------------|
| `code-review.sh` | Convenient local review script |
| `.github/code-review/demo_workflow.sh` | Workflow demonstration script |
| `.github/workflows/ai-code-review.yml` | GitHub Actions workflow |
| `.github/workflows/local-review-check.yml` | Local review validation workflow |

## 🚀 Quick Access

### For New Users

1. **Start Here**: `README.md` - Project overview
2. **Get Started**: `QUICK_START_EN.md` - Quick start guide
3. **Learn More**: `.github/code-review/README_CODE_REVIEW_BOT_EN.md` - Detailed documentation

### For Developers

1. **Workflow**: `.github/code-review/WORKFLOW_GUIDE_EN.md` - Complete workflow guide
2. **Configuration**: `.github/code-review/config.json` - Customize review rules
3. **Testing**: `.github/code-review/test_bot.py` - Run tests

### For Teams

1. **Setup**: `QUICK_START_EN.md` - Team setup instructions
2. **Integration**: `.github/workflows/` - GitHub Actions configuration
3. **Best Practices**: `.github/code-review/WORKFLOW_GUIDE_EN.md` - Team workflow

## 🔧 Usage Examples

### Local Development

```bash
# Quick start
./code-review.sh main

# Detailed review
python .github/code-review/local_review.py main --output review.md
```

### Team Integration

```bash
# Setup GitHub Actions
cp .github/workflows/ai-code-review.yml .github/workflows/

# Configure secrets
# GOOGLE_API_KEY: Your Google AI API key
# GITHUB_TOKEN: Automatically provided
```

### Customization

```bash
# Edit review rules
vim .github/code-review/config.json

# Add custom prompts
vim .github/code-review/review_prompts.py
```

## 📖 Reading Order

### For Beginners

1. `README.md` - Understand the project
2. `QUICK_START_EN.md` - Get started quickly
3. `.github/code-review/README_CODE_REVIEW_BOT_EN.md` - Learn the details

### For Advanced Users

1. `.github/code-review/WORKFLOW_GUIDE_EN.md` - Complete workflow
2. `.github/code-review/config.json` - Configuration options
3. `.github/code-review/review_prompts.py` - Custom prompts

### For Contributors

1. `.github/code-review/test_bot.py` - Run tests
2. `.github/code-review/diff_analyzer.py` - Understand analysis
3. `.github/workflows/` - CI/CD integration

## 🌐 Language Support

### English (Primary)

- ✅ All documentation
- ✅ All code comments
- ✅ All user interfaces
- ✅ All error messages

### Chinese (Legacy)

- ✅ Main documentation files
- ✅ Quick start guide
- ✅ Workflow guide
- ⚠️ May not be up-to-date

## 📝 Contributing to Documentation

When updating documentation:

1. **Update English version first**
2. **Update Chinese version if needed**
3. **Update this index**
4. **Test all examples**

## 🔗 External Resources

- [LangChain Documentation](https://langchain.com/docs)
- [Google AI Documentation](https://ai.google.dev/docs)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Code Review Best Practices](https://github.com/microsoft/vscode/wiki/Code-Review-Guidelines)

---

**Note**: English documentation is the primary source of truth. Chinese documentation is maintained for reference but may not always be up-to-date.
