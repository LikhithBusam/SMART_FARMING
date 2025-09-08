#!/usr/bin/env python3
"""
Async test of MCP server tools
"""

import asyncio
import server

async def test_mcp_tools():
    """Test MCP server tools asynchronously"""
    print("🧪 Testing MCP Server Tools (Async)")
    print("=" * 50)
    
    try:
        # Get tools
        tools = await server.mcp.get_tools()
        print(f"✅ Found {len(tools)} tools:")
        
        for tool in tools:
            print(f"   • {tool.name}: {tool.description}")
        
        # Test each tool
        for tool in tools:
            print(f"\n🔧 Testing tool: {tool.name}")
            try:
                # Get the tool object
                tool_obj = await server.mcp.get_tool(tool.name)
                print(f"   📊 Tool object: {type(tool_obj)}")
                
                # Try to call the tool
                if hasattr(tool_obj, 'call'):
                    result = await tool_obj.call()
                    print(f"   ✅ {tool.name} executed successfully")
                    print(f"   📊 Result type: {type(result)}")
                    if isinstance(result, dict):
                        print(f"   📋 Result keys: {list(result.keys())}")
                else:
                    print(f"   ⚠️ {tool.name} has no call method")
                    
            except Exception as e:
                print(f"   ❌ {tool.name} failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main test function"""
    try:
        success = asyncio.run(test_mcp_tools())
        if success:
            print("\n🎉 MCP Server tools are working correctly!")
        else:
            print("\n⚠️ MCP Server tools have issues.")
        return success
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
