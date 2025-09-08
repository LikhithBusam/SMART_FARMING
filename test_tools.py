#!/usr/bin/env python3
"""
Test script to check if MCP server tools work correctly
"""

import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Import the server module to access the MCP tools
from server import mcp


def test_repo_path():
    """Test repository path detection"""
    print("🔍 Testing repository path detection...")
    try:
        # Access the function from the tool
        repo_path = mcp.run_tool("get_repo_path")
        print(f"📁 Repository path: {repo_path}")
        return repo_path
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_project_overview():
    """Test project overview function"""
    print("\n📊 Testing project overview...")
    try:
        overview = mcp.run_tool("get_project_overview")
        print(f"✅ Project overview: {overview}")
        return overview
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_python_analysis():
    """Test Python files analysis"""
    print("\n🐍 Testing Python files analysis...")
    try:
        python_analysis = mcp.run_tool("analyze_python_files")
        print(f"✅ Python files analysis: {python_analysis}")
        return python_analysis
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_ml_components():
    """Test ML components detection"""
    print("\n🤖 Testing ML components detection...")
    try:
        ml_components = mcp.run_tool("find_ml_components")
        print(f"✅ ML components: {ml_components}")
        return ml_components
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_weather_data():
    """Test weather data fetching"""
    print("\n🌦️ Testing weather data fetching...")
    try:
        weather = mcp.run_tool("get_weather", city="Nuzividu")
        print(f"✅ Weather data: {weather}")
        return weather
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_leaf_image_analysis():
    """Test plant leaf image analysis"""
    print("\n🌿 Testing plant leaf image analysis...")
    try:
        image_analysis = mcp.run_tool("analyze_leaf_image", image_path="temp/sample_image.png")
        print(f"✅ Image analysis: {image_analysis}")
        return image_analysis
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    """Run all tests"""
    print("🧪 Testing SMART_FARMING MCP Server Tools")
    print("=" * 60)
    
    # Test all tools
    tests = [
        test_repo_path,
        test_project_overview,
        test_python_analysis,
        test_ml_components,
        test_weather_data,
        test_leaf_image_analysis
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result is not None)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary:")
    passed = sum(results)
    total = len(results)
    print(f"✅ Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! MCP server tools are working correctly.")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
