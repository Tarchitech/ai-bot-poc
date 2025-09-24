#!/usr/bin/env python3
"""
Local Code Review Bot

This script allows developers to perform code review locally before raising a PR.
It compares the current branch with the base branch (e.g., main) and generates
a comprehensive code review report.

Usage:
    python local_review.py [base_branch] [--output OUTPUT_FILE] [--format FORMAT]

Examples:
    python local_review.py main
    python local_review.py develop --output review_report.md
    python local_review.py main --format json
"""

import os
import sys
import json
import argparse
import subprocess
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

# Import our existing modules
from diff_analyzer import DiffAnalyzer
from review_prompts import ReviewPromptManager
from code_review_bot import CodeReviewBot

@dataclass
class ReviewReport:
    """Represents a local code review report"""
    timestamp: str
    base_branch: str
    current_branch: str
    files_changed: List[str]
    total_additions: int
    total_deletions: int
    summary: Dict[str, Any]
    detailed_review: str
    recommendations: List[str]
    risk_factors: List[str]

class LocalCodeReviewer:
    """Local code reviewer that compares branches"""
    
    def __init__(self, config_path: str = ".github/code-review/config.json"):
        self.config_path = config_path
        self.diff_analyzer = DiffAnalyzer()
        self.prompt_manager = ReviewPromptManager()
        self.load_config()
    
    def load_config(self):
        """Load configuration from config file"""
        try:
            with open(self.config_path, "r") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            print(f"Warning: {self.config_path} not found. Using default settings.")
            self.config = {
                "ai_settings": {
                    "model": "models/gemini-2.5-pro",
                    "temperature": 0.1,
                    "max_tokens": 2000
                },
                "review_settings": {
                    "max_files_per_review": 50,
                    "max_lines_per_file": 1000,
                    "skip_files": ["*.min.js", "*.min.css", "*.lock"],
                    "focus_languages": ["python", "javascript", "typescript", "java", "cpp", "c", "go", "rust"]
                }
            }
    
    def get_current_branch(self) -> str:
        """Get the current git branch name"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return "unknown"
    
    def get_diff(self, base_branch: str, current_branch: str, include_uncommitted: bool = True) -> str:
        """Get the diff between two branches, optionally including uncommitted changes"""
        try:
            if include_uncommitted:
                diff_parts = []
                
                # 1. Get committed changes between branches
                try:
                    result = subprocess.run(
                        ["git", "diff", f"{base_branch}...{current_branch}", "--", "."],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    if result.stdout.strip():
                        diff_parts.append(result.stdout)
                except subprocess.CalledProcessError:
                    pass
                
                # 2. Get staged changes
                try:
                    staged_result = subprocess.run(
                        ["git", "diff", "--cached"],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    if staged_result.stdout.strip():
                        diff_parts.append(staged_result.stdout)
                except subprocess.CalledProcessError:
                    pass
                
                # 3. Get working directory changes
                try:
                    working_result = subprocess.run(
                        ["git", "diff"],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    if working_result.stdout.strip():
                        diff_parts.append(working_result.stdout)
                except subprocess.CalledProcessError:
                    pass
                
                # 4. Get untracked files as "new file" diffs
                try:
                    untracked_result = subprocess.run(
                        ["git", "ls-files", "--others", "--exclude-standard"],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    untracked_files = untracked_result.stdout.strip().split('\n')
                    untracked_files = [f for f in untracked_files if f.strip()]
                    
                    if untracked_files:
                        # Create a diff-like representation for untracked files
                        untracked_diff = ""
                        for file_path in untracked_files:
                            try:
                                # Read the file content
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                
                                # Create a diff-like format
                                untracked_diff += f"diff --git a/{file_path} b/{file_path}\n"
                                untracked_diff += f"new file mode 100644\n"
                                untracked_diff += f"index 0000000..{hash(content) % 1000000:07x}\n"
                                untracked_diff += f"--- /dev/null\n"
                                untracked_diff += f"+++ b/{file_path}\n"
                                
                                # Add content with + prefix
                                for line in content.split('\n'):
                                    untracked_diff += f"+{line}\n"
                                untracked_diff += "\n"
                            except (UnicodeDecodeError, PermissionError, FileNotFoundError):
                                # Skip binary files or files we can't read
                                untracked_diff += f"diff --git a/{file_path} b/{file_path}\n"
                                untracked_diff += f"new file mode 100644\n"
                                untracked_diff += f"index 0000000..0000000\n"
                                untracked_diff += f"--- /dev/null\n"
                                untracked_diff += f"+++ b/{file_path}\n"
                                untracked_diff += f"+[Binary file or unreadable]\n\n"
                        
                        if untracked_diff.strip():
                            diff_parts.append(untracked_diff)
                except subprocess.CalledProcessError:
                    pass
                
                # Combine all diff parts
                return "\n".join(diff_parts) if diff_parts else ""
            else:
                # Only committed changes
                result = subprocess.run(
                    ["git", "diff", f"{base_branch}...{current_branch}"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error getting diff: {e}")
            return ""
    
    def get_changed_files(self, base_branch: str, current_branch: str, include_uncommitted: bool = True) -> List[str]:
        """Get list of changed files between branches, optionally including uncommitted changes"""
        try:
            files = set()
            
            if include_uncommitted:
                # Get committed changes
                try:
                    result = subprocess.run(
                        ["git", "diff", "--name-only", f"{base_branch}...{current_branch}"],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    committed_files = result.stdout.strip().split('\n')
                    files.update(f for f in committed_files if f.strip())
                except subprocess.CalledProcessError:
                    pass
                
                # Get staged changes
                try:
                    staged_result = subprocess.run(
                        ["git", "diff", "--name-only", "--cached"],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    staged_files = staged_result.stdout.strip().split('\n')
                    files.update(f for f in staged_files if f.strip())
                except subprocess.CalledProcessError:
                    pass
                
                # Get working directory changes
                try:
                    working_result = subprocess.run(
                        ["git", "diff", "--name-only"],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    working_files = working_result.stdout.strip().split('\n')
                    files.update(f for f in working_files if f.strip())
                except subprocess.CalledProcessError:
                    pass
                
                # Get untracked files
                try:
                    untracked_result = subprocess.run(
                        ["git", "ls-files", "--others", "--exclude-standard"],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    untracked_files = untracked_result.stdout.strip().split('\n')
                    files.update(f for f in untracked_files if f.strip())
                except subprocess.CalledProcessError:
                    pass
            else:
                # Only committed changes
                result = subprocess.run(
                    ["git", "diff", "--name-only", f"{base_branch}...{current_branch}"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                committed_files = result.stdout.strip().split('\n')
                files.update(f for f in committed_files if f.strip())
            
            return list(files)
        except subprocess.CalledProcessError:
            return []
    
    def filter_files(self, files: List[str]) -> List[str]:
        """Filter files based on configuration"""
        skip_patterns = self.config.get("review_settings", {}).get("skip_files", [])
        focus_languages = self.config.get("review_settings", {}).get("focus_languages", [])
        
        filtered_files = []
        for file in files:
            # Skip files matching skip patterns
            should_skip = False
            for pattern in skip_patterns:
                if pattern.startswith("*."):
                    ext = pattern[1:]  # Remove the *
                    if file.endswith(ext):
                        should_skip = True
                        break
                elif pattern in file:
                    should_skip = True
                    break
            
            if should_skip:
                continue
            
            # Check if file is in focus languages
            file_ext = os.path.splitext(file)[1]
            if focus_languages:
                language_extensions = {
                    'python': ['.py'],
                    'javascript': ['.js', '.jsx'],
                    'typescript': ['.ts', '.tsx'],
                    'java': ['.java'],
                    'cpp': ['.cpp', '.cc', '.cxx', '.hpp', '.h'],
                    'c': ['.c'],
                    'go': ['.go'],
                    'rust': ['.rs']
                }
                
                file_language = None
                for lang, exts in language_extensions.items():
                    if file_ext in exts:
                        file_language = lang
                        break
                
                if file_language and file_language in focus_languages:
                    filtered_files.append(file)
            else:
                filtered_files.append(file)
        
        return filtered_files
    
    def generate_ai_review(self, diff: str, files: List[str]) -> str:
        """Generate AI-powered code review"""
        try:
            # Import Google AI components
            from langchain_google_genai import GoogleGenerativeAI
            
            # Initialize LLM
            llm = GoogleGenerativeAI(
                model=self.config["ai_settings"]["model"],
                temperature=self.config["ai_settings"]["temperature"],
                max_output_tokens=self.config["ai_settings"]["max_tokens"]
            )
            
            # Get security prompt (highest priority)
            security_prompt = self.prompt_manager.get_prompt_by_name("security")
            
            # Create comprehensive review prompt
            files_text = "\n".join([f"- {file}" for file in files])
            
            prompt = f"""
