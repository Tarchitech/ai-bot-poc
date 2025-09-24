# AI Code Review Bot

An AI-based automated code review bot that can analyze GitHub Pull Request code differences and provide intelligent review suggestions.

## 🚀 Features

- **Intelligent Code Review**: Uses Google Gemini AI for deep code analysis
- **Multi-language Support**: Supports Python, JavaScript, TypeScript, Java, C++, Go, Rust, etc.
- **Security Detection**: Automatically identifies potential security vulnerabilities and risks
- **Performance Analysis**: Detects performance bottlenecks and optimization opportunities
- **Code Quality**: Evaluates code maintainability and best practices
- **Automated Integration**: Automatically triggers review through GitHub Actions
- **Configurable Rules**: Supports custom review rules and prompts

## 📋 System Requirements

- Python 3.8+
- GitHub Personal Access Token
- Google AI API Key
- Git (for version control)

## 🛠️ Installation and Configuration

### 1. Clone or Download Code

```bash
git clone <your-repo-url>
cd ai-bot-poc
```

### 2. Install Dependencies

```bash
pip install -r .github/code-review/requirements.txt
```

### 3. Configure Environment Variables

Copy environment variable template:
```bash
cp .github/code-review/env.example .env
```

Edit the `.env` file and fill in the following information:

```bash
# GitHub Configuration
GITHUB_TOKEN=your_github_personal_access_token_here
REPO_OWNER=your_github_username
REPO_NAME=your_repository_name

# Google AI Configuration
GOOGLE_API_KEY=your_google_ai_api_key_here

# Optional: Bot Configuration
BOT_NAME=AI Code Review Bot
REVIEW_ENABLED=true
AUTO_APPROVE_SMALL_CHANGES=false
MAX_REVIEW_COMMENTS=10
```

### 4. Get Required API Keys

