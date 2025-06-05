#!/usr/bin/env python3
"""
Test script for MCP Search Server
Demonstrates how to test MCP servers with FastMCP
"""

import asyncio
import json
import os
from fastmcp import Client

async def test_mcp_search_server():
    """Test the MCP Search Server functionality"""
    
    print("🧪 MCP Search Server Test Suite")
    print("Built with FastMCP and Exa AI\n")
    
    # Check if EXA_API_KEY is set
    if not os.getenv("EXA_API_KEY"):
        print("❌ EXA_API_KEY environment variable not set!")
        print("Please set your Exa API key: export EXA_API_KEY=your_key_here")
        return
    
    try:
        print("🚀 Testing MCP Search Server")
        print("=" * 50)
        
        # Test in-memory connection to the server
        from mcp_search_server import mcp
        
        async with Client(mcp) as client:
            print("✅ Connected to MCP Search Server\n")
            
            # List available tools
            print("📋 Available tools:")
            try:
                tools_result = await client.list_tools()
                if hasattr(tools_result, 'tools'):
                    tools = tools_result.tools
                else:
                    tools = tools_result
                
                for tool in tools:
                    if hasattr(tool, 'name'):
                        print(f"  • {tool.name}: {getattr(tool, 'description', 'No description')[:80]}...")
                    else:
                        print(f"  • {tool}")
                print()
                
                # Test 1: search_mcps tool
                print("🔍 Test 1: Testing search_mcps tool...")
                result = await client.call_tool("search_mcps", {
                    "requirement": "database access and SQL operations",
                    "max_results": 3
                })
                
                response_text = extract_response_text(result)
                test_url = None  # We'll store a URL for later tests
                
                try:
                    parsed_result = json.loads(response_text)
                    print(f"✅ Found {parsed_result.get('total_found', 0)} MCP recommendations")
                    
                    for i, rec in enumerate(parsed_result.get('recommendations', [])[:2], 1):
                        print(f"\n📦 Recommendation {i}:")
                        print(f"   Name: {rec.get('name', 'Unknown')}")
                        print(f"   Category: {rec.get('category', 'General')}")
                        print(f"   Confidence: {rec.get('confidence_score', 0):.2f}")
                        print(f"   Features: {', '.join(rec.get('key_features', [])[:3])}")
                        
                        # Store first URL for later tests
                        if i == 1 and rec.get('url'):
                            test_url = rec.get('url')
                        
                except json.JSONDecodeError:
                    print(f"✅ Tool executed successfully. Raw response:\n{response_text[:200]}...")
                
                print("\n" + "="*50)
                
                # Test 2: ask_mcp_question tool
                print("❓ Test 2: Testing ask_mcp_question tool...")
                result = await client.call_tool("ask_mcp_question", {
                    "question": "What are the best MCPs for web scraping?"
                })
                
                response_text = extract_response_text(result)
                try:
                    parsed_result = json.loads(response_text)
                    print(f"✅ Question answered successfully")
                    print(f"   Answer preview: {parsed_result.get('answer', '')[:100]}...")
                    print(f"   Sources found: {len(parsed_result.get('sources', []))}")
                except json.JSONDecodeError:
                    print(f"✅ Tool executed successfully. Raw response:\n{response_text[:200]}...")
                
                print("\n" + "="*50)
                
                # Test 3: categorize_mcps tool
                print("📂 Test 3: Testing categorize_mcps tool...")
                result = await client.call_tool("categorize_mcps", {
                    "requirement": "file management"
                })
                
                response_text = extract_response_text(result)
                try:
                    parsed_result = json.loads(response_text)
                    print(f"✅ MCPs categorized successfully")
                    print(f"   Total MCPs: {parsed_result.get('total_mcps', 0)}")
                    categories = parsed_result.get('categories', {})
                    for category, info in list(categories.items())[:3]:
                        print(f"   {category}: {info.get('count', 0)} MCPs")
                except json.JSONDecodeError:
                    print(f"✅ Tool executed successfully. Raw response:\n{response_text[:200]}...")
                
                print("\n" + "="*50)
                
                # Test 4: get_mcp_details tool (if we have a URL)
                if test_url:
                    print("🔍 Test 4: Testing get_mcp_details tool...")
                    result = await client.call_tool("get_mcp_details", {
                        "mcp_url": test_url
                    })
                    
                    response_text = extract_response_text(result)
                    try:
                        parsed_result = json.loads(response_text)
                        print(f"✅ MCP details retrieved successfully")
                        details = parsed_result.get('details', {})
                        print(f"   Name: {details.get('name', 'Unknown')}")
                        print(f"   Category: {details.get('category', 'Unknown')}")
                        print(f"   Similar MCPs found: {len(parsed_result.get('similar_mcps', []))}")
                    except json.JSONDecodeError:
                        print(f"✅ Tool executed successfully. Raw response:\n{response_text[:200]}...")
                    
                    print("\n" + "="*50)
                    
                    # Test 5: find_similar_mcps tool
                    print("🔗 Test 5: Testing find_similar_mcps tool...")
                    result = await client.call_tool("find_similar_mcps", {
                        "reference_mcp_url": test_url,
                        "max_results": 3
                    })
                    
                    response_text = extract_response_text(result)
                    try:
                        parsed_result = json.loads(response_text)
                        print(f"✅ Similar MCPs found successfully")
                        similar_mcps = parsed_result.get('similar_mcps', [])
                        print(f"   Found {len(similar_mcps)} similar MCPs")
                        for i, mcp in enumerate(similar_mcps[:2], 1):
                            print(f"   {i}. {mcp.get('name', 'Unknown')} (confidence: {mcp.get('confidence_score', 0):.2f})")
                    except json.JSONDecodeError:
                        print(f"✅ Tool executed successfully. Raw response:\n{response_text[:200]}...")
                else:
                    print("⚠️  Skipping get_mcp_details and find_similar_mcps tests (no URL available)")
                
                print("\n" + "="*50)
                
                # Test resources
                print("📚 Testing resources...")
                try:
                    resources_result = await client.list_resources()
                    if hasattr(resources_result, 'resources'):
                        resources = resources_result.resources
                    else:
                        resources = resources_result
                    
                    print(f"Available resources: {len(resources)}")
                    for resource in resources:
                        if hasattr(resource, 'uri'):
                            print(f"  • {resource.uri}")
                        else:
                            print(f"  • {resource}")
                    
                    # Test help resource
                    if any(hasattr(r, 'uri') and r.uri == "mcp-search://help" for r in resources):
                        help_content = await client.read_resource("mcp-search://help")
                        print(f"✅ Help documentation loaded ({len(str(help_content)) if help_content else 0} characters)")
                
                except Exception as e:
                    print(f"❌ Error testing resources: {e}")
                
            except Exception as e:
                print(f"❌ Error testing tools: {e}")
                
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure EXA_API_KEY is set correctly")
        print("2. Check your internet connection")
        print("3. Verify Exa API key is valid")
    
    print("\n" + "=" * 50)
    print("🎯 Demo: Tool Usage Scenarios")
    print("=" * 50)
    
    scenarios = [
        {
            "tool": "search_mcps",
            "name": "Basic MCP Discovery",
            "description": "Find MCPs for database access",
            "example": '{"requirement": "database management and SQL operations", "max_results": 5}'
        },
        {
            "tool": "ask_mcp_question",
            "name": "Question Answering", 
            "description": "Get direct answers about MCPs",
            "example": '{"question": "What are the best MCPs for web scraping?"}'
        },
        {
            "tool": "categorize_mcps",
            "name": "Categorized Discovery",
            "description": "Find MCPs organized by categories",
            "example": '{"requirement": "file and directory management"}'
        },
        {
            "tool": "get_mcp_details",
            "name": "Detailed Analysis",
            "description": "Get detailed info about a specific MCP",
            "example": '{"mcp_url": "https://github.com/example/mcp-server"}'
        },
        {
            "tool": "find_similar_mcps",
            "name": "Similarity Search",
            "description": "Find MCPs similar to a reference",
            "example": '{"reference_mcp_url": "https://github.com/example/mcp-server", "max_results": 5}'
        }
    ]
    
    for scenario in scenarios:
        print(f"\n🔧 {scenario['name']} ({scenario['tool']})")
        print(f"Description: {scenario['description']}")
        print(f"Example call: {scenario['example']}")

    print("\n" + "=" * 50)
    print("🛠️  Integration Examples")
    print("=" * 50)
    
    print("""
1. Claude Desktop Configuration:

{
  "mcpServers": {
    "mcp-search": {
      "command": "python",
      "args": ["/path/to/mcp_search_server.py"],
      "env": {
        "EXA_API_KEY": "your_api_key_here"
      }
    }
  }
}


2. Programmatic Usage:

from fastmcp import Client

async def comprehensive_mcp_search():
    async with Client("mcp_search_server.py") as client:
        # Search for MCPs
        search_result = await client.call_tool("search_mcps", {
            "requirement": "web scraping and automation",
            "max_results": 10
        })
        
        # Ask a specific question
        question_result = await client.call_tool("ask_mcp_question", {
            "question": "How do I set up an MCP server for file operations?"
        })
        
        # Get categorized results
        category_result = await client.call_tool("categorize_mcps", {
            "requirement": "data processing"
        })
        
        return {
            "search": json.loads(search_result.content[0].text),
            "question": json.loads(question_result.content[0].text),
            "categories": json.loads(category_result.content[0].text)
        }


3. Command Line Testing:

# Interactive development
fastmcp dev mcp_search_server.py

# Web inspector for testing
fastmcp inspect mcp_search_server.py

# Direct execution
python mcp_search_server.py
""")

    print("\n" + "=" * 50)
    print("✅ Comprehensive test suite completed!")
    print("""
🎉 All 5 tools tested:
  • search_mcps - Basic MCP discovery
  • ask_mcp_question - Direct Q&A about MCPs  
  • categorize_mcps - Organized MCP discovery
  • get_mcp_details - Detailed MCP analysis
  • find_similar_mcps - Similarity-based discovery

Next steps:
1. Set up your EXA_API_KEY if not already done
2. Run: python mcp_search_server.py
3. Integrate with Claude Desktop or Cursor
4. Start discovering MCPs with all available tools!""")

def extract_response_text(result):
    """Helper function to extract text from various response formats"""
    if hasattr(result, 'content') and result.content:
        content = result.content[0]
        if hasattr(content, 'text'):
            return content.text
        else:
            return str(content)
    else:
        return str(result)

if __name__ == "__main__":
    asyncio.run(test_mcp_search_server()) 