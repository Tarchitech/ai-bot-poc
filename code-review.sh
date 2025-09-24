#!/bin/bash

# AI Code Review Bot - Convenience Script
# This script provides a convenient way to run local code review from the project root
# Usage: ./code-review.sh [base_branch] [options]

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to show usage
show_usage() {
    echo "🤖 AI Code Review Bot - Convenience Script"
    echo "=========================================="
    echo ""
    echo "Usage: $0 [base_branch] [options]"
    echo ""
    echo "Arguments:"
    echo "  base_branch          Base branch to compare against (default: main)"
    echo ""
    echo "Options:"
    echo "  --current-branch     Specify current branch (default: auto-detect)"
    echo "  --output, -o         Output file path"
    echo "  --format             Output format (markdown|json)"
    echo "  --config             Configuration file path"
    echo "  --include-uncommitted Include uncommitted changes (default: True)"
    echo "  --committed-only     Only review committed changes"
    echo "  --help, -h           Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 main                                    # Compare with main branch (includes uncommitted)"
    echo "  $0 develop --output review.md             # Save to specific file"
    echo "  $0 main --format json -o review.json      # JSON format output"
    echo "  $0 main --current-branch feature/auth     # Specify current branch"
    echo "  $0 main --committed-only                  # Only review committed changes"
    echo "  $0 main --include-uncommitted             # Explicitly include uncommitted changes"
    echo ""
    echo "Environment Variables:"
    echo "  GOOGLE_API_KEY       Google AI API key (required)"
    echo ""
    echo "For more information, see:"
    echo "  .github/code-review/README_CODE_REVIEW_BOT.md"
    echo "  .github/code-review/WORKFLOW_GUIDE.md"
}

# Function to check if we're in a git repository
check_git_repo() {
    if [ ! -d ".git" ]; then
        print_error "Not in a git repository"
        echo "Please run this script from a git repository root directory"
        exit 1
    fi
}

# Function to check if the local review script exists
check_local_review_script() {
    if [ ! -f ".github/code-review/local_review.py" ]; then
        print_error "Local review script not found"
        echo "Expected location: .github/code-review/local_review.py"
        echo "Please ensure the AI Code Review Bot is properly installed"
        exit 1
    fi
}

# Function to check API key
check_api_key() {
    if [ -z "$GOOGLE_API_KEY" ]; then
        print_error "GOOGLE_API_KEY environment variable not set"
        echo ""
        echo "Please set your Google AI API key:"
        echo "  export GOOGLE_API_KEY='your_api_key_here'"
        echo ""
        echo "To get an API key:"
        echo "  1. Visit https://aistudio.google.com/app/apikey"
        echo "  2. Create a new API key"
        echo "  3. Set it as an environment variable"
        echo ""
        echo "You can also create a .env file in the project root:"
        echo "  echo 'GOOGLE_API_KEY=your_api_key_here' > .env"
        echo "  source .env"
        exit 1
    fi
    
    # Validate API key format (basic check)
    if [[ ! "$GOOGLE_API_KEY" =~ ^[A-Za-z0-9_-]+$ ]]; then
        print_warning "API key format looks unusual"
        echo "Please verify your GOOGLE_API_KEY is correct"
    fi
}

