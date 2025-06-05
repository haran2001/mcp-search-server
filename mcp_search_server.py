"""
MCP Search Server

An MCP server that uses the Exa search API to find and recommend MCPs (Model Context Protocol servers) 
based on user requirements. Built with FastMCP.

Features:
- Search for existing MCP servers based on user requirements
- Analyze search results to provide structured recommendations
- Get detailed information about specific MCPs
- Find similar MCPs to a given reference

Author: Hari Ayappane
"""

import asyncio
import json
import os
import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from urllib.parse import urlparse

import httpx
from mcp.server.fastmcp import FastMCP, Context

import dotenv
dotenv.load_dotenv()

# Initialize the MCP server
mcp = FastMCP(
    name="MCP Search Server",
    version="1.0.0",
    description="Search and discover MCP servers using Exa AI search"
)

@dataclass
class MCPRecommendation:
    """Represents a recommended MCP server"""
    name: str
    description: str
    url: str
    repository: Optional[str] = None
    category: Optional[str] = None
    confidence_score: float = 0.0
    key_features: List[str] = None
    installation_notes: Optional[str] = None

class ExaSearchClient:
    """Client for interacting with Exa search API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.exa.ai"
        self.headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }
    
    async def search(
        self, 
        query: str, 
        num_results: int = 10,
        include_domains: List[str] = None,
        search_type: str = "auto",
        include_text: bool = True,
        include_summary: bool = True
    ) -> Dict[str, Any]:
        """Search the web using Exa API"""
        
        payload = {
            "query": query,
            "numResults": num_results,
            "type": search_type,
            "contents": {
                "text": include_text,
                "summary": include_summary,
                "highlights": True
            }
        }
        
        if include_domains:
            payload["includeDomains"] = include_domains
            
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/search",
                headers=self.headers,
                json=payload,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    async def get_answer(self, query: str) -> Dict[str, Any]:
        """Get a direct answer using Exa Answer API"""
        
        payload = {
            "query": query,
            "text": True
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/answer",
                headers=self.headers,
                json=payload,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    async def find_similar(self, url: str, num_results: int = 5) -> Dict[str, Any]:
        """Find similar content to a given URL"""
        
        payload = {
            "url": url,
            "numResults": num_results,
            "contents": {
                "text": True,
                "summary": True
            }
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/findSimilar",
                headers=self.headers,
                json=payload,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()

class MCPAnalyzer:
    """Analyzes search results to identify and rank MCP servers"""
    
    MCP_INDICATORS = [
        "model context protocol", "mcp server", "mcp-server", "fastmcp",
        "claude desktop", "cursor mcp", "anthropic mcp", "mcp tool",
        "mcp client", "context protocol", "llm tool", "ai assistant tool"
    ]
    
    REPOSITORY_PATTERNS = [
        r"github\.com/[\w-]+/[\w-]+",
        r"gitlab\.com/[\w-]+/[\w-]+",
        r"bitbucket\.org/[\w-]+/[\w-]+"
    ]
    
    def analyze_search_results(self, results: Dict[str, Any]) -> List[MCPRecommendation]:
        """Analyze search results and extract MCP recommendations"""
        
        recommendations = []
        
        for result in results.get("results", []):
            # Calculate relevance score
            score = self._calculate_relevance_score(result)
            
            if score > 0.3:  # Threshold for MCP relevance
                recommendation = self._extract_mcp_info(result, score)
                if recommendation:
                    recommendations.append(recommendation)
        
        # Sort by confidence score
        recommendations.sort(key=lambda x: x.confidence_score, reverse=True)
        return recommendations
    
    def _calculate_relevance_score(self, result: Dict[str, Any]) -> float:
        """Calculate how relevant a result is to MCP"""
        
        score = 0.0
        text_content = f"{result.get('title', '')} {result.get('text', '')} {result.get('summary', '')}".lower()
        
        # Check for MCP indicators
        for indicator in self.MCP_INDICATORS:
            if indicator.lower() in text_content:
                score += 0.2
        
        # Boost GitHub repositories
        if "github.com" in result.get('url', ''):
            score += 0.3
        
        # Boost if it's a README or documentation
        url = result.get('url', '').lower()
        if any(keyword in url for keyword in ['readme', 'docs', 'documentation']):
            score += 0.1
        
        # Boost based on Exa's own score
        exa_score = result.get('score', 0)
        score += exa_score * 0.5
        
        return min(score, 1.0)
    
    def _extract_mcp_info(self, result: Dict[str, Any], score: float) -> Optional[MCPRecommendation]:
        """Extract MCP information from a search result"""
        
        try:
            url = result.get('url', '')
            title = result.get('title', '')
            text = result.get('text', '')
            summary = result.get('summary', '')
            
            # Extract repository URL
            repository = self._extract_repository(url, text)
            
            # Extract name (try to clean up the title)
            name = self._extract_name(title, url)
            
            # Extract description
            description = summary or text[:200] + "..." if text else "No description available"
            
            # Extract features
            features = self._extract_features(text)
            
            # Determine category
            category = self._determine_category(text, title)
            
            return MCPRecommendation(
                name=name,
                description=description,
                url=url,
                repository=repository,
                category=category,
                confidence_score=score,
                key_features=features
            )
        
        except Exception as e:
            print(f"Error extracting MCP info: {e}")
            return None
    
    def _extract_repository(self, url: str, text: str) -> Optional[str]:
        """Extract repository URL from content"""
        
        # Check if URL itself is a repository
        for pattern in self.REPOSITORY_PATTERNS:
            if re.search(pattern, url):
                return url
        
        # Look for repository links in text
        for pattern in self.REPOSITORY_PATTERNS:
            match = re.search(pattern, text)
            if match:
                return f"https://{match.group()}"
        
        return None
    
    def _extract_name(self, title: str, url: str) -> str:
        """Extract a clean name for the MCP"""
        
        # Try to extract from GitHub URL
        if "github.com" in url:
            parts = url.split("/")
            if len(parts) >= 5:
                return parts[4]  # Repository name
        
        # Clean up title
        name = title.replace(" - GitHub", "").replace("GitHub - ", "")
        return name[:50] if name else "Unknown MCP"
    
    def _extract_features(self, text: str) -> List[str]:
        """Extract key features from text"""
        
        features = []
        text_lower = text.lower()
        
        feature_keywords = {
            "Database": ["database", "sql", "sqlite", "postgres", "mysql"],
            "Web Scraping": ["scraping", "crawling", "web data", "selenium"],
            "File System": ["file system", "files", "directories", "fs"],
            "API Integration": ["api", "rest", "graphql", "webhook"],
            "Data Processing": ["data processing", "csv", "json", "xml"],
            "Search": ["search", "elasticsearch", "indexing"],
            "Documentation": ["documentation", "docs", "readme"],
            "Communication": ["slack", "discord", "email", "notifications"],
            "Development Tools": ["git", "deployment", "ci/cd", "testing"]
        }
        
        for category, keywords in feature_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                features.append(category)
        
        return features[:5]  # Limit to top 5 features
    
    def _determine_category(self, text: str, title: str) -> str:
        """Determine the category of the MCP"""
        
        content = f"{title} {text}".lower()
        
        categories = {
            "Database & Storage": ["database", "sql", "storage", "data"],
            "Web & APIs": ["web", "api", "http", "rest", "scraping"],
            "File System": ["file", "filesystem", "directory"],
            "Communication": ["slack", "discord", "email", "chat"],
            "Development Tools": ["git", "development", "code", "deploy"],
            "AI & ML": ["ai", "machine learning", "model", "llm"],
            "Utilities": ["utility", "tool", "helper"]
        }
        
        for category, keywords in categories.items():
            if any(keyword in content for keyword in keywords):
                return category
        
        return "General"

# Initialize clients
exa_client = None
mcp_analyzer = MCPAnalyzer()

def get_exa_client() -> ExaSearchClient:
    """Get or create Exa client"""
    global exa_client
    
    if exa_client is None:
        api_key = os.getenv("EXA_API_KEY")
        if not api_key:
            raise ValueError("EXA_API_KEY environment variable is required")
        exa_client = ExaSearchClient(api_key)
    
    return exa_client

@mcp.tool()
async def search_mcps(
    requirement: str,
    max_results: int = 10,
    include_github_only: bool = False,
    ctx: Context = None
) -> str:
    """
    Search for MCP servers that match specific requirements.
    
    Args:
        requirement: Description of what kind of MCP you need (e.g., "database access", "web scraping", "file management")
        max_results: Maximum number of results to return (default: 10)
        include_github_only: If True, only search GitHub repositories (default: False)
    
    Returns:
        JSON string containing list of recommended MCP servers with details
    """
    
    try:
        if ctx:
            await ctx.info(f"Searching for MCPs related to: {requirement}")
        
        client = get_exa_client()
        
        # Construct search query
        search_query = f"MCP server {requirement} Model Context Protocol"
        if include_github_only:
            search_query += " site:github.com"
        
        # Perform search
        search_results = await client.search(
            query=search_query,
            num_results=max_results * 2,  # Get more results to filter
            include_domains=["github.com", "docs.anthropic.com", "modelcontextprotocol.io"] if include_github_only else None,
            include_text=True,
            include_summary=True
        )
        
        if ctx:
            await ctx.info(f"Found {len(search_results.get('results', []))} initial results")
        
        # Analyze results
        recommendations = mcp_analyzer.analyze_search_results(search_results)
        
        # Limit to requested number
        recommendations = recommendations[:max_results]
        
        if ctx:
            await ctx.info(f"Filtered to {len(recommendations)} relevant MCP recommendations")
        
        # Format results
        result = {
            "query": requirement,
            "total_found": len(recommendations),
            "recommendations": [
                {
                    "name": rec.name,
                    "description": rec.description,
                    "url": rec.url,
                    "repository": rec.repository,
                    "category": rec.category,
                    "confidence_score": round(rec.confidence_score, 2),
                    "key_features": rec.key_features,
                    "installation_notes": rec.installation_notes
                }
                for rec in recommendations
            ]
        }
        
        return json.dumps(result, indent=2)
    
    except Exception as e:
        error_msg = f"Error searching for MCPs: {str(e)}"
        if ctx:
            await ctx.error(error_msg)
        return json.dumps({"error": error_msg})

@mcp.tool()
async def get_mcp_details(
    mcp_url: str,
    ctx: Context = None
) -> str:
    """
    Get detailed information about a specific MCP server.
    
    Args:
        mcp_url: URL of the MCP server or repository
    
    Returns:
        JSON string with detailed information about the MCP
    """
    
    try:
        if ctx:
            await ctx.info(f"Getting detailed information for: {mcp_url}")
        
        client = get_exa_client()
        
        # Search for detailed information about this specific MCP
        domain = urlparse(mcp_url).netloc
        search_query = f"site:{domain} {mcp_url} MCP server documentation setup"
        
        search_results = await client.search(
            query=search_query,
            num_results=5,
            include_text=True,
            include_summary=True
        )
        
        # Also try to find similar MCPs
        try:
            similar_results = await client.find_similar(mcp_url, num_results=3)
        except:
            similar_results = {"results": []}
        
        # Analyze the main result
        recommendations = mcp_analyzer.analyze_search_results(search_results)
        main_rec = recommendations[0] if recommendations else None
        
        # Analyze similar MCPs
        similar_mcps = mcp_analyzer.analyze_search_results(similar_results)
        
        result = {
            "url": mcp_url,
            "details": {
                "name": main_rec.name if main_rec else "Unknown",
                "description": main_rec.description if main_rec else "No description available",
                "category": main_rec.category if main_rec else "Unknown",
                "key_features": main_rec.key_features if main_rec else [],
                "confidence_score": main_rec.confidence_score if main_rec else 0.0
            },
            "installation_info": search_results.get("results", [{}])[0].get("text", "")[:500] + "...",
            "similar_mcps": [
                {
                    "name": rec.name,
                    "url": rec.url,
                    "description": rec.description[:100] + "...",
                    "confidence_score": round(rec.confidence_score, 2)
                }
                for rec in similar_mcps[:3]
            ]
        }
        
        return json.dumps(result, indent=2)
    
    except Exception as e:
        error_msg = f"Error getting MCP details: {str(e)}"
        if ctx:
            await ctx.error(error_msg)
        return json.dumps({"error": error_msg})

@mcp.tool()
async def find_similar_mcps(
    reference_mcp_url: str,
    max_results: int = 5,
    ctx: Context = None
) -> str:
    """
    Find MCP servers similar to a reference MCP.
    
    Args:
        reference_mcp_url: URL of the reference MCP server
        max_results: Maximum number of similar MCPs to return
    
    Returns:
        JSON string with list of similar MCPs
    """
    
    try:
        if ctx:
            await ctx.info(f"Finding MCPs similar to: {reference_mcp_url}")
        
        client = get_exa_client()
        
        # Find similar content
        similar_results = await client.find_similar(
            reference_mcp_url,
            num_results=max_results * 2
        )
        
        # Analyze results to filter for MCPs
        recommendations = mcp_analyzer.analyze_search_results(similar_results)
        recommendations = recommendations[:max_results]
        
        result = {
            "reference_url": reference_mcp_url,
            "similar_mcps": [
                {
                    "name": rec.name,
                    "description": rec.description,
                    "url": rec.url,
                    "repository": rec.repository,
                    "category": rec.category,
                    "confidence_score": round(rec.confidence_score, 2),
                    "key_features": rec.key_features
                }
                for rec in recommendations
            ]
        }
        
        return json.dumps(result, indent=2)
    
    except Exception as e:
        error_msg = f"Error finding similar MCPs: {str(e)}"
        if ctx:
            await ctx.error(error_msg)
        return json.dumps({"error": error_msg})

@mcp.tool()
async def ask_mcp_question(
    question: str,
    ctx: Context = None
) -> str:
    """
    Ask a specific question about MCP servers and get a direct answer.
    
    Args:
        question: Your question about MCP servers, tools, or recommendations
    
    Returns:
        Direct answer with citations
    """
    
    try:
        if ctx:
            await ctx.info(f"Getting answer for: {question}")
        
        client = get_exa_client()
        
        # Use Exa's Answer API for direct responses
        answer_response = await client.get_answer(f"Model Context Protocol MCP {question}")
        
        result = {
            "question": question,
            "answer": answer_response.get("answer", "No answer available"),
            "sources": [
                {
                    "title": citation.get("title", ""),
                    "url": citation.get("url", ""),
                    "author": citation.get("author", "")
                }
                for citation in answer_response.get("citations", [])
            ]
        }
        
        return json.dumps(result, indent=2)
    
    except Exception as e:
        error_msg = f"Error getting answer: {str(e)}"
        if ctx:
            await ctx.error(error_msg)
        return json.dumps({"error": error_msg})

@mcp.tool()
async def categorize_mcps(
    requirement: str,
    ctx: Context = None
) -> str:
    """
    Get MCPs organized by categories for a specific requirement.
    
    Args:
        requirement: Your requirement description
    
    Returns:
        JSON with MCPs organized by categories
    """
    
    try:
        if ctx:
            await ctx.info(f"Categorizing MCPs for: {requirement}")
        
        # Search for MCPs
        search_result = await search_mcps(requirement, max_results=20, ctx=ctx)
        search_data = json.loads(search_result)
        
        if "error" in search_data:
            return search_result
        
        # Group by category
        categories = {}
        for rec in search_data.get("recommendations", []):
            category = rec.get("category", "General")
            if category not in categories:
                categories[category] = []
            categories[category].append(rec)
        
        result = {
            "requirement": requirement,
            "categories": {
                category: {
                    "count": len(mcps),
                    "mcps": mcps
                }
                for category, mcps in categories.items()
            },
            "total_mcps": len(search_data.get("recommendations", []))
        }
        
        return json.dumps(result, indent=2)
    
    except Exception as e:
        error_msg = f"Error categorizing MCPs: {str(e)}"
        if ctx:
            await ctx.error(error_msg)
        return json.dumps({"error": error_msg})

# Resource for providing help and documentation
@mcp.resource("mcp-search://help")
async def get_help():
    """Get help documentation for the MCP Search Server"""
    
    help_content = """
