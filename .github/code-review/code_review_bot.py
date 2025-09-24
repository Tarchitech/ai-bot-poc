#!/usr/bin/env python3
"""
AI Code Review Bot for GitHub Pull Requests

This bot automatically reviews code changes in pull requests using AI
and provides feedback based on predefined rules.

Setup Instructions:
1. Install required dependencies:
   pip install langchain langchain_community langchain-google-genai requests python-dotenv

2. Set up environment variables:
   - GITHUB_TOKEN: Your GitHub personal access token
   - GOOGLE_API_KEY: Your Google AI API key
   - REPO_OWNER: GitHub repository owner
   - REPO_NAME: GitHub repository name

3. Configure review rules in config.json

Usage:
   python code_review_bot.py <pr_number>
"""

import os
import sys
import json
import requests
import argparse
from typing import List, Dict, Any
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import LangChain components
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage

@dataclass
class CodeReviewRule:
    """Represents a code review rule"""
    name: str
    description: str
    severity: str  # 'error', 'warning', 'info'
    pattern: str
    suggestion: str

@dataclass
class CodeReviewResult:
    """Represents the result of a code review"""
    file_path: str
    line_number: int
    rule_name: str
    severity: str
    message: str
    suggestion: str

class GitHubAPIClient:
    """Client for interacting with GitHub API"""
    
    def __init__(self, token: str, owner: str, repo: str):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.base_url = f"https://api.github.com/repos/{owner}/{repo}"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def get_pr_diff(self, pr_number: int) -> str:
        """Get the diff for a pull request"""
        url = f"{self.base_url}/pulls/{pr_number}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        # Get the diff URL
        pr_data = response.json()
        diff_url = pr_data["diff_url"]
        
        # Fetch the actual diff
        diff_response = requests.get(diff_url, headers=self.headers)
        diff_response.raise_for_status()
        
        return diff_response.text
    
    def get_pr_files(self, pr_number: int) -> List[Dict[str, Any]]:
        """Get the list of files changed in a pull request"""
        url = f"{self.base_url}/pulls/{pr_number}/files"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def post_comment(self, pr_number: int, comment: str) -> None:
        """Post a comment to a pull request"""
        url = f"{self.base_url}/issues/{pr_number}/comments"
        data = {"body": comment}
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()