# Function to check Python dependencies
check_dependencies() {
    print_info "Checking Python dependencies..."
    
    # Check if Python is available
    if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
        print_error "Python not found"
        echo "Please install Python 3.8 or higher"
        exit 1
    fi
    
    # Determine Python command
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    else
        PYTHON_CMD="python"
    fi
    
    # Check if required packages are installed
    local missing_packages=()
    
    # Check for langchain
    if ! $PYTHON_CMD -c "import langchain" 2>/dev/null; then
        missing_packages+=("langchain")
    fi
    
    # Check for requests
    if ! $PYTHON_CMD -c "import requests" 2>/dev/null; then
        missing_packages+=("requests")
    fi
    
    # Check for python-dotenv
    if ! $PYTHON_CMD -c "import dotenv" 2>/dev/null; then
        missing_packages+=("python-dotenv")
    fi
    
    if [ ${#missing_packages[@]} -gt 0 ]; then
        print_warning "Missing Python packages: ${missing_packages[*]}"
        echo ""
        echo "To install missing packages:"
        echo "  pip install -r .github/code-review/requirements.txt"
        echo ""
        echo "Or install individually:"
        for package in "${missing_packages[@]}"; do
            echo "  pip install $package"
        done
        echo ""
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    else
        print_success "All required dependencies are installed"
    fi
}

# Function to get current branch
get_current_branch() {
    local current_branch
    current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
    echo "$current_branch"
}

# Function to check if base branch exists
check_base_branch() {
    local base_branch="$1"
    
    if ! git show-ref --verify --quiet "refs/heads/$base_branch" && ! git show-ref --verify --quiet "refs/remotes/origin/$base_branch"; then
        print_warning "Base branch '$base_branch' not found locally"
        echo "Available branches:"
        git branch -a 2>/dev/null | head -10
        echo ""
        echo "Trying to fetch from remote..."
        if git fetch origin "$base_branch" 2>/dev/null; then
            print_success "Successfully fetched $base_branch from remote"
        else
            print_error "Could not find or fetch base branch '$base_branch'"
            echo "Please check the branch name or create the branch first"
            exit 1
        fi
    fi
}

# Function to show repository info
show_repo_info() {
    local base_branch="$1"
    local current_branch
    current_branch=$(get_current_branch)
    
    print_info "Repository Information:"
    echo "  Repository: $(git remote get-url origin 2>/dev/null || echo 'No remote')"
    echo "  Current branch: $current_branch"
    echo "  Base branch: $base_branch"
    echo "  Working directory: $(pwd)"
    echo ""
}

# Function to show changes summary
show_changes_summary() {
    local base_branch="$1"
    local include_uncommitted="$2"
    local current_branch
    current_branch=$(get_current_branch)
    
    print_info "Changes Summary:"
    
    # Count changed files
    local changed_files=0
    local stats=""
    
    if [ "$include_uncommitted" = "true" ]; then
        # Include uncommitted changes
        local committed_files
        committed_files=$(git diff --name-only "$base_branch...$current_branch" 2>/dev/null | wc -l)
        
        local staged_files
        staged_files=$(git diff --name-only --cached 2>/dev/null | wc -l)
        
        local working_files
        working_files=$(git diff --name-only 2>/dev/null | wc -l)
        
        local untracked_files
        untracked_files=$(git ls-files --others --exclude-standard 2>/dev/null | wc -l)
        
        changed_files=$((committed_files + staged_files + working_files + untracked_files))
        
        # Get combined stats
        local committed_stats
        committed_stats=$(git diff --shortstat "$base_branch...$current_branch" 2>/dev/null || echo "")
        
        local staged_stats
        staged_stats=$(git diff --shortstat --cached 2>/dev/null || echo "")
        
        local working_stats
        working_stats=$(git diff --shortstat 2>/dev/null || echo "")
        
        echo "  Committed changes: $committed_files files"
        echo "  Staged changes: $staged_files files"
        echo "  Working directory changes: $working_files files"
        echo "  Untracked files: $untracked_files files"
        echo "  Total files changed: $changed_files"
        
        if [ -n "$committed_stats" ]; then
            echo "  Committed: $committed_stats"
        fi
        if [ -n "$staged_stats" ]; then
            echo "  Staged: $staged_stats"
        fi
        if [ -n "$working_stats" ]; then
            echo "  Working: $working_stats"
        fi
        if [ "$untracked_files" -gt 0 ]; then
            echo "  Untracked: $untracked_files new files"
        fi
    else
        # Only committed changes
        changed_files=$(git diff --name-only "$base_branch...$current_branch" 2>/dev/null | wc -l)
        stats=$(git diff --shortstat "$base_branch...$current_branch" 2>/dev/null || echo "0 files changed")
        echo "  Files changed: $changed_files"
        echo "  Changes: $stats"
    fi
    
    if [ "$changed_files" -eq 0 ]; then
        print_warning "No changes found between $base_branch and $current_branch"
        if [ "$include_uncommitted" = "true" ]; then
            echo "Try running with --committed-only if you want to review only committed changes."
        fi
        echo "The review will show no issues."
    fi
    echo ""
}

# Main function
main() {
    # Parse arguments
    local base_branch="main"
    local args=()
    local include_uncommitted="true"
    
    # Handle help
    if [[ "$1" == "--help" || "$1" == "-h" ]]; then
        show_usage
        exit 0
    fi
    
    # Set base branch if provided and not an option
    if [[ -n "$1" && ! "$1" =~ ^-- ]]; then
        base_branch="$1"
        shift
    fi
    
    # Check for uncommitted changes options
    local temp_args=()
    for arg in "$@"; do
        case "$arg" in
            --committed-only)
                include_uncommitted="false"
                temp_args+=("$arg")
                ;;
            --include-uncommitted)
                include_uncommitted="true"
                temp_args+=("$arg")
                ;;
            *)
                temp_args+=("$arg")
                ;;
        esac
    done
    
    # Pass remaining arguments to the Python script
    args=("${temp_args[@]}")
    
    # Show header
    echo "🤖 AI Code Review Bot"
    echo "===================="
    echo ""
    
    # Run checks
    check_git_repo
    check_local_review_script
    check_api_key
    check_dependencies
    check_base_branch "$base_branch"
    
    # Show information
    show_repo_info "$base_branch"
    show_changes_summary "$base_branch" "$include_uncommitted"
    
    # Determine Python command
    local python_cmd
    if command -v python3 &> /dev/null; then
        python_cmd="python3"
    else
        python_cmd="python"
    fi
    
    # Build command
    local cmd=("$python_cmd" ".github/code-review/local_review.py" "$base_branch" "${args[@]}")
    
    print_info "Running code review..."
    echo "Command: ${cmd[*]}"
    echo ""
    
    # Run the local review script
    if "${cmd[@]}"; then
        echo ""
        print_success "Code review completed successfully!"
        echo ""
        echo "📋 Next steps:"
        echo "  1. Review the generated report"
        echo "  2. Fix any critical issues found"
        echo "  3. Commit your changes: git add . && git commit -m 'fix: address review issues'"
        echo "  4. Push to remote: git push origin $(get_current_branch)"
        echo "  5. Create Pull Request on GitHub"
        echo "  6. GitHub Actions will automatically run additional review"
    else
        print_error "Code review failed"
        echo "Please check the error messages above and try again"
        exit 1
    fi
}

# Run main function with all arguments
main "$@"