# MCP Search Server Help

This server helps you discover and research MCP (Model Context Protocol) servers using Exa AI search.

## Available Tools:

### 1. search_mcps
Search for MCP servers based on your requirements.
**Example**: "I need an MCP for database access"

### 2. get_mcp_details  
Get detailed information about a specific MCP server.
**Example**: Provide a GitHub URL or MCP server URL

### 3. find_similar_mcps
Find MCP servers similar to a reference MCP.
**Example**: Provide a reference MCP URL

### 4. ask_mcp_question
Ask specific questions about MCP servers.
**Example**: "What are the best MCPs for web scraping?"

### 5. categorize_mcps
Get MCPs organized by categories for your requirement.
**Example**: "file management" → returns MCPs grouped by type

## Setup Requirements:
- Set EXA_API_KEY environment variable with your Exa API key
- Get API key from: https://dashboard.exa.ai/

## Usage Tips:
- Be specific about your requirements for better results
- Check the confidence scores to gauge relevance
- Use categorize_mcps for broader exploration
- Ask follow-up questions using ask_mcp_question
"""
    
    return help_content


if __name__ == "__main__":
    # Check for API key
    if not os.getenv("EXA_API_KEY"):
        print("Warning: EXA_API_KEY environment variable not set!")
        print("Get your API key from: https://dashboard.exa.ai/")
        print("Set it with: export EXA_API_KEY=your_key_here")
    
    mcp.run() 