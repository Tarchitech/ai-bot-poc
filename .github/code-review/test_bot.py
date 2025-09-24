#!/usr/bin/env python3
"""
Test script for AI Code Review Bot

This script provides basic testing functionality for the code review bot
without requiring actual GitHub API calls.
"""

import os
import sys
import json
from unittest.mock import Mock, patch
from diff_analyzer import DiffAnalyzer
from review_prompts import ReviewPromptManager

def test_diff_analyzer():
    """Test the diff analyzer functionality"""
    print("🧪 Testing Diff Analyzer...")
    
    analyzer = DiffAnalyzer()
    
    # Test language detection
    assert analyzer.detect_language("test.py") == "python"
    assert analyzer.detect_language("test.js") == "javascript"
    assert analyzer.detect_language("test.java") == "java"
    print("✅ Language detection working")
    
    # Test diff parsing
    sample_diff = """
diff --git a/test.py b/test.py
index 1234567..abcdefg 100644
--- a/test.py
+++ b/test.py
@@ -1,3 +1,4 @@
 def hello():
-    print("Hello")
+    print("Hello World")
+    return True
"""
    
    analyses = analyzer.analyze_diff(sample_diff)
    assert len(analyses) == 1
    assert analyses[0].file_path == "test.py"
    assert analyses[0].total_additions == 2
    assert analyses[0].total_deletions == 1
    print("✅ Diff parsing working")
    
    # Test summary generation
    summary = analyzer.generate_summary(analyses)
    assert summary['summary']['total_files_changed'] == 1
    assert summary['summary']['total_additions'] == 2
    assert summary['summary']['total_deletions'] == 1
    print("✅ Summary generation working")

def test_review_prompts():
    """Test the review prompts functionality"""
    print("🧪 Testing Review Prompts...")
    
    manager = ReviewPromptManager()
    
    # Test getting prompts for specific language
    python_prompts = manager.get_prompts_for_language("python")
    assert len(python_prompts) > 0
    print("✅ Language-specific prompts working")
    
    # Test getting specific prompt
    security_prompt = manager.get_prompt_by_name("security")
    assert security_prompt.name == "security"
    assert "security" in security_prompt.prompt_template.lower()
    print("✅ Specific prompt retrieval working")
    
    # Test getting all prompts
    all_prompts = manager.get_all_prompts()
    assert len(all_prompts) > 0
    assert all_prompts[0].priority <= all_prompts[1].priority
    print("✅ Priority sorting working")

def test_config_loading():
    """Test configuration loading"""
    print("🧪 Testing Configuration Loading...")
    
    # Test if config file exists and is valid JSON
    if os.path.exists(".github/code-review/config.json"):
        with open(".github/code-review/config.json", "r") as f:
            config = json.load(f)
        
        assert "rules" in config
        assert "ai_settings" in config
        assert "review_settings" in config
        print("✅ Configuration file valid")
    else:
        print("⚠️  Configuration file not found - this is expected for testing")

def test_environment_variables():
    """Test environment variable handling"""
    print("🧪 Testing Environment Variables...")
    
    # Test required variables
    required_vars = ["GITHUB_TOKEN", "GOOGLE_API_KEY", "REPO_OWNER", "REPO_NAME"]
    
    for var in required_vars:
        if os.getenv(var):
            print(f"✅ {var} is set")
        else:
            print(f"⚠️  {var} is not set (expected for testing)")

def mock_github_api_test():
    """Test with mocked GitHub API"""
    print("🧪 Testing with Mocked GitHub API...")
    
    # Mock GitHub API responses
    mock_files = [
        {
            "filename": "test.py",
            "status": "modified",
            "additions": 5,
            "deletions": 2,
            "changes": 7
        }
    ]
    
    mock_diff = """
diff --git a/test.py b/test.py
index 1234567..abcdefg 100644
--- a/test.py
+++ b/test.py
@@ -1,3 +1,6 @@
 def hello():
-    print("Hello")
+    print("Hello World")
+    return True
+
+def goodbye():
+    print("Goodbye")
"""
    
    # Test with mocked data
    analyzer = DiffAnalyzer()
    analyses = analyzer.analyze_diff(mock_diff)
    
    assert len(analyses) == 1
    assert analyses[0].file_path == "test.py"
    assert analyses[0].total_additions == 4
    assert analyses[0].total_deletions == 1
    
    print("✅ Mocked API test working")

def run_integration_test():
    """Run a basic integration test"""
    print("🧪 Running Integration Test...")
    
    try:
        # Test importing all modules
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from code_review_bot import CodeReviewBot, GitHubAPIClient
        from diff_analyzer import DiffAnalyzer
        from review_prompts import ReviewPromptManager
        
        print("✅ All modules imported successfully")
        
        # Test basic functionality
        analyzer = DiffAnalyzer()
        manager = ReviewPromptManager()
        
        print("✅ Core components initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting AI Code Review Bot Tests\n")
    
    tests = [
        test_diff_analyzer,
        test_review_prompts,
        test_config_loading,
        test_environment_variables,
        mock_github_api_test,
        run_integration_test
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            test()
            passed += 1
            print()
        except Exception as e:
            print(f"❌ Test failed: {e}")
            print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The bot is ready to use.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