#### GitHub Personal Access Token
1. Visit [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Select the following permissions:
   - `repo` (full repository access)
   - `pull_requests` (pull requests)
   - `issues` (issues)
4. Copy the generated token

#### Google AI API Key
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Copy the generated key

### 5. Configure GitHub Actions

Add the `.github/workflows/ai-code-review.yml` file to your repository and add the following Secrets in GitHub repository settings:

- `GOOGLE_API_KEY`: Your Google AI API key
- `GITHUB_TOKEN`: Your GitHub Personal Access Token (usually automatically provided)

## 🎯 Usage

### Local Code Review (Recommended)

Before submitting a PR, perform local review first:

```bash
# Compare current branch with main branch (includes all changes by default)
# This includes: committed changes, staged changes, working directory changes, and untracked files
python .github/code-review/local_review.py main

# Specify output file
python .github/code-review/local_review.py main --output my_review.md

# JSON format output
python .github/code-review/local_review.py main --format json

# Only review committed changes (excludes uncommitted and untracked files)
python .github/code-review/local_review.py main --committed-only

# Explicitly include all uncommitted changes (default behavior)
python .github/code-review/local_review.py main --include-uncommitted
```

### Remote Automatic Review

After configuring GitHub Actions, the bot will automatically run in the following situations:
- New Pull Request created
- Pull Request updated
- Pull Request reopened
- Pull Request marked as ready for review

### Manual Remote Review

```bash
# Review specific Pull Request
python .github/code-review/code_review_bot.py <PR_NUMBER>

# For example: review PR #123
python .github/code-review/code_review_bot.py 123
```

## ⚙️ Configuration Options

### Review Rules Configuration (.github/code-review/config.json)

```json
{
  "rules": [
    {
      "name": "security_check",
      "description": "Check for potential security vulnerabilities",
      "severity": "error",
      "pattern": "password|secret|key|token",
      "suggestion": "Consider using environment variables or secure storage for sensitive data"
    }
  ],
  "ai_settings": {
    "model": "models/gemini-2.5-pro",
    "temperature": 0.1,
    "max_tokens": 2000
  },
  "review_settings": {
    "max_files_per_review": 50,
    "max_lines_per_file": 1000,
    "skip_files": ["*.min.js", "*.min.css"],
    "focus_languages": ["python", "javascript", "typescript"]
  }
}
```

### Custom Review Prompts

You can customize different types of review prompts by modifying `.github/code-review/review_prompts.py`:

- **Security Review**: Focus on security vulnerability detection
- **Performance Review**: Analyze performance bottlenecks
- **Maintainability Review**: Evaluate code quality
- **Best Practices Review**: Check coding standards
- **Documentation Review**: Check documentation completeness
- **Testing Review**: Evaluate test coverage

## 📊 Review Report Example

The bot will post detailed review reports in Pull Requests, including:

```
🤖 AI Code Review Results

## 🔒 Security Review Summary
Overall security assessment: Found 2 potential security issues

## 🚨 Critical Security Issues
- **File**: auth.py
  - **Line**: 15
  - **Issue**: Hardcoded API key
  - **Risk**: May lead to security vulnerabilities
  - **Fix**: Use environment variables to store sensitive information

## ⚠️ Security Warnings
- **File**: database.py
  - **Line**: 42
  - **Issue**: Potential SQL injection risk
  - **Suggestion**: Use parameterized queries

## 💡 Security Recommendations
- Implement input validation
- Use HTTPS for all communications
- Regularly update dependencies
```

## 🔧 Advanced Features

### 1. Diff Analysis

`.github/code-review/diff_analyzer.py` provides advanced code diff analysis:

- Automatic language detection
- Change impact assessment
- Risk factor identification
- Complexity change analysis

### 2. Multi-language Support

Supports specific reviews for the following programming languages:

- **Python**: PEP 8 standards, type hints, exception handling
- **JavaScript/TypeScript**: ES6+ features, type safety, async handling
- **Java**: Design patterns, memory management, exception handling
- **C++**: Memory safety, RAII, modern C++ features
- **Go**: Concurrency safety, error handling, performance optimization
- **Rust**: Ownership, lifetimes, memory safety

### 3. Custom Rules Engine

You can add custom review rules by modifying `.github/code-review/config.json`:

```json
{
  "name": "custom_rule",
  "description": "Custom rule description",
  "severity": "warning",
  "pattern": "your_regex_pattern",
  "suggestion": "Improvement suggestion"
}
```

## 🚨 Troubleshooting

### Common Issues

1. **API Key Error**
   ```
   Error: Missing required environment variables: GOOGLE_API_KEY
   ```
   **Solution**: Ensure API key is correctly set in `.env` file

2. **GitHub Permission Error**
   ```
   Error: 403 Forbidden
   ```
   **Solution**: Check if GitHub token has sufficient permissions

3. **Network Connection Issues**
   ```
   Error: Connection timeout
   ```
   **Solution**: Check network connection, consider using proxy

### Debug Mode

Enable verbose log output:

```bash
export DEBUG=true
python .github/code-review/code_review_bot.py <PR_NUMBER>
```

## 📈 Performance Optimization

### 1. Batch Processing

For large PRs, the bot automatically processes files in batches to avoid API limits.

### 2. Caching Mechanism

The bot caches analyzed files to improve performance.

### 3. Parallel Processing

Supports parallel analysis of multiple files to improve speed.

## 🔒 Security Considerations

- API keys are stored in environment variables and not committed to the codebase
- All sensitive information is properly sanitized
- Supports private repository reviews
- Follows the principle of least privilege

## 🤝 Contributing

Welcome to submit Issues and Pull Requests to improve this project!

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) - AI application development framework
- [Google Gemini](https://ai.google.dev/) - AI model
- [GitHub API](https://docs.github.com/en/rest) - GitHub integration

## 📚 Related Documentation

- **Complete Workflow Guide**: See `WORKFLOW_GUIDE_EN.md`
- **Local Review Script**: See `local_review.py`
- **Test Script**: See `test_bot.py`

---

**Note**: This is a proof-of-concept project. Please conduct thorough testing and evaluation before using in production environments.
