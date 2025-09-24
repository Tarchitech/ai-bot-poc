#!/usr/bin/env python3
"""
Advanced Review Prompts for AI Code Review Bot

This module contains specialized prompts for different types of code reviews,
including security, performance, maintainability, and best practices.
"""

from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class ReviewPrompt:
    """Represents a specialized review prompt"""
    name: str
    description: str
    prompt_template: str
    applicable_languages: List[str]
    priority: int  # 1 = highest priority

class ReviewPromptManager:
    """Manages different types of review prompts"""
    
    def __init__(self):
        self.prompts = self._initialize_prompts()
    
    def _initialize_prompts(self) -> List[ReviewPrompt]:
        """Initialize all review prompts"""
        return [
            self._get_security_prompt(),
            self._get_performance_prompt(),
            self._get_maintainability_prompt(),
            self._get_best_practices_prompt(),
            self._get_documentation_prompt(),
            self._get_testing_prompt(),
            self._get_accessibility_prompt(),
            self._get_api_design_prompt()
        ]
    
    def _get_security_prompt(self) -> ReviewPrompt:
        """Security-focused review prompt"""
        return ReviewPrompt(
            name="security",
            description="Comprehensive security review",
            applicable_languages=["python", "javascript", "typescript", "java", "cpp", "c", "go", "rust"],
            priority=1,
            prompt_template="""
You are a cybersecurity expert conducting a thorough security review of the following code changes.

SECURITY CHECKLIST:
1. **Authentication & Authorization**
   - Are user inputs properly validated and sanitized?
   - Are authentication mechanisms secure?
   - Are authorization checks in place?

2. **Data Protection**
   - Are sensitive data (passwords, keys, tokens) properly handled?
   - Is data encryption used where appropriate?
   - Are database queries protected against injection?

3. **Input Validation**
   - Are all user inputs validated?
   - Are file uploads properly restricted?
   - Are URL parameters sanitized?

4. **Error Handling**
   - Do error messages leak sensitive information?
   - Are exceptions properly caught and handled?

5. **Dependencies**
   - Are third-party libraries up to date?
   - Are known vulnerable packages used?

CODE CHANGES:
{diff}

Please provide a detailed security analysis focusing on:
- **Critical Issues**: Immediate security vulnerabilities
- **High Risk**: Potential security concerns
- **Medium Risk**: Security best practices violations
- **Recommendations**: Specific security improvements

Format your response as:
## 🔒 Security Review Summary
[Overall security assessment]

## 🚨 Critical Security Issues
- **File**: [filename]
  - **Line**: [line number]
  - **Issue**: [specific security vulnerability]
  - **Risk**: [explanation of the risk]
  - **Fix**: [specific remediation steps]

## ⚠️ Security Warnings
[High and medium risk issues]

## 💡 Security Recommendations
[General security improvements]
"""
        )
    
    def _get_performance_prompt(self) -> ReviewPrompt:
        """Performance-focused review prompt"""
        return ReviewPrompt(
            name="performance",
            description="Performance optimization review",
            applicable_languages=["python", "javascript", "typescript", "java", "cpp", "c", "go", "rust"],
            priority=2,
            prompt_template="""
You are a performance optimization expert reviewing the following code changes for efficiency and scalability.

PERFORMANCE CHECKLIST:
1. **Algorithm Complexity**
   - Are algorithms optimal for the use case?
   - Are there unnecessary nested loops?
   - Are data structures chosen appropriately?

2. **Memory Usage**
   - Are there memory leaks?
   - Is memory allocation efficient?
   - Are large objects properly disposed?

3. **Database Operations**
   - Are queries optimized?
   - Are indexes used appropriately?
   - Are N+1 queries avoided?

4. **Network Operations**
   - Are API calls minimized?
   - Is caching implemented where appropriate?
   - Are timeouts configured?

5. **Concurrency**
   - Are race conditions handled?
   - Is thread safety considered?
   - Are async operations used appropriately?

CODE CHANGES:
{diff}

Please provide a detailed performance analysis focusing on:
- **Performance Bottlenecks**: Code that may cause slowdowns
- **Memory Issues**: Potential memory leaks or excessive usage
- **Scalability Concerns**: Issues that may impact scaling
- **Optimization Opportunities**: Specific performance improvements

Format your response as:
## ⚡ Performance Review Summary
[Overall performance assessment]

## 🐌 Performance Bottlenecks
- **File**: [filename]
  - **Line**: [line number]
  - **Issue**: [specific performance problem]
  - **Impact**: [explanation of performance impact]
  - **Solution**: [specific optimization approach]

## 💾 Memory Concerns
[Memory-related issues]

## 📈 Optimization Recommendations
[Specific performance improvements]
"""
        )
    
    def _get_maintainability_prompt(self) -> ReviewPrompt:
        """Maintainability-focused review prompt"""
        return ReviewPrompt(
            name="maintainability",
            description="Code maintainability and readability review",
            applicable_languages=["python", "javascript", "typescript", "java", "cpp", "c", "go", "rust"],
            priority=3,
            prompt_template="""
You are a senior software engineer reviewing code for maintainability, readability, and long-term sustainability.

MAINTAINABILITY CHECKLIST:
1. **Code Structure**
   - Is the code well-organized and modular?
   - Are functions and classes appropriately sized?
   - Is separation of concerns maintained?

2. **Readability**
   - Are variable and function names descriptive?
   - Is the code self-documenting?
   - Are complex logic sections commented?

3. **Consistency**
   - Does the code follow established patterns?
   - Are coding standards consistently applied?
   - Is the style consistent with the codebase?

4. **Complexity**
   - Is cyclomatic complexity reasonable?
   - Are there overly complex functions?
   - Can the code be easily understood by new developers?

5. **Technical Debt**
   - Are there TODO/FIXME comments that need attention?
   - Are there code smells present?
   - Is the code ready for production?

CODE CHANGES:
{diff}

Please provide a detailed maintainability analysis focusing on:
- **Code Quality**: Overall code quality assessment
- **Readability Issues**: Code that's hard to understand
- **Structural Problems**: Organization and architecture concerns
- **Technical Debt**: Areas that need improvement

Format your response as:
## 🔧 Maintainability Review Summary
[Overall maintainability assessment]

## 📖 Readability Issues
- **File**: [filename]
  - **Line**: [line number]
  - **Issue**: [specific readability problem]
  - **Impact**: [why this affects maintainability]
  - **Improvement**: [specific suggestions]

## 🏗️ Structural Concerns
[Architecture and organization issues]

## 💳 Technical Debt
[Areas requiring attention]
"""
        )
    
    def _get_best_practices_prompt(self) -> ReviewPrompt:
        """Best practices review prompt"""
        return ReviewPrompt(
            name="best_practices",
            description="Industry best practices review",
            applicable_languages=["python", "javascript", "typescript", "java", "cpp", "c", "go", "rust"],
            priority=4,
            prompt_template="""
You are an expert software engineer reviewing code for adherence to industry best practices and modern development standards.

BEST PRACTICES CHECKLIST:
1. **Language-Specific Practices**
   - Are language idioms used correctly?
   - Are modern language features utilized?
   - Are deprecated patterns avoided?

2. **Error Handling**
   - Are exceptions handled appropriately?
   - Is error logging implemented?
   - Are graceful degradation strategies in place?

3. **Resource Management**
   - Are resources properly closed/disposed?
   - Is connection pooling used where appropriate?
   - Are file handles managed correctly?

4. **Configuration Management**
   - Are configuration values externalized?
   - Are environment-specific settings handled?
   - Are secrets properly managed?

5. **Logging and Monitoring**
   - Is appropriate logging implemented?
   - Are metrics and monitoring considered?
   - Is debugging information available?

CODE CHANGES:
{diff}

Please provide a detailed best practices analysis focusing on:
- **Standards Compliance**: Adherence to coding standards
- **Modern Practices**: Use of current best practices
- **Anti-patterns**: Code that violates best practices
- **Improvements**: Specific recommendations

Format your response as:
## ✅ Best Practices Review Summary
[Overall best practices assessment]

## 📋 Standards Compliance
- **File**: [filename]
  - **Line**: [line number]
  - **Issue**: [specific standards violation]
  - **Standard**: [which standard is violated]
  - **Recommendation**: [specific improvement]

## 🚫 Anti-patterns
[Code that violates best practices]

## 🎯 Improvement Opportunities
[Specific best practice recommendations]
"""
        )
    
    def _get_documentation_prompt(self) -> ReviewPrompt:
        """Documentation-focused review prompt"""
        return ReviewPrompt(
            name="documentation",
            description="Documentation and comments review",
            applicable_languages=["python", "javascript", "typescript", "java", "cpp", "c", "go", "rust"],
            priority=5,
            prompt_template="""
You are a technical writer reviewing code for documentation quality and completeness.

DOCUMENTATION CHECKLIST:
1. **Function Documentation**
   - Do functions have clear docstrings/comments?
   - Are parameters and return values documented?
   - Are examples provided for complex functions?

2. **API Documentation**
   - Are public APIs well-documented?
   - Are usage examples provided?
   - Are edge cases documented?

3. **Code Comments**
   - Are complex algorithms explained?
   - Are business logic decisions documented?
   - Are non-obvious code sections commented?

4. **README and Setup**
   - Is setup documentation clear?
   - Are dependencies listed?
   - Are usage instructions provided?

CODE CHANGES:
{diff}

Please provide a detailed documentation analysis focusing on:
- **Missing Documentation**: Areas lacking documentation
- **Documentation Quality**: Quality of existing documentation
- **Clarity Issues**: Unclear or confusing documentation
- **Completeness**: Documentation gaps

Format your response as:
## 📚 Documentation Review Summary
[Overall documentation assessment]

## ❌ Missing Documentation
- **File**: [filename]
  - **Function/Class**: [specific item]
  - **Issue**: [what documentation is missing]
  - **Importance**: [why this documentation is needed]
  - **Suggestion**: [specific documentation to add]

## 📝 Documentation Quality Issues
[Problems with existing documentation]

## 🔍 Clarity Improvements
[Suggestions for clearer documentation]
"""
        )
    
    def _get_testing_prompt(self) -> ReviewPrompt:
        """Testing-focused review prompt"""
        return ReviewPrompt(
            name="testing",
            description="Test coverage and quality review",
            applicable_languages=["python", "javascript", "typescript", "java", "cpp", "c", "go", "rust"],
            priority=6,
            prompt_template="""
You are a QA engineer reviewing code for testability and test coverage.

TESTING CHECKLIST:
1. **Test Coverage**
   - Are new functions/classes tested?
   - Are edge cases covered?
   - Are error conditions tested?

2. **Test Quality**
   - Are tests meaningful and not just coverage?
   - Are tests maintainable?
   - Are test data realistic?

3. **Testability**
   - Is the code testable?
   - Are dependencies properly mocked?
   - Are side effects minimized?

4. **Test Organization**
   - Are tests well-organized?
   - Are test names descriptive?
   - Are test utilities available?

CODE CHANGES:
{diff}

Please provide a detailed testing analysis focusing on:
- **Test Coverage**: Areas lacking test coverage
- **Test Quality**: Quality of existing tests
- **Testability Issues**: Code that's hard to test
- **Testing Recommendations**: Specific testing improvements

Format your response as:
## 🧪 Testing Review Summary
[Overall testing assessment]

## 📊 Test Coverage Gaps
- **File**: [filename]
  - **Function/Class**: [specific item]
  - **Issue**: [what testing is missing]
  - **Risk**: [why this needs testing]
  - **Suggestion**: [specific tests to add]

## 🎯 Test Quality Issues
[Problems with existing tests]

## 🔧 Testability Improvements
[Suggestions for more testable code]
"""
        )
    
    def _get_accessibility_prompt(self) -> ReviewPrompt:
        """Accessibility-focused review prompt"""
        return ReviewPrompt(
            name="accessibility",
            description="Web accessibility review",
            applicable_languages=["javascript", "typescript", "html", "css"],
            priority=7,
            prompt_template="""
You are an accessibility expert reviewing web code for WCAG compliance and inclusive design.

ACCESSIBILITY CHECKLIST:
1. **Semantic HTML**
   - Are semantic HTML elements used?
   - Is the document structure logical?
   - Are headings properly nested?

2. **Keyboard Navigation**
   - Is all functionality keyboard accessible?
   - Is tab order logical?
   - Are focus indicators visible?

3. **Screen Reader Support**
   - Are ARIA labels provided?
   - Is alternative text provided for images?
   - Are dynamic content changes announced?

4. **Visual Design**
   - Is color contrast sufficient?
   - Is text resizable?
   - Are interactive elements clearly identifiable?

CODE CHANGES:
{diff}

Please provide a detailed accessibility analysis focusing on:
- **WCAG Violations**: Specific accessibility violations
- **Keyboard Issues**: Keyboard navigation problems
- **Screen Reader Issues**: Problems for assistive technology
- **Visual Issues**: Visual accessibility concerns

Format your response as:
## ♿ Accessibility Review Summary
[Overall accessibility assessment]

## 🚫 WCAG Violations
- **File**: [filename]
  - **Line**: [line number]
  - **Issue**: [specific accessibility violation]
  - **WCAG Level**: [A, AA, or AAA]
  - **Fix**: [specific remediation]

## ⌨️ Keyboard Navigation Issues
[Problems with keyboard accessibility]

## 🔊 Screen Reader Issues
[Problems for assistive technology users]

## 👁️ Visual Accessibility Issues
[Visual design accessibility concerns]
"""
        )
    
    def _get_api_design_prompt(self) -> ReviewPrompt:
        """API design review prompt"""
        return ReviewPrompt(
            name="api_design",
            description="API design and RESTful practices review",
            applicable_languages=["python", "javascript", "typescript", "java", "go", "rust"],
            priority=8,
            prompt_template="""
You are an API design expert reviewing code for RESTful design principles and API best practices.

API DESIGN CHECKLIST:
1. **RESTful Design**
   - Are HTTP methods used correctly?
   - Are URLs resource-oriented?
   - Is statelessness maintained?

2. **Response Design**
   - Are status codes appropriate?
   - Is response format consistent?
   - Are error responses informative?

3. **Request Design**
   - Are query parameters used appropriately?
   - Is request validation implemented?
   - Are content types handled correctly?

4. **Versioning**
   - Is API versioning implemented?
   - Is backward compatibility maintained?
   - Are breaking changes handled?

5. **Security**
   - Is authentication implemented?
   - Is authorization checked?
   - Are rate limits considered?

CODE CHANGES:
{diff}

Please provide a detailed API design analysis focusing on:
- **REST Violations**: Deviations from REST principles
- **Design Issues**: Poor API design choices
- **Security Concerns**: API security problems
- **Best Practices**: Specific API improvements

Format your response as:
## 🌐 API Design Review Summary
[Overall API design assessment]

## 🚫 REST Violations
- **File**: [filename]
  - **Line**: [line number]
  - **Issue**: [specific REST violation]
  - **Principle**: [which REST principle is violated]
  - **Fix**: [specific correction]

## 🎨 Design Issues
[Poor API design choices]

## 🔒 Security Concerns
[API security problems]

## 📈 Best Practice Recommendations
[Specific API improvements]
"""
        )
    
    def get_prompts_for_language(self, language: str) -> List[ReviewPrompt]:
        """Get applicable prompts for a specific language"""
        return [prompt for prompt in self.prompts if language in prompt.applicable_languages]
    
    def get_prompt_by_name(self, name: str) -> ReviewPrompt:
        """Get a specific prompt by name"""
        for prompt in self.prompts:
            if prompt.name == name:
                return prompt
        raise ValueError(f"Prompt '{name}' not found")
    
    def get_all_prompts(self) -> List[ReviewPrompt]:
        """Get all available prompts sorted by priority"""
        return sorted(self.prompts, key=lambda x: x.priority)
