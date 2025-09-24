#!/bin/bash

# AI Code Review Bot - Demo Workflow Script
# This script demonstrates the complete workflow from local review to PR creation

echo "🚀 AI Code Review Bot - Demo Workflow"
echo "======================================"
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository"
    echo "Please run this script from a git repository root"
    exit 1
fi

# Check if Google API key is set
if [ -z "$GOOGLE_API_KEY" ]; then
    echo "⚠️  Warning: GOOGLE_API_KEY not set"
    echo "Please set your Google AI API key:"
    echo "  export GOOGLE_API_KEY='your_api_key_here'"
    echo ""
    echo "For demo purposes, we'll continue without AI review..."
    DEMO_MODE=true
else
    DEMO_MODE=false
fi

echo "📋 Current Repository Status:"
echo "  Repository: $(git remote get-url origin 2>/dev/null || echo 'No remote')"
echo "  Current branch: $(git rev-parse --abbrev-ref HEAD)"
echo "  Base branch: main"
echo ""

# Step 1: Check current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" = "main" ]; then
    echo "⚠️  You're currently on the main branch"
    echo "Creating a demo feature branch..."
    git checkout -b demo-feature-$(date +%s) 2>/dev/null || echo "Could not create branch"
    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
fi

echo "🌿 Working on branch: $CURRENT_BRANCH"
echo ""

# Step 2: Show what files have changed
echo "📁 Files changed since main:"
git diff --name-only main...HEAD 2>/dev/null || echo "  No changes found"
echo ""

# Step 3: Run local review
if [ "$DEMO_MODE" = false ]; then
    echo "🔍 Running local code review..."
    echo "Command: python .github/code-review/local_review.py main"
    echo ""
    
    # Check if the script exists
    if [ -f ".github/code-review/local_review.py" ]; then
        python .github/code-review/local_review.py main --output demo_review.md
        echo "✅ Local review completed!"
        echo "📄 Review report saved to: demo_review.md"
        
        if [ -f "demo_review.md" ]; then
            echo ""
            echo "📊 Review Summary:"
            echo "=================="
            head -20 demo_review.md
            echo ""
            echo "📄 Full report available in: demo_review.md"
        fi
    else
        echo "❌ Local review script not found"
        echo "Please ensure .github/code-review/local_review.py exists"
    fi
else
    echo "🎭 Demo Mode: Simulating local review..."
    echo "✅ Local review completed (simulated)"
    echo "📄 Review report would be saved to: demo_review.md"
fi

echo ""
echo "📋 Next Steps:"
echo "=============="
echo "1. ✅ Local review completed"
echo "2. 🔄 Fix any issues found in the review"
echo "3. 📝 Commit your changes:"
echo "   git add ."
echo "   git commit -m 'feat: implement new feature'"
echo "4. 🚀 Push to remote:"
echo "   git push origin $CURRENT_BRANCH"
echo "5. 📋 Create Pull Request on GitHub"
echo "6. 🤖 GitHub Actions will automatically run AI review"
echo ""

# Step 4: Show GitHub Actions workflow info
echo "🔧 GitHub Actions Configuration:"
echo "==============================="
echo "The following workflows will be triggered on PR creation:"
echo ""
echo "1. 🤖 AI Code Review (.github/workflows/ai-code-review.yml)"
echo "   - Automatically reviews PR code"
echo "   - Posts review comments"
echo "   - Provides security and quality analysis"
echo ""
echo "2. 🔍 Local Review Check (.github/workflows/local-review-check.yml)"
echo "   - Checks for local review reports"
echo "   - Validates review quality"
echo "   - Suggests local review for new PRs"
echo ""

# Step 5: Show configuration requirements
echo "⚙️  Required Configuration:"
echo "=========================="
echo "GitHub Repository Secrets:"
echo "  - GOOGLE_API_KEY: Your Google AI API key"
echo "  - GITHUB_TOKEN: Automatically provided by GitHub"
echo ""

echo "Environment Variables (for local review):"
echo "  - GOOGLE_API_KEY: Your Google AI API key"
echo "  - GITHUB_TOKEN: Your GitHub personal access token (optional)"
echo ""

# Step 6: Show usage examples
echo "💡 Usage Examples:"
echo "=================="
echo ""
echo "Local Review:"
echo "  python .github/code-review/local_review.py main"
echo "  python .github/code-review/local_review.py main --output my_review.md"
echo "  python .github/code-review/local_review.py main --format json"
echo ""
echo "Remote Review (manual):"
echo "  python .github/code-review/code_review_bot.py <PR_NUMBER>"
echo ""

echo "🎉 Demo workflow completed!"
echo "=========================="
echo ""
echo "For more information, see:"
echo "  - .github/code-review/README_CODE_REVIEW_BOT.md"
echo "  - .github/code-review/WORKFLOW_GUIDE.md"
echo ""
echo "Happy coding! 🚀"
