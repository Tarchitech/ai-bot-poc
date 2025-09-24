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
# Simplest way: use convenient script
./code-review.sh main

# Specify output file
./code-review.sh main --output my_review.md

# JSON format output
./code-review.sh main --format json -o review.json
```

## 🎯 使用场景

### 场景 1: 开发新功能

```bash
# 1. 创建新分支
git checkout -b feature/new-feature

# 2. 编写代码...

# 3. 本地审查
./code-review.sh main

# 4. 修复问题后提交
git add .
git commit -m "feat: add new feature"

# 5. 推送到远程
git push origin feature/new-feature

# 6. 创建 PR（GitHub Actions 会自动审查）
```

### 场景 2: 修复 Bug

```bash
# 1. 创建修复分支
git checkout -b fix/bug-123

# 2. 修复代码...

# 3. 审查修复
./code-review.sh main --output bug_fix_review.md

# 4. 提交修复
git add .
git commit -m "fix: resolve bug #123"

# 5. 推送并创建 PR
git push origin fix/bug-123
```

### 场景 3: 重构代码

```bash
# 1. 创建重构分支
git checkout -b refactor/improve-performance

# 2. 重构代码...

# 3. 详细审查
./code-review.sh main --format json --output refactor_review.json

# 4. 分析审查结果
cat refactor_review.json | jq '.summary'

# 5. 提交重构
git add .
git commit -m "refactor: improve performance"

# 6. 推送并创建 PR
git push origin refactor/improve-performance
```

## 🔧 高级用法

### 自定义配置

```bash
# 使用自定义配置文件
./code-review.sh main --config my_config.json

# 指定当前分支
./code-review.sh main --current-branch feature/auth
```

### 批量审查

```bash
# 审查多个分支
for branch in feature/auth feature/payment feature/notification; do
    echo "Reviewing $branch..."
    ./code-review.sh main --current-branch $branch --output "review_${branch}.md"
done
```

### 集成到 CI/CD

```bash
# 在 CI 脚本中使用
if ./code-review.sh main --format json --output ci_review.json; then
    echo "Code review passed"
    # 继续部署流程
else
    echo "Code review failed"
    exit 1
fi
```

## 📊 审查报告示例

### Markdown 格式

```markdown
# Code Review Report

**Generated**: 2024-01-15T10:30:00
**Branch Comparison**: main → feature/auth
**Files Changed**: 5
**Additions**: 120
**Deletions**: 15

## 🔍 Detailed Review

## 🔒 Security Review Summary
Overall security assessment: 发现 1 个潜在安全问题

## 🚨 Critical Issues
- **File**: src/auth/login.py
  - **Line**: 25
  - **Issue**: 硬编码的 JWT 密钥
  - **Risk**: 可能导致安全漏洞
  - **Fix**: 使用环境变量存储密钥

## 💡 Recommendations
- 实施输入验证
- 使用 HTTPS 进行所有通信
- 添加日志记录
```

### JSON 格式

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
    "实施输入验证",
    "使用环境变量存储敏感信息"
  ],
  "risk_factors": [
    "security: password|secret|key|token",
    "performance: for.*for"
  ]
}
```

## 🚨 故障排除

### 常见问题

1. **API 密钥错误**
   ```
   ❌ GOOGLE_API_KEY environment variable not set
   ```
   **解决**: 设置正确的 API 密钥

2. **Python 依赖缺失**
   ```
   ⚠️ Missing Python packages: langchain requests
   ```
   **解决**: `pip install -r .github/code-review/requirements.txt`

3. **Git 仓库错误**
   ```
   ❌ Not in a git repository
   ```
   **解决**: 确保在 Git 仓库根目录运行

4. **分支不存在**
   ```
   ❌ Base branch 'main' not found
   ```
   **解决**: 检查分支名称或创建分支

### 调试模式

```bash
# 启用详细输出
export DEBUG=true
./code-review.sh main
```

## 📚 更多资源

- **完整文档**: `.github/code-review/README_CODE_REVIEW_BOT.md`
- **工作流程指南**: `.github/code-review/WORKFLOW_GUIDE.md`
- **演示脚本**: `.github/code-review/demo_workflow.sh`

## 🎉 开始使用

现在您已经了解了基本用法，开始使用 AI 代码审查机器人来提高代码质量吧！

```bash
# 立即开始
./code-review.sh main
```

Happy coding! 🚀
