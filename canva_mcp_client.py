#!/usr/bin/env python3
"""
Canva MCP Client - Entry point for DSH skill integration.

Connects to Canva's MCP server and enables agents to create designs,
manage assets, and perform other Canva operations via the Model Context Protocol.

Usage in DSH:
  - This file is referenced by the canva-mcp skill definition
  - DSH's MCP integration will invoke this client when the agent
    requests Canva operations
"""

import asyncio
import json
import sys
from mcp import ClientSession, StdioServerParameters, ListToolsResult, CallToolResult


def get_server_params():
    """Configure the Canva MCP server connection via mcp-remote."""
    return StdioServerParameters(
        command="npx",
        args=["mcp-remote@latest", "https://mcp.canva.com/mcp"],
        env=None
    )


async def run_client():
    """Run the Canva MCP client session and return available tools."""
    server_params = get_server_params()
    
    async with ClientSession(server_params) as session:
        # Initialize the session
        await session.initialize()
        
        # List available tools
        list_result: ListToolsResult = await session.list_tools()
        
        print("=" * 60)
        print("Canva MCP Tools Available:")
        print("=" * 60)
        
        tools = list_result.tools
        for tool in tools:
            print(f"\n  • {tool.name}")
            if tool.description:
                print(f"    Description: {tool.description}")
            if tool.inputSchema:
                params = tool.inputSchema.get("properties", {})
                print(f"    Parameters: {list(params.keys())}")
        
        print(f"\n✅ Connected! Found {len(tools)} tools.")
        print(f"📡 Server: https://mcp.canva.com/mcp")
        
        # Print tool names for reference
        tool_names = [t.name for t in tools]
        print(f"\nAvailable tools: {', '.join(tool_names)}")
        
        return tools, session


async def generate_design(session, tools, description: str, output_format: str = "PNG"):
    """Generate a design from a text description."""
    # Check if generate-design tool is available
    generate_tool = next((t for t in tools if t.name == "generate-design"), None)
    
    if not generate_tool:
        print("❌ generate-design tool not available")
        return None
    
    print(f"\n🎨 Generating design: {description}")
    print(f"   Output format: {output_format}")
    
    try:
        result: CallToolResult = await session.call_tool(
            name="generate-design",
            arguments={
                "description": description,
                "output_format": output_format
            }
        )
        
        print(f"\n✅ Design generation initiated!")
        
        # Process result
        if result.content:
            for content_block in result.content:
                if hasattr(content_block, 'text') and content_block.text:
                    text = content_block.text
                    # Try to parse JSON response
                    try:
                        data = json.loads(text)
                        if 'design' in data or 'candidates' in data:
                            print(f"   Design candidates returned: {json.dumps(data, indent=2)[:300]}...")
                        else:
                            print(f"   Output: {text[:300]}...")
                    except:
                        print(f"   Output: {text[:300]}...")
                elif hasattr(content_block, 'data') and content_block.data:
                    print(f"   Data: {str(content_block.data)[:200]}...")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Error generating design: {type(e).__name__}: {e}")
        return None


async def search_designs(session, tools, query: str = None):
    """Search for existing designs in the user's Canva account."""
    search_tool = next((t for t in tools if t.name == "search-designs"), None)
    
    if not search_tool:
        print("❌ search-designs tool not available")
        return None
    
    suffix = f' - "{query}"' if query else ''
    print(f"\n🔍 Searching designs{suffix}")
    
    try:
        result: CallToolResult = await session.call_tool(
            name="search-designs",
            arguments={"query": query} if query else {}
        )
        
        print(f"✅ Search complete!")
        
        if result.content:
            for content_block in result.content:
                if hasattr(content_block, 'text') and content_block.text:
                    text = content_block.text
                    try:
                        data = json.loads(text)
                        total = data.get('total', '?')
                        designs = data.get('designs', [])
                        print(f"   Found {total} designs")
                        for d in designs[:5]:
                            title = d.get('title', 'Untitled')
                            did = d.get('id', '?')
                            print(f"   - {title} ({did})")
                    except:
                        print(f"   Raw output: {text[:300]}...")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Error searching designs: {type(e).__name__}: {e}")
        return None


async def export_design(session, tools, design_id: str, format_type: str = "PNG"):
    """Export a design to the specified format."""
    export_tool = next((t for t in tools if t.name == "export-design"), None)
    
    if not export_tool:
        print("❌ export-design tool not available")
        return None
    
    print(f"\n📤 Exporting design {design_id} as {format_type}")
    
    try:
        result: CallToolResult = await session.call_tool(
            name="export-design",
            arguments={
                "design_id": design_id,
                "format": format_type
            }
        )
        
        print(f"✅ Export initiated!")
        
        if result.content:
            for content_block in result.content:
                if hasattr(content_block, 'text') and content_block.text:
                    print(f"   Output: {content_block.text[:300]}...")
                elif hasattr(content_block, 'download_url') and content_block.download_url:
                    print(f"   Download URL: {content_block.download_url}")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Error exporting design: {type(e).__name__}: {e}")
        return None


async def main():
    """Main entry point."""
    print("Canva MCP Client for DSH")
    print("=" * 60)
    print(f"\nConnecting to Canva MCP server...")
    
    try:
        # Run the client session
        tools, session = await run_client()
        
        if not tools:
            print("❌ No tools available - check authentication")
            return
        
        # Example operations - in real use, these would be triggered by agent prompts
        print("\n" + "=" * 60)
        print("Example Operations:")
        print("=" * 60)
        
        # 1. Search designs
        await search_designs(session, tools, query="")
        
        # 2. Generate design (commented out - requires user prompt)
        # await generate_design(session, tools, 
        #   "Instagram carousel with 3 slides about AI-powered design tips, brand colors blue and white, modern minimal style")
        
        # 3. Export design (would need design_id from generation above)
        # await export_design(session, tools, "design_12345", "PNG")
        
        print("\n⚠️  Operations above are examples - agent prompts will trigger these.")
        print("💡 Use the Canva MCP skill in DSH to create designs via natural language.")
        
    except Exception as e:
        print(f"\n❌ Client error: {type(e).__name__}: {e}")
        print("\nTroubleshooting:")
        print("  1. Ensure you have a Canva account")
        print("  2. First connection requires OAuth authentication")
        print("  3. Some tools require Canva Pro plan")
        print("  4. Check rate limits and AI credit allowance")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nClient stopped by user.")
        sys.exit(0)
