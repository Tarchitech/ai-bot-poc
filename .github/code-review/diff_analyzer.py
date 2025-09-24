#!/usr/bin/env python3
"""
Advanced Diff Analyzer for Code Review Bot

This module provides sophisticated analysis of code differences,
including syntax highlighting, change categorization, and impact assessment.
"""

import re
import ast
import json
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import difflib

class ChangeType(Enum):
    """Types of code changes"""
    ADDITION = "addition"
    DELETION = "deletion"
    MODIFICATION = "modification"
    MOVEMENT = "movement"

class ChangeImpact(Enum):
    """Impact levels of changes"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class CodeChange:
    """Represents a single code change"""
    file_path: str
    line_number: int
    change_type: ChangeType
    old_content: str
    new_content: str
    impact: ChangeImpact
    context: str
    language: str

@dataclass
class FileAnalysis:
    """Analysis results for a single file"""
    file_path: str
    language: str
    changes: List[CodeChange]
    total_additions: int
    total_deletions: int
    complexity_change: int
    risk_factors: List[str]
    suggestions: List[str]

class DiffAnalyzer:
    """Advanced diff analyzer for code review"""
    
    def __init__(self):
        self.language_patterns = self._init_language_patterns()
        self.risk_patterns = self._init_risk_patterns()
        self.complexity_keywords = self._init_complexity_keywords()
    
    def _init_language_patterns(self) -> Dict[str, Dict[str, str]]:
        """Initialize language detection patterns"""
        return {
            'python': {
                'extensions': ['.py'],
                'keywords': ['def ', 'class ', 'import ', 'from ', 'if __name__'],
                'syntax': ['def', 'class', 'import', 'from', 'if', 'for', 'while', 'try', 'except']
            },
            'javascript': {
                'extensions': ['.js', '.jsx'],
                'keywords': ['function', 'const ', 'let ', 'var ', 'class ', 'import ', 'export '],
                'syntax': ['function', 'const', 'let', 'var', 'class', 'import', 'export', 'if', 'for', 'while']
            },
            'typescript': {
                'extensions': ['.ts', '.tsx'],
                'keywords': ['function', 'const ', 'let ', 'var ', 'class ', 'interface ', 'type ', 'import ', 'export '],
                'syntax': ['function', 'const', 'let', 'var', 'class', 'interface', 'type', 'import', 'export']
            },
            'java': {
                'extensions': ['.java'],
                'keywords': ['public class', 'private ', 'public ', 'protected ', 'import ', 'package '],
                'syntax': ['public', 'private', 'protected', 'class', 'interface', 'import', 'package']
            },
            'cpp': {
                'extensions': ['.cpp', '.cc', '.cxx', '.hpp', '.h'],
                'keywords': ['#include', 'class ', 'struct ', 'namespace ', 'template '],
                'syntax': ['#include', 'class', 'struct', 'namespace', 'template', 'public', 'private']
            },
            'go': {
                'extensions': ['.go'],
                'keywords': ['package ', 'import ', 'func ', 'type ', 'struct ', 'interface '],
                'syntax': ['package', 'import', 'func', 'type', 'struct', 'interface']
            },
            'rust': {
                'extensions': ['.rs'],
                'keywords': ['fn ', 'struct ', 'enum ', 'impl ', 'trait ', 'mod ', 'use '],
                'syntax': ['fn', 'struct', 'enum', 'impl', 'trait', 'mod', 'use']
            }
        }
    
    def _init_risk_patterns(self) -> Dict[str, List[str]]:
        """Initialize risk detection patterns"""
        return {
            'security': [
                r'password\s*=\s*["\'][^"\']+["\']',
                r'secret\s*=\s*["\'][^"\']+["\']',
                r'api_key\s*=\s*["\'][^"\']+["\']',
                r'private_key\s*=\s*["\'][^"\']+["\']',
                r'SELECT.*\+.*FROM',
                r'INSERT.*\+.*INTO',
                r'UPDATE.*\+.*SET',
                r'DELETE.*\+.*FROM',
                r'eval\s*\(',
                r'exec\s*\(',
                r'system\s*\(',
                r'shell_exec\s*\('
            ],
            'performance': [
                r'for\s*\([^)]*\)\s*\{[^}]*for\s*\([^)]*\)',
                r'while\s*\(\s*true\s*\)',
                r'sleep\s*\(',
                r'time\.sleep\s*\(',
                r'Thread\.sleep\s*\(',
                r'SELECT\s+\*\s+FROM',
                r'\.map\s*\([^)]*\)\.map\s*\(',
                r'\.filter\s*\([^)]*\)\.filter\s*\('
            ],
            'maintainability': [
                r'TODO',
                r'FIXME',
                r'XXX',
                r'HACK',
                r'BUG',
                r'TEMP',
                r'print\s*\(',
                r'console\.log\s*\(',
                r'System\.out\.print',
                r'debugger\s*;'
            ],
            'error_handling': [
                r'except\s*:',
                r'catch\s*\(\s*Exception\s*\)',
                r'catch\s*\(\s*\w*\s*\)\s*\{\s*\}',
                r'throw\s+new\s+Error\s*\(',
                r'raise\s+Exception\s*\('
            ]
        }
    
    def _init_complexity_keywords(self) -> List[str]:
        """Initialize complexity assessment keywords"""
        return [
            'if', 'elif', 'else', 'for', 'while', 'try', 'except', 'catch',
            'switch', 'case', 'break', 'continue', 'return', 'yield',
            '&&', '||', '?', ':', 'and', 'or', 'not'
        ]
    
    def detect_language(self, file_path: str, content: str = "") -> str:
        """Detect programming language from file path and content"""
        # First, try to detect from file extension
        for lang, patterns in self.language_patterns.items():
            for ext in patterns['extensions']:
                if file_path.endswith(ext):
                    return lang
        
        # If no extension match, try to detect from content
        if content:
            for lang, patterns in self.language_patterns.items():
                keyword_count = 0
                for keyword in patterns['keywords']:
                    if keyword in content:
                        keyword_count += 1
                
                if keyword_count >= 2:  # At least 2 keywords match
                    return lang
        
        return 'unknown'
    
    def analyze_diff(self, diff_text: str) -> List[FileAnalysis]:
        """Analyze a unified diff and return structured analysis"""
        files = self._parse_diff(diff_text)
        analyses = []
        
        for file_info in files:
            analysis = self._analyze_file(file_info)
            analyses.append(analysis)
        
        return analyses
    
    def _parse_diff(self, diff_text: str) -> List[Dict[str, Any]]:
        """Parse unified diff into structured format"""
        files = []
        current_file = None
        current_hunk = None
        
        lines = diff_text.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # File header
            if line.startswith('diff --git'):
                if current_file:
                    files.append(current_file)
                
                current_file = {
                    'file_path': self._extract_file_path(line),
                    'language': 'unknown',
                    'changes': [],
                    'old_content': '',
                    'new_content': ''
                }
            
            # File paths
            elif line.startswith('---') or line.startswith('+++'):
                if current_file:
                    if line.startswith('---'):
                        current_file['old_path'] = line[4:].strip()
                    else:
                        current_file['new_path'] = line[4:].strip()
            
            # Hunk header
            elif line.startswith('@@'):
                current_hunk = self._parse_hunk_header(line)
            
            # Content lines
            elif line.startswith(('+', '-', ' ')) and current_file and current_hunk:
                change = self._parse_content_line(line, current_hunk)
                if change:
                    current_file['changes'].append(change)
            
            i += 1
        
        if current_file:
            files.append(current_file)
        
        return files
    
    def _extract_file_path(self, diff_line: str) -> str:
        """Extract file path from diff header"""
        # Format: diff --git a/path/to/file b/path/to/file
        parts = diff_line.split()
        if len(parts) >= 4:
            return parts[3][2:]  # Remove 'b/' prefix
        return 'unknown'
    
    def _parse_hunk_header(self, header: str) -> Dict[str, int]:
        """Parse hunk header to get line numbers"""
        # Format: @@ -start,count +start,count @@
        match = re.search(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', header)
        if match:
            return {
                'old_start': int(match.group(1)),
                'old_count': int(match.group(2)) if match.group(2) else 1,
                'new_start': int(match.group(3)),
                'new_count': int(match.group(4)) if match.group(4) else 1
            }
        return {}
    
    def _parse_content_line(self, line: str, hunk: Dict[str, int]) -> Optional[Dict[str, Any]]:
        """Parse a content line and return change information"""
        if len(line) < 1:
            return None
        
        prefix = line[0]
        content = line[1:]
        
        change_type = None
        if prefix == '+':
            change_type = ChangeType.ADDITION
        elif prefix == '-':
            change_type = ChangeType.DELETION
        elif prefix == ' ':
            return None  # Context line
        
        return {
            'type': change_type,
            'content': content,
            'line_number': hunk.get('new_start', 0) if prefix == '+' else hunk.get('old_start', 0)
        }
    
    def _analyze_file(self, file_info: Dict[str, Any]) -> FileAnalysis:
        """Analyze a single file's changes"""
        file_path = file_info['file_path']
        changes = file_info['changes']
        
        # Detect language
        language = self.detect_language(file_path)
        
        # Count additions and deletions
        additions = sum(1 for change in changes if change['type'] == ChangeType.ADDITION)
        deletions = sum(1 for change in changes if change['type'] == ChangeType.DELETION)
        
        # Analyze complexity change
        complexity_change = self._analyze_complexity_change(changes)
        
        # Identify risk factors
        risk_factors = self._identify_risk_factors(changes, language)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(changes, language, risk_factors)
        
        # Create CodeChange objects
        code_changes = []
        for change in changes:
            impact = self._assess_change_impact(change, risk_factors)
            code_change = CodeChange(
                file_path=file_path,
                line_number=change['line_number'],
                change_type=change['type'],
                old_content='' if change['type'] == ChangeType.ADDITION else change['content'],
                new_content=change['content'] if change['type'] == ChangeType.ADDITION else '',
                impact=impact,
                context=self._get_context(changes, change),
                language=language
            )
            code_changes.append(code_change)
        
        return FileAnalysis(
            file_path=file_path,
            language=language,
            changes=code_changes,
            total_additions=additions,
            total_deletions=deletions,
            complexity_change=complexity_change,
            risk_factors=risk_factors,
            suggestions=suggestions
        )
    
    def _analyze_complexity_change(self, changes: List[Dict[str, Any]]) -> int:
        """Analyze how changes affect code complexity"""
        complexity_delta = 0
        
        for change in changes:
            content = change['content']
            
            # Count complexity keywords
            keyword_count = sum(1 for keyword in self.complexity_keywords if keyword in content)
            
            if change['type'] == ChangeType.ADDITION:
                complexity_delta += keyword_count
            elif change['type'] == ChangeType.DELETION:
                complexity_delta -= keyword_count
        
        return complexity_delta
    
    def _identify_risk_factors(self, changes: List[Dict[str, Any]], language: str) -> List[str]:
        """Identify potential risk factors in changes"""
        risk_factors = []
        
        for change in changes:
            content = change['content']
            
            for risk_type, patterns in self.risk_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        risk_factors.append(f"{risk_type}: {pattern}")
        
        return list(set(risk_factors))  # Remove duplicates
    
    def _generate_suggestions(self, changes: List[Dict[str, Any]], language: str, risk_factors: List[str]) -> List[str]:
        """Generate improvement suggestions based on changes"""
        suggestions = []
        
        # Language-specific suggestions
        if language == 'python':
            suggestions.extend(self._get_python_suggestions(changes))
        elif language in ['javascript', 'typescript']:
            suggestions.extend(self._get_js_suggestions(changes))
        elif language == 'java':
            suggestions.extend(self._get_java_suggestions(changes))
        
        # Risk-based suggestions
        for risk in risk_factors:
            if 'security' in risk:
                suggestions.append("Review security implications and consider using secure alternatives")
            elif 'performance' in risk:
                suggestions.append("Consider performance optimization and caching strategies")
            elif 'maintainability' in risk:
                suggestions.append("Address technical debt and improve code documentation")
        
        return suggestions
    
    def _get_python_suggestions(self, changes: List[Dict[str, Any]]) -> List[str]:
        """Get Python-specific suggestions"""
        suggestions = []
        
        for change in changes:
            content = change['content']
            
            if 'print(' in content:
                suggestions.append("Consider using logging instead of print statements")
            if 'except:' in content:
                suggestions.append("Use specific exception handling instead of bare except")
            if 'import *' in content:
                suggestions.append("Avoid wildcard imports for better namespace clarity")
        
        return suggestions
    
    def _get_js_suggestions(self, changes: List[Dict[str, Any]]) -> List[str]:
        """Get JavaScript/TypeScript-specific suggestions"""
        suggestions = []
        
        for change in changes:
            content = change['content']
            
            if 'var ' in content:
                suggestions.append("Consider using 'const' or 'let' instead of 'var'")
            if 'console.log' in content:
                suggestions.append("Consider using proper logging instead of console.log")
            if '===' not in content and '==' in content:
                suggestions.append("Use strict equality (===) instead of loose equality (==)")
        
        return suggestions
    
    def _get_java_suggestions(self, changes: List[Dict[str, Any]]) -> List[str]:
        """Get Java-specific suggestions"""
        suggestions = []
        
        for change in changes:
            content = change['content']
            
            if 'System.out.print' in content:
                suggestions.append("Consider using proper logging framework instead of System.out")
            if 'catch (Exception' in content:
                suggestions.append("Use specific exception types instead of generic Exception")
            if 'new Date()' in content:
                suggestions.append("Consider using java.time API instead of legacy Date")
        
        return suggestions
    
    def _assess_change_impact(self, change: Dict[str, Any], risk_factors: List[str]) -> ChangeImpact:
        """Assess the impact level of a change"""
        content = change['content']
        
        # Check for critical patterns
        critical_patterns = [
            r'password', r'secret', r'api_key', r'private_key',
            r'eval\s*\(', r'exec\s*\(', r'system\s*\(',
            r'SELECT.*\+', r'INSERT.*\+', r'UPDATE.*\+', r'DELETE.*\+'
        ]
        
        for pattern in critical_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return ChangeImpact.CRITICAL
        
        # Check for high impact patterns
        high_patterns = [
            r'for.*for', r'while.*true', r'sleep\s*\(',
            r'Thread\.sleep', r'time\.sleep'
        ]
        
        for pattern in high_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return ChangeImpact.HIGH
        
        # Check for medium impact patterns
        medium_patterns = [
            r'TODO', r'FIXME', r'XXX', r'HACK',
            r'print\s*\(', r'console\.log'
        ]
        
        for pattern in medium_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return ChangeImpact.MEDIUM
        
        return ChangeImpact.LOW
    
    def _get_context(self, changes: List[Dict[str, Any]], current_change: Dict[str, Any]) -> str:
        """Get context around a change"""
        # Simple context extraction - in a real implementation,
        # you'd want to get more surrounding lines
        context_lines = []
        
        for change in changes:
            if abs(change['line_number'] - current_change['line_number']) <= 3:
                context_lines.append(change['content'])
        
        return '\n'.join(context_lines)
    
    def generate_summary(self, analyses: List[FileAnalysis]) -> Dict[str, Any]:
        """Generate a summary of all file analyses"""
        total_files = len(analyses)
        total_additions = sum(analysis.total_additions for analysis in analyses)
        total_deletions = sum(analysis.total_deletions for analysis in analyses)
        
        # Count changes by impact
        impact_counts = {
            ChangeImpact.CRITICAL: 0,
            ChangeImpact.HIGH: 0,
            ChangeImpact.MEDIUM: 0,
            ChangeImpact.LOW: 0
        }
        
        all_risk_factors = []
        all_suggestions = []
        
        for analysis in analyses:
            for change in analysis.changes:
                impact_counts[change.impact] += 1
            
            all_risk_factors.extend(analysis.risk_factors)
            all_suggestions.extend(analysis.suggestions)
        
        return {
            'summary': {
                'total_files_changed': total_files,
                'total_additions': total_additions,
                'total_deletions': total_deletions,
                'net_change': total_additions - total_deletions
            },
            'impact_breakdown': {
                'critical': impact_counts[ChangeImpact.CRITICAL],
                'high': impact_counts[ChangeImpact.HIGH],
                'medium': impact_counts[ChangeImpact.MEDIUM],
                'low': impact_counts[ChangeImpact.LOW]
            },
            'risk_factors': list(set(all_risk_factors)),
            'suggestions': list(set(all_suggestions)),
            'files': [
                {
                    'path': analysis.file_path,
                    'language': analysis.language,
                    'changes_count': len(analysis.changes),
                    'risk_factors': analysis.risk_factors,
                    'complexity_change': analysis.complexity_change
                }
                for analysis in analyses
            ]
        }