class CodeReviewBot:
    """AI-powered code review bot"""
    
    def __init__(self, github_client: GitHubAPIClient):
        self.github_client = github_client
        self.llm = GoogleGenerativeAI(model="models/gemini-2.5-pro")
        self.rules = self._load_review_rules()
    
    def _load_review_rules(self) -> List[CodeReviewRule]:
        """Load code review rules from configuration"""
        try:
            with open(".github/code-review/config.json", "r") as f:
                config = json.load(f)
            
            rules = []
            for rule_config in config.get("rules", []):
                rule = CodeReviewRule(
                    name=rule_config["name"],
                    description=rule_config["description"],
                    severity=rule_config["severity"],
                    pattern=rule_config["pattern"],
                    suggestion=rule_config["suggestion"]
                )
                rules.append(rule)
            
            return rules
        except FileNotFoundError:
            print("Warning: .github/code-review/config.json not found. Using default rules.")
            return self._get_default_rules()
    
    def _get_default_rules(self) -> List[CodeReviewRule]:
        """Get default code review rules"""
        return [
            CodeReviewRule(
                name="security_check",
                description="Check for potential security vulnerabilities",
                severity="error",
                pattern="password|secret|key|token",
                suggestion="Consider using environment variables or secure storage for sensitive data"
            ),
            CodeReviewRule(
                name="performance_check",
                description="Check for performance issues",
                severity="warning",
                pattern="for.*in.*range|while.*True|sleep\\(|time\\.sleep",
                suggestion="Consider optimizing loops and avoiding blocking operations"
            ),
            CodeReviewRule(
                name="code_quality",
                description="Check for code quality issues",
                severity="info",
                pattern="TODO|FIXME|XXX|HACK",
                suggestion="Consider addressing technical debt markers"
            )
        ]
    
    def _create_review_prompt(self, diff: str, rules: List[CodeReviewRule]) -> str:
        """Create a prompt for AI code review"""
        rules_text = "\n".join([
            f"- {rule.name}: {rule.description} (Severity: {rule.severity})"
            for rule in rules
        ])
        
        prompt = f"""
You are an expert code reviewer. Please review the following code changes and provide feedback based on these rules:

RULES:
{rules_text}

CODE CHANGES:
{diff}

Please provide a comprehensive review that includes:
1. Overall assessment of the changes
2. Specific issues found (if any) with line numbers
3. Suggestions for improvement
4. Security considerations
5. Performance implications
6. Code quality observations

Format your response as:
## Code Review Summary
[Overall assessment]

## Issues Found
- **File**: [filename]
  - **Line**: [line number]
  - **Issue**: [description]
  - **Severity**: [error/warning/info]
  - **Suggestion**: [how to fix]

## Recommendations
[General recommendations for improvement]
"""
        return prompt
    
    def review_pr(self, pr_number: int) -> List[CodeReviewResult]:
        """Review a pull request and return results"""
        print(f"Reviewing PR #{pr_number}...")
        
        # Get PR diff and files
        diff = self.github_client.get_pr_diff(pr_number)
        files = self.github_client.get_pr_files(pr_number)
        
        print(f"Found {len(files)} changed files")
        
        # Create AI review prompt
        prompt = self._create_review_prompt(diff, self.rules)
        
        # Get AI review
        print("Getting AI review...")
        ai_review = self.llm.invoke(prompt)
        
        # Parse AI review and create results
        results = self._parse_ai_review(ai_review, files)
        
        return results
    
    def _parse_ai_review(self, ai_review: str, files: List[Dict[str, Any]]) -> List[CodeReviewResult]:
        """Parse AI review response into structured results"""
        results = []
        
        # Simple parsing - in a real implementation, you'd want more sophisticated parsing
        lines = ai_review.split('\n')
        current_file = None
        
        for line in lines:
            if line.startswith('**File**:'):
                current_file = line.split('**File**:')[1].strip()
            elif line.startswith('- **Line**:'):
                line_num = int(line.split('**Line**:')[1].strip())
                # Extract issue details from subsequent lines
                issue_line = lines[lines.index(line) + 1] if lines.index(line) + 1 < len(lines) else ""
                suggestion_line = lines[lines.index(line) + 2] if lines.index(line) + 2 < len(lines) else ""
                
                result = CodeReviewResult(
                    file_path=current_file or "unknown",
                    line_number=line_num,
                    rule_name="ai_review",
                    severity="info",
                    message=issue_line.replace('- **Issue**:', '').strip(),
                    suggestion=suggestion_line.replace('- **Suggestion**:', '').strip()
                )
                results.append(result)
        
        return results
    
    def post_review_comments(self, pr_number: int, results: List[CodeReviewResult]) -> None:
        """Post review comments to the pull request"""
        if not results:
            comment = "✅ **AI Code Review Complete**\n\nNo issues found! Great work!"
        else:
            comment = "🤖 **AI Code Review Results**\n\n"
            
            # Group results by severity
            errors = [r for r in results if r.severity == "error"]
            warnings = [r for r in results if r.severity == "warning"]
            infos = [r for r in results if r.severity == "info"]
            
            if errors:
                comment += "## ❌ Errors Found\n"
                for result in errors:
                    comment += f"- **{result.file_path}:{result.line_number}** - {result.message}\n"
                    if result.suggestion:
                        comment += f"  💡 *Suggestion*: {result.suggestion}\n"
                comment += "\n"
            
            if warnings:
                comment += "## ⚠️ Warnings\n"
                for result in warnings:
                    comment += f"- **{result.file_path}:{result.line_number}** - {result.message}\n"
                    if result.suggestion:
                        comment += f"  💡 *Suggestion*: {result.suggestion}\n"
                comment += "\n"
            
            if infos:
                comment += "## ℹ️ Suggestions\n"
                for result in infos:
                    comment += f"- **{result.file_path}:{result.line_number}** - {result.message}\n"
                    if result.suggestion:
                        comment += f"  💡 *Suggestion*: {result.suggestion}\n"
        
        self.github_client.post_comment(pr_number, comment)
        print(f"Posted review comment to PR #{pr_number}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="AI Code Review Bot")
    parser.add_argument("pr_number", type=int, help="Pull request number to review")
    parser.add_argument("--config", default=".github/code-review/config.json", help="Configuration file path")
    
    args = parser.parse_args()
    
    # Check environment variables
    required_vars = ["GITHUB_TOKEN", "GOOGLE_API_KEY", "REPO_OWNER", "REPO_NAME"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
        print("\nPlease set the following environment variables:")
        for var in missing_vars:
            print(f"  export {var}='your_value_here'")
        sys.exit(1)
    
    # Initialize clients
    github_client = GitHubAPIClient(
        token=os.getenv("GITHUB_TOKEN"),
        owner=os.getenv("REPO_OWNER"),
        repo=os.getenv("REPO_NAME")
    )
    
    review_bot = CodeReviewBot(github_client)
    
    try:
        # Review the PR
        results = review_bot.review_pr(args.pr_number)
        
        # Post comments
        review_bot.post_review_comments(args.pr_number, results)
        
        print(f"✅ Code review completed for PR #{args.pr_number}")
        print(f"Found {len(results)} issues")
        
    except Exception as e:
        print(f"❌ Error during code review: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
