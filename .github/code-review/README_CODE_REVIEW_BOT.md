# AI Code Review Bot

An AI-based automated code review bot that can analyze GitHub Pull Request code differences and provide intelligent review suggestions.

## 🚀 功能特性

- **智能代码审查**: 使用 Google Gemini AI 进行深度代码分析
- **多语言支持**: 支持 Python、JavaScript、TypeScript、Java、C++、Go、Rust 等
- **安全检测**: 自动识别潜在的安全漏洞和风险
- **性能分析**: 检测性能瓶颈和优化机会
- **代码质量**: 评估代码可维护性和最佳实践
- **自动化集成**: 通过 GitHub Actions 自动触发审查
- **可配置规则**: 支持自定义审查规则和提示词

## 📋 系统要求

- Python 3.8+
- GitHub Personal Access Token
- Google AI API Key
- Git (用于版本控制)

## 🛠️ 安装和配置

### 1. 克隆或下载代码

```bash
git clone <your-repo-url>
cd ai-bot-poc
```

### 2. 安装依赖

```bash
pip install -r .github/code-review/requirements.txt
```

### 3. 配置环境变量

复制环境变量模板：
```bash
cp .github/code-review/env.example .env
```

编辑 `.env` 文件，填入以下信息：

```bash
# GitHub 配置
GITHUB_TOKEN=your_github_personal_access_token_here
REPO_OWNER=your_github_username
REPO_NAME=your_repository_name

# Google AI 配置
GOOGLE_API_KEY=your_google_ai_api_key_here

# 可选：机器人配置
BOT_NAME=AI Code Review Bot
REVIEW_ENABLED=true
AUTO_APPROVE_SMALL_CHANGES=false
MAX_REVIEW_COMMENTS=10
```

### 4. 获取必要的 API 密钥

#### GitHub Personal Access Token
1. 访问 [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. 点击 "Generate new token (classic)"
3. 选择以下权限：
   - `repo` (完整仓库访问)
   - `pull_requests` (拉取请求)
   - `issues` (问题)
4. 复制生成的 token

#### Google AI API Key
1. 访问 [Google AI Studio](https://aistudio.google.com/app/apikey)
2. 创建新的 API 密钥
3. 复制生成的密钥

### 5. 配置 GitHub Actions

将 `.github/workflows/ai-code-review.yml` 文件添加到你的仓库中，并在 GitHub 仓库设置中添加以下 Secrets：

- `GOOGLE_API_KEY`: 你的 Google AI API 密钥
- `GITHUB_TOKEN`: 你的 GitHub Personal Access Token (通常自动提供)

## 🎯 使用方法

### 本地代码审查（推荐）

在提交 PR 之前，先进行本地审查：

```bash
# 比较当前分支与 main 分支
python .github/code-review/local_review.py main

# 指定输出文件
python .github/code-review/local_review.py main --output my_review.md

# JSON 格式输出
python .github/code-review/local_review.py main --format json
```

### 远程自动审查

配置 GitHub Actions 后，机器人会在以下情况自动运行：
- 新的 Pull Request 创建
- Pull Request 更新
- Pull Request 重新打开
- Pull Request 标记为准备审查

### 手动运行远程审查

```bash
# 审查特定的 Pull Request
python .github/code-review/code_review_bot.py <PR_NUMBER>

# 例如：审查 PR #123
python .github/code-review/code_review_bot.py 123
```

## ⚙️ 配置选项

### 审查规则配置 (.github/code-review/config.json)

```json
{
  "rules": [
    {
      "name": "security_check",
      "description": "检查潜在的安全漏洞",
      "severity": "error",
      "pattern": "password|secret|key|token",
      "suggestion": "考虑使用环境变量或安全存储敏感数据"
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

### 自定义审查提示词

你可以通过修改 `.github/code-review/review_prompts.py` 来自定义不同类型的审查提示词：

- **安全审查**: 专注于安全漏洞检测
- **性能审查**: 分析性能瓶颈
- **可维护性审查**: 评估代码质量
- **最佳实践审查**: 检查编码标准
- **文档审查**: 检查文档完整性
- **测试审查**: 评估测试覆盖率

## 📊 审查报告示例

机器人会在 Pull Request 中发布详细的审查报告，包括：

```
🤖 AI Code Review Results

## 🔒 Security Review Summary
Overall security assessment: 发现 2 个潜在安全问题

## 🚨 Critical Security Issues
- **File**: auth.py
  - **Line**: 15
  - **Issue**: 硬编码的 API 密钥
  - **Risk**: 可能导致安全漏洞
  - **Fix**: 使用环境变量存储敏感信息

## ⚠️ Security Warnings
- **File**: database.py
  - **Line**: 42
  - **Issue**: 潜在的 SQL 注入风险
  - **Suggestion**: 使用参数化查询

## 💡 Security Recommendations
- 实施输入验证
- 使用 HTTPS 进行所有通信
- 定期更新依赖项
```

## 🔧 高级功能

### 1. 差异分析

`.github/code-review/diff_analyzer.py` 提供高级的代码差异分析：

- 自动语言检测
- 变更影响评估
- 风险因素识别
- 复杂度变化分析

### 2. 多语言支持

支持以下编程语言的特定审查：

- **Python**: PEP 8 规范、类型提示、异常处理
- **JavaScript/TypeScript**: ES6+ 特性、类型安全、异步处理
- **Java**: 设计模式、内存管理、异常处理
- **C++**: 内存安全、RAII、现代 C++ 特性
- **Go**: 并发安全、错误处理、性能优化
- **Rust**: 所有权、生命周期、内存安全

### 3. 自定义规则引擎

你可以通过修改 `.github/code-review/config.json` 来添加自定义审查规则：

```json
{
  "name": "custom_rule",
  "description": "自定义规则描述",
  "severity": "warning",
  "pattern": "your_regex_pattern",
  "suggestion": "改进建议"
}
```

## 🚨 故障排除

### 常见问题

1. **API 密钥错误**
   ```
   Error: Missing required environment variables: GOOGLE_API_KEY
   ```
   **解决方案**: 确保在 `.env` 文件中正确设置了 API 密钥

2. **GitHub 权限错误**
   ```
   Error: 403 Forbidden
   ```
   **解决方案**: 检查 GitHub token 是否有足够的权限

3. **网络连接问题**
   ```
   Error: Connection timeout
   ```
   **解决方案**: 检查网络连接，考虑使用代理

### 调试模式

启用详细日志输出：

```bash
export DEBUG=true
python code_review_bot.py <PR_NUMBER>
```

## 📈 性能优化

### 1. 批量处理

对于大型 PR，机器人会自动分批处理文件以避免 API 限制。

### 2. 缓存机制

机器人会缓存已分析的文件以提高性能。

### 3. 并行处理

支持并行分析多个文件以提高速度。

## 🔒 安全考虑

- API 密钥存储在环境变量中，不会提交到代码库
- 所有敏感信息都经过适当的脱敏处理
- 支持私有仓库的审查
- 遵循最小权限原则

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [LangChain](https://langchain.com/) - AI 应用开发框架
- [Google Gemini](https://ai.google.dev/) - AI 模型
- [GitHub API](https://docs.github.com/en/rest) - GitHub 集成

## 📚 相关文档

- **完整工作流程指南**: 查看 `WORKFLOW_GUIDE.md`
- **本地审查脚本**: 查看 `local_review.py`
- **测试脚本**: 查看 `test_bot.py`

---

**注意**: 这是一个概念验证项目，在生产环境中使用前请进行充分的测试和评估。
