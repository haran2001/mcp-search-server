#!/usr/bin/env python3
"""
Database MCP Discovery Script

This script helps you find the best MCPs for database CRUD operations.
It provides setup instructions and common database MCP recommendations.
"""

import os
import sys
import subprocess
import json
from typing import List, Dict

def check_requirements():
    """Check if required packages are installed"""
    print("🔍 Checking requirements...")
    
    try:
        import fastmcp
        import httpx
        print("✅ Required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Installing requirements...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True

def setup_exa_api():
    """Guide user through EXA API setup"""
    print("\n🔧 EXA API Setup")
    print("="*50)
    
    api_key = os.getenv("EXA_API_KEY")
    if api_key:
        print("✅ EXA_API_KEY is already set")
        return True
    
    print("To use the MCP search functionality, you need an EXA API key:")
    print("1. Visit: https://dashboard.exa.ai/")
    print("2. Sign up for a free account")
    print("3. Get your API key from the dashboard")
    print("4. Set it as an environment variable:")
    print("   Windows: set EXA_API_KEY=your_key_here")
    print("   Linux/Mac: export EXA_API_KEY=your_key_here")
    print()
    
    key = input("Enter your EXA API key (or press Enter to skip): ").strip()
    if key:
        os.environ["EXA_API_KEY"] = key
        print("✅ API key set for this session")
        return True
    else:
        print("⚠️  Skipping API key setup - search functionality will be limited")
        return False

def get_database_mcp_recommendations():
    """Provide curated list of database MCPs based on common patterns"""
    
    recommendations = {
        "SQLite MCPs": [
            {
                "name": "sqlite-mcp",
                "description": "Full-featured SQLite MCP with CRUD operations, schema management, and query execution",
                "features": ["CREATE, READ, UPDATE, DELETE operations", "Schema introspection", "Transaction support", "Query execution"],
                "typical_url": "https://github.com/*/sqlite-mcp",
                "confidence": "High"
            },
            {
                "name": "fastmcp-sqlite",
                "description": "FastMCP-based SQLite server for database operations",
                "features": ["Async operations", "Type safety", "Query builder", "Migration support"],
                "typical_url": "https://github.com/*/fastmcp-sqlite",
                "confidence": "High"
            }
        ],
        "PostgreSQL MCPs": [
            {
                "name": "postgres-mcp",
                "description": "PostgreSQL MCP server with full CRUD support and advanced features",
                "features": ["Full SQL support", "Connection pooling", "Transaction management", "JSON operations"],
                "typical_url": "https://github.com/*/postgres-mcp",
                "confidence": "High"
            },
            {
                "name": "postgresql-mcp-server",
                "description": "Enterprise-grade PostgreSQL MCP with security features",
                "features": ["Role-based access", "Query optimization", "Backup integration", "Monitoring"],
                "typical_url": "https://github.com/*/postgresql-mcp-server",
                "confidence": "Medium"
            }
        ],
        "MySQL MCPs": [
            {
                "name": "mysql-mcp",
                "description": "MySQL MCP server for database operations and management",
                "features": ["CRUD operations", "Index management", "Performance monitoring", "Replication support"],
                "typical_url": "https://github.com/*/mysql-mcp",
                "confidence": "High"
            }
        ],
        "General Database MCPs": [
            {
                "name": "database-mcp",
                "description": "Multi-database MCP supporting SQLite, PostgreSQL, and MySQL",
                "features": ["Multiple DB support", "Unified interface", "Schema management", "Data migration"],
                "typical_url": "https://github.com/*/database-mcp",
                "confidence": "High"
            },
            {
                "name": "sql-mcp-server",
                "description": "Generic SQL MCP with support for various database engines",
                "features": ["Cross-database queries", "Query caching", "Result formatting", "Data export"],
                "typical_url": "https://github.com/*/sql-mcp-server",
                "confidence": "Medium"
            }
        ]
    }
    
    return recommendations

async def search_database_mcps():
    """Search for database MCPs using the MCP search server"""
    
    print("\n🔍 Searching for Database MCPs...")
    print("="*50)
    
    try:
        from mcp_search_server import get_exa_client, mcp_analyzer
        
        client = get_exa_client()
        
        # Search queries for different database types
        search_queries = [
            "SQLite MCP server CRUD operations",
            "PostgreSQL MCP server database",
            "MySQL MCP server Model Context Protocol", 
            "database MCP server SQL operations",
            "FastMCP database SQLite PostgreSQL"
        ]
        
        all_results = []
        
        for query in search_queries:
            try:
                print(f"Searching: {query}")
                results = await client.search(
                    query=query,
                    num_results=5,
                    include_domains=["github.com"],
                    include_text=True,
                    include_summary=True
                )
                
                recommendations = mcp_analyzer.analyze_search_results(results)
                all_results.extend(recommendations)
                
            except Exception as e:
                print(f"  Error searching '{query}': {e}")
        
        # Remove duplicates and sort by confidence
        unique_results = {}
        for rec in all_results:
            if rec.url not in unique_results or rec.confidence_score > unique_results[rec.url].confidence_score:
                unique_results[rec.url] = rec
        
        sorted_results = sorted(unique_results.values(), key=lambda x: x.confidence_score, reverse=True)
        
        print(f"\n✅ Found {len(sorted_results)} unique database MCPs:")
        for i, rec in enumerate(sorted_results[:10], 1):
            print(f"\n{i}. {rec.name}")
            print(f"   URL: {rec.url}")
            print(f"   Description: {rec.description[:100]}...")
            print(f"   Confidence: {rec.confidence_score:.2f}")
            print(f"   Features: {', '.join(rec.key_features[:3])}")
        
        return sorted_results
        
    except Exception as e:
        print(f"❌ Error during search: {e}")
        return []

def display_curated_recommendations():
    """Display curated database MCP recommendations"""
    
    print("\n📦 Curated Database MCP Recommendations")
    print("="*50)
    
    recommendations = get_database_mcp_recommendations()
    
    for category, mcps in recommendations.items():
        print(f"\n🗂️  {category}")
        print("-" * len(category))
        
        for i, mcp in enumerate(mcps, 1):
            print(f"\n{i}. {mcp['name']}")
            print(f"   Description: {mcp['description']}")
            print(f"   Key Features:")
            for feature in mcp['features']:
                print(f"     • {feature}")
            print(f"   Confidence: {mcp['confidence']}")
            print(f"   Search Pattern: {mcp['typical_url']}")

def generate_search_commands():
    """Generate MCP search commands for database operations"""
    
    print("\n🛠️  MCP Search Commands for Database Operations")
    print("="*50)
    
    commands = [
        {
            "purpose": "Find SQLite MCPs",
            "command": 'search_mcps(requirement="SQLite database CRUD operations", max_results=5)',
            "description": "Search for MCPs that work with SQLite databases"
        },
        {
            "purpose": "Find PostgreSQL MCPs", 
            "command": 'search_mcps(requirement="PostgreSQL database management", max_results=5)',
            "description": "Search for MCPs that work with PostgreSQL"
        },
        {
            "purpose": "Find MySQL MCPs",
            "command": 'search_mcps(requirement="MySQL database operations", max_results=5)', 
            "description": "Search for MCPs that work with MySQL"
        },
        {
            "purpose": "Find general database MCPs",
            "command": 'search_mcps(requirement="database CRUD SQL operations", max_results=10)',
            "description": "Search for MCPs that work with multiple database types"
        },
        {
            "purpose": "Categorize database MCPs",
            "command": 'categorize_mcps(requirement="database management")',
            "description": "Get database MCPs organized by categories"
        }
    ]
    
    for cmd in commands:
        print(f"\n🎯 {cmd['purpose']}")
        print(f"   Command: {cmd['command']}")
        print(f"   Description: {cmd['description']}")

async def main():
    """Main function to run the database MCP discovery"""
    
    print("🗄️  Database MCP Discovery Tool")
    print("=" * 50)
    print("Find the best MCPs for database CRUD operations\n")
    
    # Check requirements
    if not check_requirements():
        return
    
    # Setup EXA API
    has_api_key = setup_exa_api()
    
    # Display curated recommendations
    display_curated_recommendations()
    
    # Generate search commands
    generate_search_commands()
    
    if has_api_key:
        print("\n" + "="*50)
        response = input("Do you want to run live search for database MCPs? (y/n): ").strip().lower()
        if response == 'y':
            await search_database_mcps()
    else:
        print("\n⚠️  Live search unavailable without EXA API key")
        print("Set EXA_API_KEY environment variable to enable search functionality")
    
    print("\n✅ Database MCP discovery complete!")
    print("\n📚 Next steps:")
    print("1. Set up your EXA API key if you haven't already")
    print("2. Use the MCP search server to find specific database MCPs")
    print("3. Test MCPs with your database requirements")
    print("4. Install and configure chosen MCPs in your environment")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 