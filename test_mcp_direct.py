#!/usr/bin/env python3
"""
Direct test of MCP server functionality
"""

import asyncio
import json
import subprocess
import sys
from pathlib import Path

async def test_mcp_server():
    """Test the MCP server by running it and sending commands"""
    print("🧪 Testing MCP Server Directly")
    print("=" * 50)
    
    # Start the MCP server process
    server_path = Path(__file__).parent / "server.py"
    
    try:
        # Start the server process
        process = subprocess.Popen(
            [sys.executable, str(server_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("✅ MCP Server started successfully")
        
        # Send initialization request
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        # Send the request
        process.stdin.write(json.dumps(init_request) + "\n")
        process.stdin.flush()
        
        # Read response
        response_line = process.stdout.readline()
        if response_line:
            response = json.loads(response_line)
            print(f"✅ Server initialized: {response.get('result', {}).get('serverInfo', {}).get('name', 'Unknown')}")
        
        # List tools
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        process.stdin.write(json.dumps(tools_request) + "\n")
        process.stdin.flush()
        
        tools_response = process.stdout.readline()
        if tools_response:
            tools_data = json.loads(tools_response)
            tools = tools_data.get('result', {}).get('tools', [])
            print(f"✅ Found {len(tools)} tools:")
            for tool in tools:
                print(f"   • {tool.get('name', 'Unknown')}: {tool.get('description', 'No description')}")
        
        # Test a simple tool call
        if tools:
            test_tool = tools[0]  # Use the first tool
            tool_request = {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": test_tool.get('name'),
                    "arguments": {}
                }
            }
            
            process.stdin.write(json.dumps(tool_request) + "\n")
            process.stdin.flush()
            
            tool_response = process.stdout.readline()
            if tool_response:
                tool_data = json.loads(tool_response)
                if 'result' in tool_data:
                    print(f"✅ Tool '{test_tool.get('name')}' executed successfully")
                else:
                    print(f"❌ Tool '{test_tool.get('name')}' failed: {tool_data.get('error', 'Unknown error')}")
        
        # Clean up
        process.terminate()
        process.wait()
        
        print("✅ MCP Server test completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error testing MCP server: {e}")
        if 'process' in locals():
            process.terminate()
        return False

def main():
    """Main test function"""
    try:
        success = asyncio.run(test_mcp_server())
        if success:
            print("\n🎉 MCP Server is working correctly!")
        else:
            print("\n⚠️ MCP Server has issues.")
        return success
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)




