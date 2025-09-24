# 🚀 Quick Start Guide

Quick start guide for using the AI Code Review Bot.

## 📋 Prerequisites

1. **Python 3.8+**
2. **Git repository**
3. **Google AI API Key**

## ⚡ Quick Start

### 1. Set up API Key

```bash
# Method 1: Environment variable
export GOOGLE_API_KEY="your_google_ai_api_key_here"

# Method 2: .env file
echo 'GOOGLE_API_KEY=your_google_ai_api_key_here' > .env
source .env
```

### 2. Install Dependencies

```bash
pip install -r .github/code-review/requirements.txt
```

### 3. Run Code Review

```bash
# Simplest way: use convenient script (includes all changes by default)
# This includes: committed changes, staged changes, working directory changes, and untracked files
./code-review.sh main

# Specify output file
./code-review.sh main --output my_review.md

# JSON format output
./code-review.sh main --format json -o review.json

# Only review committed changes (excludes uncommitted and untracked files)
./code-review.sh main --committed-only

# Explicitly include all uncommitted changes (default behavior)
./code-review.sh main --include-uncommitted
```

## 🎯 Use Cases

### Case 1: Developing New Features

```bash
# 1. Create new branch
git checkout -b feature/new-feature

# 2. Write code...

# 3. Local review
./code-review.sh main

# 4. Commit after fixing issues
git add .
git commit -m "feat: add new feature"

# 5. Push to remote
git push origin feature/new-feature

# 6. Create PR (GitHub Actions will automatically review)
```

### Case 2: Fixing Bugs

```bash
# 1. Create fix branch
git checkout -b fix/bug-123

# 2. Fix code...

# 3. Review the fix
./code-review.sh main --output bug_fix_review.md

# 4. Commit the fix
git add .
git commit -m "fix: resolve bug #123"

# 5. Push and create PR
git push origin fix/bug-123
```

### Case 3: Refactoring Code

```bash
# 1. Create refactor branch
git checkout -b refactor/improve-performance

# 2. Refactor code...

# 3. Detailed review
./code-review.sh main --format json --output refactor_review.json

# 4. Analyze review results
cat refactor_review.json | jq '.summary'

# 5. Commit refactoring
git add .
git commit -m "refactor: improve performance"

# 6. Push and create PR
git push origin refactor/improve-performance
```

## 🔧 Advanced Usage

### Custom Configuration

```bash
# Use custom configuration file
./code-review.sh main --config my_config.json

# Specify current branch
./code-review.sh main --current-branch feature/auth
```

### Batch Review

```bash
# Review multiple branches
for branch in feature/auth feature/payment feature/notification; do
    echo "Reviewing $branch..."
    ./code-review.sh main --current-branch $branch --output "review_${branch}.md"
done
```

### CI/CD Integration

```bash
# Use in CI scripts
if ./code-review.sh main --format json --output ci_review.json; then
    echo "Code review passed"
    # Continue deployment process
else
    echo "Code review failed"
    exit 1
fi
```

## 📊 Review Report Examples

### Markdown Format

```markdown
# Code Review Report

**Generated**: 2024-01-15T10:30:00
**Branch Comparison**: main → feature/auth
**Files Changed**: 5
**Additions**: 120
**Deletions**: 15

## 🔍 Detailed Review

## 🔒 Security Review Summary
Overall security assessment: Found 1 potential security issue

## 🚨 Critical Issues
- **File**: src/auth/login.py
  - **Line**: 25
  - **Issue**: Hardcoded JWT secret key
  - **Risk**: May lead to security vulnerabilities
  - **Fix**: Use environment variables to store the key

## 💡 Recommendations
- Implement input validation
- Use HTTPS for all communications
- Add logging
```

### JSON Format

```json
{
  "timestamp": "2024-01-15T10:30:00",
  "base_branch": "main",
  "current_branch": "feature/auth",
  "files_changed": ["src/auth/login.py", "src/auth/register.py"],
  "total_additions": 120,
  "total_deletions": 15,
  "summary": {
    "total_files_changed": 2,
    "impact_breakdown": {
      "critical": 1,
      "high": 2,
      "medium": 3,
      "low": 5
    }
  },
  "detailed_review": "## 🔒 Security Review Summary...",
  "recommendations": [
    "Implement input validation",
    "Use environment variables for sensitive information"
  ],
  "risk_factors": [
    "security: password|secret|key|token",
    "performance: for.*for"
  ]
}
```

## 🚨 Troubleshooting

### Common Issues

1. **API Key Error**
   ```
   ❌ GOOGLE_API_KEY environment variable not set
   ```
   **Solution**: Set the correct API key

2. **Missing Python Dependencies**
   ```
   ⚠️ Missing Python packages: langchain requests
   ```
   **Solution**: `pip install -r .github/code-review/requirements.txt`

3. **Git Repository Error**
   ```
   ❌ Not in a git repository
   ```
   **Solution**: Ensure you're running from the Git repository root

4. **Branch Not Found**
   ```
   ❌ Base branch 'main' not found
   ```
   **Solution**: Check branch name or create the branch

### Debug Mode

```bash
# Enable verbose output
export DEBUG=true
./code-review.sh main
```

## 📚 More Resources

- **Complete Documentation**: `.github/code-review/README_CODE_REVIEW_BOT.md`
- **Workflow Guide**: `.github/code-review/WORKFLOW_GUIDE_EN.md`
- **Demo Script**: `.github/code-review/demo_workflow.sh`

## 🎉 Get Started

Now that you understand the basic usage, start using the AI Code Review Bot to improve code quality!

```bash
# Start immediately
./code-review.sh main
```

Happy coding! 🚀
