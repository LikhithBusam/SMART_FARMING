#!/usr/bin/env python3
"""
Test script for the SMART_FARMING MCP Server
This script tests the MCP server functionality
"""

import asyncio
import sys
from pathlib import Path

# Add the mcp-server-demo directory to the path
mcp_server_path = Path(__file__).parent / "mcp-server-demo"
sys.path.insert(0, str(mcp_server_path))

from main import get_repo_path, get_project_overview

def test_repo_path():
    """Test if the repository path is correctly detected"""
    print("🔍 Testing repository path detection...")
    repo_path = get_repo_path()
    print(f"📁 Detected repository path: {repo_path}")
    
    if Path(repo_path).exists():
        print("✅ Repository path exists")
        if (Path(repo_path) / "app.py").exists():
            print("✅ Found app.py - this looks like the SMART_FARMING project")
        else:
            print("⚠️ app.py not found - path might be incorrect")
    else:
        print("❌ Repository path does not exist")
    
    return repo_path

def test_project_overview():
    """Test the project overview function"""
    print("\n📊 Testing project overview...")
    try:
        overview = get_project_overview()
        print("✅ Project overview generated successfully")
        print(f"📋 Project exists: {overview.get('exists', 'Unknown')}")
        print(f"📁 Repository path: {overview.get('repository_path', 'Unknown')}")
        print(f"🔧 Key files found: {len(overview.get('key_files', []))}")
        print(f"🏗️ Structure levels: {len(overview.get('structure', {}))}")
        return overview
    except Exception as e:
        print(f"❌ Error generating project overview: {e}")
        return None

def main():
    """Main test function"""
    print("🧪 Testing SMART_FARMING MCP Server")
    print("=" * 50)
    
    # Test repository path detection
    repo_path = test_repo_path()
    
    # Test project overview
    overview = test_project_overview()
    
    print("\n" + "=" * 50)
    if overview and overview.get('exists'):
        print("🎉 All tests passed! MCP server should work correctly.")
    else:
        print("⚠️ Some tests failed. Check the configuration.")
    
    print(f"\n📝 To run the MCP server: python server.py")
    print(f"📝 To run the Streamlit app: streamlit run app.py")

if __name__ == "__main__":
    main()