You are an expert code reviewer conducting a comprehensive review of the following changes.

FILES CHANGED:
{files_text}

CODE CHANGES:
{diff}

Please provide a detailed code review focusing on:

1. **Security Analysis**
   - Authentication and authorization issues
   - Input validation problems
   - Data protection concerns
   - SQL injection vulnerabilities
   - XSS and other web vulnerabilities

2. **Performance Issues**
   - Algorithm efficiency
   - Memory usage
   - Database query optimization
   - Network operations
   - Caching opportunities

3. **Code Quality**
   - Code structure and organization
   - Readability and maintainability
   - Error handling
   - Testing coverage
   - Documentation

4. **Best Practices**
   - Language-specific best practices
   - Design patterns
   - Code standards compliance
   - Technical debt

Format your response as:

## 🔍 Code Review Summary
[Overall assessment of the changes]

## 🚨 Critical Issues
- **File**: [filename]
  - **Line**: [line number]
  - **Issue**: [specific problem]
  - **Risk**: [explanation of risk]
  - **Fix**: [specific solution]

## ⚠️ Warnings
[High and medium priority issues]

## 💡 Recommendations
[General improvement suggestions]

## 📊 Metrics
- Files changed: {len(files)}
- Estimated complexity change: [assessment]
- Risk level: [Low/Medium/High/Critical]
"""
            
            # Generate review
            review = llm.invoke(prompt)
            return review
            
        except Exception as e:
            return f"Error generating AI review: {e}"
    
    def apply_rules(self, diff: str, files: List[str]) -> List[dict]:
        """Apply configured rules to detect issues with detailed information"""
        issues = []
        rules = self.config.get("rules", [])
        
        # Read file contents for rule matching
        file_contents = {}
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_contents[file_path] = f.read()
            except (UnicodeDecodeError, PermissionError, FileNotFoundError):
                # Skip binary files or files we can't read
                continue
        
        # Apply each rule
        for rule in rules:
            rule_name = rule['name']
            pattern = rule['pattern']
            severity = rule['severity']
            description = rule['description']
            suggestion = rule['suggestion']
            
            import re
            rule_issues = []
            
            # Check individual files for detailed information
            for file_path, content in file_contents.items():
                lines = content.split('\n')
                for line_num, line in enumerate(lines, 1):
                    if re.search(pattern, line, re.IGNORECASE):
                        # Extract the matching part
                        match = re.search(pattern, line, re.IGNORECASE)
                        matched_text = match.group(0) if match else line.strip()
                        
                        rule_issues.append({
                            'file': file_path,
                            'line': line_num,
                            'code': line.strip(),
                            'matched_text': matched_text,
                            'rule': rule_name,
                            'severity': severity,
                            'description': description,
                            'suggestion': suggestion
                        })
            
            # Add rule summary if any issues found
            if rule_issues:
                issues.extend(rule_issues)
        
        return issues
    
    def generate_detailed_review(self, rule_issues: List[dict], ai_review: str) -> str:
        """Generate detailed review text with specific issue locations"""
        if not rule_issues:
            return ai_review if ai_review else "No issues found."
        
        # Group issues by severity
        critical_issues = [i for i in rule_issues if i['severity'] == 'error']
        warning_issues = [i for i in rule_issues if i['severity'] == 'warning']
        info_issues = [i for i in rule_issues if i['severity'] == 'info']
        
        detailed_text = []
        
        # Add AI review if available
        if ai_review and not ai_review.startswith("Error generating AI review"):
            detailed_text.append("## 🤖 AI Review")
            detailed_text.append(ai_review)
            detailed_text.append("")
        
        # Add rule-based analysis
        detailed_text.append("## 🔍 Rule-Based Analysis")
        detailed_text.append("")
        
        if critical_issues:
            detailed_text.append("### 🚨 Critical Issues")
            detailed_text.append("")
            for issue in critical_issues:  # Show all critical issues
                issue_text = f"**File**: `{issue['file']}`<br>\n**Line**: {issue['line']}<br>\n**Issue**: {issue['description']}<br>\n**Code**: `{issue['code']}`<br>\n**Suggestion**: {issue['suggestion']}"
                detailed_text.append(issue_text)
                detailed_text.append("")  # Empty line separator between issues
        
        if warning_issues:
            detailed_text.append("### ⚠️ Warnings")
            detailed_text.append("")
            for issue in warning_issues[:10]:  # Limit to first 10 for readability
                issue_text = f"**File**: `{issue['file']}`<br>\n**Line**: {issue['line']}<br>\n**Issue**: {issue['description']}<br>\n**Code**: `{issue['code']}`<br>\n**Suggestion**: {issue['suggestion']}"
                detailed_text.append(issue_text)
                detailed_text.append("")  # Empty line separator between issues
        
        if info_issues:
            detailed_text.append("### ℹ️ Information")
            detailed_text.append("")
            for issue in info_issues[:10]:  # Limit to first 10 for readability
                issue_text = f"**File**: `{issue['file']}`<br>\n**Line**: {issue['line']}<br>\n**Issue**: {issue['description']}<br>\n**Code**: `{issue['code']}`<br>\n**Suggestion**: {issue['suggestion']}"
                detailed_text.append(issue_text)
                detailed_text.append("")  # Empty line separator between issues
        
        # Add summary
        total_issues = len(rule_issues)
        displayed_warning = min(len(warning_issues), 10)
        displayed_info = min(len(info_issues), 10)
        
        detailed_text.append("### 📊 Summary")
        detailed_text.append(f"- **Total Issues Found**: {total_issues}")
        detailed_text.append(f"- **Critical Issues**: {len(critical_issues)} (showing all)")
        detailed_text.append(f"- **Warning Issues**: {len(warning_issues)} (showing {displayed_warning})")
        detailed_text.append(f"- **Info Issues**: {len(info_issues)} (showing {displayed_info})")
        
        # Add note about truncation if there are more issues
        if len(warning_issues) > 10 or len(info_issues) > 10:
            detailed_text.append("")
            detailed_text.append("> **Note**: All critical issues are shown. Warning and info issues are limited to 10 for readability.")
        
        return "\n".join(detailed_text)
    
    def perform_review(self, base_branch: str, current_branch: Optional[str] = None, include_uncommitted: bool = True) -> ReviewReport:
        """Perform comprehensive code review"""
        if current_branch is None:
            current_branch = self.get_current_branch()
        
        print(f"🔍 Starting code review...")
        print(f"📊 Comparing: {base_branch} → {current_branch}")
        
        if include_uncommitted:
            print("📝 Including uncommitted changes in working directory")
        
        # Get diff and changed files
        diff = self.get_diff(base_branch, current_branch, include_uncommitted)
        all_files = self.get_changed_files(base_branch, current_branch, include_uncommitted)
        filtered_files = self.filter_files(all_files)
        
        if not diff:
            print("❌ No differences found between branches")
            return ReviewReport(
                timestamp=datetime.now().isoformat(),
                base_branch=base_branch,
                current_branch=current_branch,
                files_changed=[],
                total_additions=0,
                total_deletions=0,
                summary={},
                detailed_review="No changes found between branches.",
                recommendations=[],
                risk_factors=[]
            )
        
        print(f"📁 Found {len(all_files)} changed files")
        print(f"🎯 Reviewing {len(filtered_files)} files (after filtering)")
        
        # Analyze diff
        analyses = self.diff_analyzer.analyze_diff(diff)
        summary = self.diff_analyzer.generate_summary(analyses)
        
        # Apply rule-based analysis first
        print("🔍 Applying rule-based analysis...")
        rule_issues = self.apply_rules(diff, filtered_files)
        
        # Generate AI review
        print("🤖 Generating AI review...")
        ai_review = self.generate_ai_review(diff, filtered_files)
        
        # Extract recommendations and risk factors
        recommendations = []
        risk_factors = []
        
        # Add rule-based issues to recommendations and risk factors
        for issue in rule_issues:
            if issue['severity'] == 'error':
                risk_factors.append(f"{issue['rule']}: {issue['description']}")
            else:
                recommendations.append(f"{issue['rule']}: {issue['description']}")
        
        # Generate detailed review text
        detailed_review = self.generate_detailed_review(rule_issues, ai_review)
        
        for analysis in analyses:
            recommendations.extend(analysis.suggestions)
            risk_factors.extend(analysis.risk_factors)
        
        return ReviewReport(
            timestamp=datetime.now().isoformat(),
            base_branch=base_branch,
            current_branch=current_branch,
            files_changed=filtered_files,
            total_additions=summary["summary"]["total_additions"],
            total_deletions=summary["summary"]["total_deletions"],
            summary=summary,
            detailed_review=detailed_review,
            recommendations=list(set(recommendations)),
            risk_factors=list(set(risk_factors))
        )
    
    def save_report(self, report: ReviewReport, output_file: str, format: str = "markdown"):
        """Save review report to file"""
        if format.lower() == "json":
            # Save as JSON
            report_dict = {
                "timestamp": report.timestamp,
                "base_branch": report.base_branch,
                "current_branch": report.current_branch,
                "files_changed": report.files_changed,
                "total_additions": report.total_additions,
                "total_deletions": report.total_deletions,
                "summary": report.summary,
                "detailed_review": report.detailed_review,
                "recommendations": report.recommendations,
                "risk_factors": report.risk_factors
            }
            
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(report_dict, f, indent=2, ensure_ascii=False)
        
        else:
            # Save as Markdown
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(f"# Code Review Report\n\n")
                f.write(f"**Generated**: {report.timestamp}\n")
                f.write(f"**Branch Comparison**: {report.base_branch} → {report.current_branch}\n")
                f.write(f"**Files Changed**: {len(report.files_changed)}\n")
                f.write(f"**Additions**: {report.total_additions}\n")
                f.write(f"**Deletions**: {report.total_deletions}\n\n")
                
                f.write("## 📁 Changed Files\n\n")
                for file in report.files_changed:
                    f.write(f"- {file}\n")
                f.write("\n")
                
                f.write("## 🔍 Detailed Review\n\n")
                f.write(report.detailed_review)
                f.write("\n\n")
                
                if report.recommendations:
                    f.write("## 💡 Recommendations\n\n")
                    for rec in report.recommendations:
                        f.write(f"- {rec}\n")
                    f.write("\n")
                
                if report.risk_factors:
                    f.write("## ⚠️ Risk Factors\n\n")
                    for risk in report.risk_factors:
                        f.write(f"- {risk}\n")
                    f.write("\n")
        
        print(f"📄 Report saved to: {output_file}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Local Code Review Bot")
    parser.add_argument("base_branch", nargs="?", default="main", help="Base branch to compare against")
    parser.add_argument("--current-branch", help="Current branch (default: auto-detect)")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="Output format")
    parser.add_argument("--config", default=".github/code-review/config.json", help="Configuration file path")
    parser.add_argument("--include-uncommitted", action="store_true", default=True, help="Include uncommitted changes (default: True)")
    parser.add_argument("--committed-only", action="store_true", help="Only review committed changes")
    
    args = parser.parse_args()
    
    # Determine if we should include uncommitted changes
    include_uncommitted = args.include_uncommitted and not args.committed_only
    
    # Check if we're in a git repository
    if not os.path.exists(".git"):
        print("❌ Error: Not in a git repository")
        sys.exit(1)
    
    # Check for Google AI API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY environment variable not set")
        print("Please set your Google AI API key:")
        print("  export GOOGLE_API_KEY='your_api_key_here'")
        sys.exit(1)
    
    try:
        # Initialize reviewer
        reviewer = LocalCodeReviewer(args.config)
        
        # Perform review
        report = reviewer.perform_review(args.base_branch, args.current_branch, include_uncommitted)
        
        # Display summary
        print("\n" + "="*60)
        print("📊 REVIEW SUMMARY")
        print("="*60)
        print(f"Branch: {args.base_branch} → {report.current_branch}")
        print(f"Files: {len(report.files_changed)}")
        print(f"Changes: +{report.total_additions} -{report.total_deletions}")
        print(f"Risk Factors: {len(report.risk_factors)}")
        print(f"Recommendations: {len(report.recommendations)}")
        
        # Save report if output file specified
        if args.output:
            reviewer.save_report(report, args.output, args.format)
        else:
            # Default output file - sanitize branch name for filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_branch_name = report.current_branch.replace("/", "_").replace("\\", "_")
            output_file = f"code_review_{safe_branch_name}_{timestamp}.md"
            reviewer.save_report(report, output_file, args.format)
        
        # Display risk level
        risk_level = "Low"
        if len(report.risk_factors) > 5:
            risk_level = "High"
        elif len(report.risk_factors) > 2:
            risk_level = "Medium"
        
        print(f"\n🎯 Risk Level: {risk_level}")
        
        if report.risk_factors:
            print("\n⚠️  Key Risk Factors:")
            for risk in report.risk_factors[:3]:  # Show top 3
                print(f"   - {risk}")
        
        print("\n✅ Code review completed!")
        
    except Exception as e:
        print(f"❌ Error during code review: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
