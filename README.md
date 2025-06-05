# MCP Search Server - Comprehensive Documentation 🚀

An intelligent MCP (Model Context Protocol) server that helps you discover and research MCP servers using the powerful Exa AI search engine. Built with FastMCP for seamless integration with AI assistants like Claude, Cursor, and more.

## Table of Contents

1. [Features](#-features)
2. [Architecture](#-architecture) 
3. [Quick Start](#-quick-start)
4. [Installation Guide](#-installation-guide)
5. [Usage Guide](#-usage-guide)
6. [Configuration](#-configuration)
7. [API Reference](#-api-reference)
8. [Integration](#-integration)
9. [Troubleshooting](#-troubleshooting)
10. [Contributing](#-contributing)
11. [License](#-license)

---

## 🌟 Features

- **Smart MCP Discovery**: Search for MCP servers based on your specific requirements
- **Intelligent Analysis**: Automatically analyzes and ranks search results for MCP relevance
- **Detailed Information**: Get comprehensive details about specific MCP servers
- **Similar MCPs**: Find MCP servers similar to ones you already know
- **Category Organization**: MCPs organized by functional categories
- **Direct Q&A**: Ask specific questions about MCP servers and get direct answers
- **Multiple Search Modes**: Support for both broad and GitHub-focused searches

## 🏗️ Architecture

The server consists of several key components:

### Core Components

1. **ExaSearchClient**: Handles interaction with Exa's search, answer, and find-similar APIs
2. **MCPAnalyzer**: Intelligent analysis engine that:
   - Identifies MCP-relevant content from search results
   - Calculates confidence scores based on multiple factors
   - Extracts structured information (features, categories, etc.)
   - Filters and ranks recommendations

3. **MCPRecommendation**: Data structure representing discovered MCPs with:
   - Name, description, and URLs
   - Repository information
   - Confidence scores
   - Key features and categories
   - Installation notes

### Available Tools

| Tool | Description | Use Case |
|------|-------------|----------|
| `search_mcps` | Search for MCPs based on requirements | "I need an MCP for database access" |
| `get_mcp_details` | Get detailed info about a specific MCP | Analyze a specific GitHub repo |
| `find_similar_mcps` | Find MCPs similar to a reference | Discover alternatives to known MCPs |
| `ask_mcp_question` | Ask specific questions about MCPs | "What are the best MCPs for web scraping?" |
| `categorize_mcps` | Get MCPs organized by categories | Explore MCPs by functional area |

---

## 🚀 Quick Start

### Prerequisites

1. **Python 3.10+**
2. **Exa API Key** - Get one from [Exa Dashboard](https://dashboard.exa.ai/)

### Installation

1. **Clone and setup:**
   ```bash
   git clone <this-repo>
   cd mcp-search-server
   pip install -r requirements.txt
   ```

2. **Set your Exa API key:**
   ```bash
   export EXA_API_KEY=your_api_key_here
   ```

3. **Run the server:**
   ```bash
   python mcp_search_server.py
   ```

### Testing with FastMCP CLI

```bash
# Test the server interactively
fastmcp dev mcp_search_server.py

# Or inspect with web UI
fastmcp inspect mcp_search_server.py
```

---

## 📦 Installation Guide

This guide covers installing and setting up the MCP Search Server on different operating systems.

### 📋 Prerequisites

#### Required:
- **Python 3.10 or higher**
- **Exa API Key** (get from [Exa Dashboard](https://dashboard.exa.ai/))
- **Internet connection** for search functionality

#### Optional:
- **Git** for cloning repositories
- **FastMCP CLI** for testing and development

### 🐍 Python Installation

#### Windows

**Option 1: Microsoft Store (Recommended)**
1. Open Microsoft Store
2. Search for "Python 3.11" or "Python 3.12"
3. Click "Get" to install
4. Verify installation: `python --version`

**Option 2: Python.org**
1. Visit [python.org/downloads](https://python.org/downloads)
2. Download latest Python 3.10+ for Windows
3. Run installer with "Add to PATH" checked
4. Verify: `python --version`

**Option 3: Chocolatey**
```powershell
# Install Chocolatey first (if not installed)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install Python
choco install python
```

#### macOS

**Option 1: Homebrew (Recommended)**
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.11
```

**Option 2: Python.org**
1. Visit [python.org/downloads](https://python.org/downloads)
2. Download latest Python 3.10+ for macOS
3. Run the installer
4. Verify: `python3 --version`

#### Linux (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install Python 3.11
sudo apt install python3.11 python3.11-pip python3.11-venv

# Verify installation
python3.11 --version
```

#### Linux (CentOS/RHEL/Fedora)

```bash
# Fedora
sudo dnf install python311 python311-pip

# CentOS/RHEL (with EPEL)
sudo yum install python311 python311-pip
```

### 🚀 MCP Search Server Installation

#### Method 1: Direct Download and Setup

1. **Download the files:**
   ```bash
   # Create project directory
   mkdir mcp-search-server
   cd mcp-search-server
   
   # Download files (or copy from this project)
   # - mcp_search_server.py
   # - requirements.txt
   # - README.md
   # - test_mcp_search.py
   ```

2. **Install dependencies:**
   ```bash
   # Using pip
   pip install -r requirements.txt
   
   # Or install manually
   pip install fastmcp>=2.0.0 httpx>=0.25.0
   ```

3. **Set up environment:**
   ```bash
   # Linux/Mac
   export EXA_API_KEY=your_exa_api_key_here
   
   # Windows Command Prompt
   set EXA_API_KEY=your_exa_api_key_here
   
   # Windows PowerShell
   $env:EXA_API_KEY="your_exa_api_key_here"
   ```

#### Method 2: Using Virtual Environment (Recommended)

1. **Create virtual environment:**
   ```bash
   # Create virtual environment
   python -m venv mcp-search-env
   
   # Activate it
   # Linux/Mac:
   source mcp-search-env/bin/activate
   
   # Windows:
   mcp-search-env\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run server:**
   ```bash
   python mcp_search_server.py
   ```

### 🔑 Exa API Key Setup

#### 1. Get API Key
1. Visit [Exa Dashboard](https://dashboard.exa.ai/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `exa_`)

#### 2. Set Environment Variable

**Temporary (Current Session)**
```bash
# Linux/Mac
export EXA_API_KEY=exa_your_key_here

# Windows Command Prompt
set EXA_API_KEY=exa_your_key_here

# Windows PowerShell
$env:EXA_API_KEY="exa_your_key_here"
```

**Permanent Setup**

**Linux/Mac (~/.bashrc or ~/.zshrc):**
```bash
echo 'export EXA_API_KEY=exa_your_key_here' >> ~/.bashrc
source ~/.bashrc
```

**Windows (System Environment Variables):**
1. Open "Environment Variables" in Control Panel
2. Add new User Variable:
   - Name: `EXA_API_KEY`
   - Value: `exa_your_key_here`
3. Restart terminal/applications

### ✅ Verification and Testing

#### 1. Basic Installation Test
```bash
# Test Python installation
python --version

# Test package imports
python -c "import fastmcp, httpx; print('Dependencies OK')"
```

#### 2. API Key Test
```bash
# Test environment variable
python -c "import os; print('API Key:', 'Set' if os.getenv('EXA_API_KEY') else 'Not Set')"
```

#### 3. Server Test
```bash
# Run test script
python test_mcp_search.py

# Or run server directly
python mcp_search_server.py
```

---

## 📚 Usage Guide

This guide walks you through setting up and using the MCP Search Server to discover and research MCP servers for your projects.

### 🛠️ Integration Methods

#### Method 1: Claude Desktop Integration

1. **Locate Claude Desktop config file:**
   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

2. **Add server configuration:**
   ```json
   {
     "mcpServers": {
       "mcp-search": {
         "command": "python",
         "args": ["/absolute/path/to/mcp_search_server.py"],
         "env": {
           "EXA_API_KEY": "your_exa_api_key_here"
         }
       }
     }
   }
   ```

3. **Restart Claude Desktop**

4. **Test in Claude:**
   - Type: "Search for database MCP servers"
   - Claude should now be able to use the MCP search tools

#### Method 2: Cursor Integration

1. **Open Cursor settings**
2. **Navigate to MCP configuration**
3. **Add the MCP search server:**
   ```json
   {
     "command": "python",
     "args": ["/path/to/mcp_search_server.py"],
     "env": {
       "EXA_API_KEY": "your_api_key"
     }
   }
   ```

#### Method 3: Command Line Testing

```bash
# Interactive testing with FastMCP CLI
fastmcp dev mcp_search_server.py

# Web-based inspector
fastmcp inspect mcp_search_server.py
```

#### Method 4: Programmatic Usage

```python
import asyncio
import json
from fastmcp import Client

async def search_for_mcps():
    async with Client("mcp_search_server.py") as client:
        # Search for MCPs
        result = await client.call_tool("search_mcps", {
            "requirement": "database access",
            "max_results": 5
        })
        
        data = json.loads(result.text)
        print(f"Found {data['total_found']} MCPs")
        
        for rec in data['recommendations']:
            print(f"- {rec['name']}: {rec['description']}")

# Run the search
asyncio.run(search_for_mcps())
```

### 🎯 Common Use Cases

#### Use Case 1: Finding MCPs for Specific Tasks

**Goal:** Find MCPs for database operations

**Steps:**
1. Use the `search_mcps` tool
2. Provide requirement: "database access and SQL operations"
3. Review confidence scores and categories
4. Get detailed info with `get_mcp_details`

**Example interaction:**
```
User: "I need an MCP for SQLite database access"
Tool: search_mcps(requirement="SQLite database access", max_results=5)
Result: List of SQLite-related MCPs with confidence scores
```

#### Use Case 2: Exploring MCP Categories

**Goal:** Understand what MCPs are available in different areas

**Steps:**
1. Use `categorize_mcps` tool
2. Provide broad requirement like "file management"
3. Explore different categories returned
4. Drill down into specific categories

**Example interaction:**
```
User: "What file management MCPs are available?"
Tool: categorize_mcps(requirement="file management")
Result: MCPs grouped by categories (File System, Cloud Storage, etc.)
```

#### Use Case 3: Research and Comparison

**Goal:** Compare similar MCPs

**Steps:**
1. Find initial MCP with `search_mcps`
2. Use `find_similar_mcps` to find alternatives
3. Use `get_mcp_details` for detailed comparison
4. Ask specific questions with `ask_mcp_question`

**Example interaction:**
```
User: "Find alternatives to the FastMCP file server"
Tool: find_similar_mcps(reference_mcp_url="https://github.com/example/fastmcp-file")
Result: List of similar MCPs with comparison data
```

#### Use Case 4: General Questions

**Goal:** Get expert answers about MCPs

**Steps:**
1. Use `ask_mcp_question` tool
2. Ask specific questions about MCP ecosystem
3. Get answers with citations
4. Follow up with more specific searches

**Example interaction:**
```
User: "What are the most popular MCPs for web scraping?"
Tool: ask_mcp_question(question="most popular MCPs for web scraping")
Result: Direct answer with citations and source links
```

### 📋 Available Tools Reference

#### 1. `search_mcps`
**Purpose:** Search for MCPs based on requirements

**Parameters:**
- `requirement` (string): What you need (e.g., "database access")
- `max_results` (int, default=10): Number of results
- `include_github_only` (bool, default=false): Limit to GitHub repos

**Returns:** JSON with MCP recommendations, confidence scores, categories

#### 2. `get_mcp_details`
**Purpose:** Get detailed information about a specific MCP

**Parameters:**
- `mcp_url` (string): URL of the MCP repository or documentation

**Returns:** Detailed MCP information including similar MCPs

#### 3. `find_similar_mcps`
**Purpose:** Find MCPs similar to a reference MCP

**Parameters:**
- `reference_mcp_url` (string): URL of reference MCP
- `max_results` (int, default=5): Number of similar MCPs

**Returns:** List of similar MCPs with comparison data

#### 4. `ask_mcp_question`
**Purpose:** Ask specific questions about MCPs

**Parameters:**
- `question` (string): Your question about MCP servers

**Returns:** Direct answer with citations and sources

#### 5. `categorize_mcps`
**Purpose:** Get MCPs organized by categories

**Parameters:**
- `requirement` (string): Requirement to categorize MCPs for

**Returns:** MCPs grouped by functional categories

### 🔍 Understanding Results

#### Confidence Scores
- **0.8-1.0:** Highly relevant, definitely an MCP
- **0.6-0.8:** Likely relevant, probably an MCP
- **0.4-0.6:** Possibly relevant, might be related
- **0.2-0.4:** Low relevance, worth checking
- **0.0-0.2:** Minimal relevance

#### Categories
- **Database & Storage:** SQL, NoSQL, file storage
- **Web & APIs:** HTTP clients, REST APIs, scraping
- **File System:** File operations, directory management
- **Communication:** Slack, Discord, email integration
- **Development Tools:** Git, CI/CD, testing tools
- **AI & ML:** Machine learning, model integration
- **Utilities:** General-purpose tools and helpers

#### Key Features
Automatically extracted capabilities:
- Database operations
- API integration
- File management
- Web scraping
- Communication tools
- Development utilities

---

## 🔧 Configuration

### Environment Variables

- `EXA_API_KEY` (required): Your Exa AI API key

### Server Configuration

The server can be run with different transports:

```python
# STDIO (default) - for local use
mcp.run()

# HTTP Streaming - for web deployment
mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)

# SSE - for compatibility
mcp.run(transport="sse", host="127.0.0.1", port=8000)
```

---

## 📊 API Reference

### Tool Parameters

#### `search_mcps`
- `requirement` (str): Description of what you need
- `max_results` (int, default=10): Number of results to return
- `include_github_only` (bool, default=False): Limit to GitHub repositories

#### `get_mcp_details`
- `mcp_url` (str): URL of the MCP server or repository

#### `find_similar_mcps`
- `reference_mcp_url` (str): URL of reference MCP
- `max_results` (int, default=5): Number of similar MCPs to find

#### `ask_mcp_question`
- `question` (str): Your question about MCP servers

#### `categorize_mcps`
- `requirement` (str): Requirement to categorize MCPs for

### Response Format

All tools return structured JSON with:
- Clear data organization
- Confidence scores where applicable
- Rich metadata (categories, features, etc.)
- Error handling with descriptive messages

---

## 🛠️ Integration

### With Claude Desktop

Add to your `claude_desktop_config.json`:

```json
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
```

### With Cursor

Configure in your MCP settings to enable MCP discovery within Cursor.

### Programmatic Access

```python
from fastmcp import Client

async def main():
    async with Client("mcp_search_server.py") as client:
        result = await client.call_tool("search_mcps", {
            "requirement": "file management",
            "max_results": 5
        })
        print(result.text)
```

---

## 🚨 Troubleshooting

### Common Issues

#### Issue: "python: command not found"
**Solutions:**
- Install Python (see Python Installation section)
- Use `python3` instead of `python`
- Check if Python is in PATH

#### Issue: "No module named 'fastmcp'"
**Solutions:**
```bash
# Install missing dependencies
pip install fastmcp httpx

# Or reinstall from requirements
pip install -r requirements.txt
```

#### Issue: "EXA_API_KEY environment variable is required"
**Solutions:**
- Set the environment variable (see Exa API Key Setup)
- Check if variable is set: `echo $EXA_API_KEY` (Linux/Mac) or `echo %EXA_API_KEY%` (Windows)
- Restart terminal after setting environment variable

#### Issue: Permission errors during installation
**Solutions:**
```bash
# Use --user flag
pip install --user -r requirements.txt

# Or use virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

#### Issue: "SSL Certificate verify failed"
**Solutions:**
```bash
# Upgrade certificates
pip install --upgrade certifi

# Or use --trusted-host (temporary fix)
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org fastmcp
```

#### Issue: "Error searching for MCPs: HTTP 401"
**Solution:** Check that your Exa API key is valid and active

#### Issue: "No MCPs found for requirement"
**Solutions:**
- Try broader search terms
- Use different keywords
- Check if the requirement is too specific

#### Issue: Tool returns empty results
**Solutions:**
- Verify internet connection
- Try different search terms
- Check Exa API status

### Platform-Specific Issues

#### Windows PowerShell Execution Policy
If you get execution policy errors:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### macOS Permission Issues
If you get permission errors:
```bash
# Use Homebrew Python instead of system Python
brew install python@3.11
export PATH="/opt/homebrew/bin:$PATH"
```

#### Linux Missing Development Headers
If compilation fails:
```bash
# Ubuntu/Debian
sudo apt install python3-dev build-essential

# CentOS/RHEL
sudo yum install python3-devel gcc
```

### Performance Tips

1. **Use specific requirements** for better results
2. **Start with broader searches** then narrow down
3. **Check confidence scores** to gauge relevance
4. **Use GitHub-only search** for higher quality results
5. **Try category search** for exploration

### API Limits

- Exa API has rate limits based on your plan
- The server respects these limits automatically
- Consider caching results for frequently searched terms
- Use smaller `max_results` values for faster responses

---

## 🎓 Best Practices

### 1. Search Strategy
- Start broad, then narrow down
- Use domain-specific terminology
- Try multiple phrasings of requirements
- Check confidence scores before diving deep

### 2. Result Evaluation
- Review confidence scores (>0.6 recommended)
- Check repository activity and stars
- Read descriptions carefully
- Verify installation requirements

### 3. Integration Tips
- Test server standalone before integrating
- Use absolute paths in configurations
- Set environment variables properly
- Monitor error logs for issues

### 4. Workflow Optimization
- Save useful MCP URLs for future reference
- Use categorization for discovery
- Ask follow-up questions for clarification
- Compare similar MCPs before choosing

---

## 🔍 How It Works

### Search Intelligence

The system uses multiple signals to identify and rank MCP servers:

1. **Content Analysis**: Scans for MCP-specific keywords and indicators
2. **Source Credibility**: Prioritizes GitHub repositories and official documentation
3. **Exa Scoring**: Leverages Exa's semantic understanding
4. **Feature Extraction**: Automatically identifies key capabilities
5. **Category Classification**: Groups MCPs by functional area

### Quality Scoring

Each MCP recommendation includes a confidence score based on:
- Presence of MCP-specific terminology
- Repository quality indicators
- Documentation completeness
- Exa's semantic relevance score

---

## 🧪 Testing

Run the server in development mode:

```bash
# Interactive testing
fastmcp dev mcp_search_server.py

# Web-based inspector
fastmcp inspect mcp_search_server.py

# Run test script
python test_mcp_search.py
```

---

## 🔒 Security & Privacy

- **API Key Security**: Exa API key required but never logged or exposed
- **Read-Only Operations**: Server only performs search operations, no modifications
- **Error Handling**: Graceful degradation with informative error messages
- **Rate Limiting**: Respects Exa API rate limits

---

## 🚦 Limitations

- Requires Exa API key (paid service)
- Search quality depends on Exa's index coverage
- Results limited by Exa's rate limits
- MCP detection based on content analysis (may have false positives/negatives)

---

## 🎯 Use Cases

### For Developers
- **Discover Tools**: Find MCPs that solve specific development challenges
- **Evaluate Options**: Compare different MCPs for the same use case
- **Learn**: Understand what MCPs are available in the ecosystem

### For AI Assistants
- **Recommendation Engine**: Provide intelligent MCP recommendations to users
- **Research Tool**: Help users find the right tools for their projects
- **Knowledge Base**: Answer questions about the MCP ecosystem

### For Teams
- **Standardization**: Find approved MCPs for team use
- **Documentation**: Maintain knowledge of available tools
- **Discovery**: Stay updated with new MCP releases

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:

1. **Enhanced Analysis**: Better MCP detection algorithms
2. **Caching**: Add result caching for performance
3. **Filtering**: Additional filtering options
4. **Exports**: Export capabilities for found MCPs
5. **Monitoring**: Usage analytics and performance monitoring

---

## 📞 Getting Help

### Built-in Help
Access the help resource: `mcp-search://help`

### Error Messages
The server provides detailed error messages with troubleshooting tips

### Testing
Use the test script to verify functionality:
```bash
python test_mcp_search.py
```

### Support Resources
- FastMCP Documentation: https://gofastmcp.com
- Exa AI Documentation: https://docs.exa.ai
- Model Context Protocol: https://modelcontextprotocol.io

---

## 📄 License

MIT License - see LICENSE file for details.

---

## 🔗 Links

- [FastMCP Documentation](https://gofastmcp.com)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [Exa AI](https://exa.ai)
- [Get Exa API Key](https://dashboard.exa.ai/)

---

## 🆘 Support

- Check the built-in help: Use the `mcp-search://help` resource
- Review error messages for troubleshooting guidance
- Ensure `EXA_API_KEY` is properly set
- Verify network connectivity to Exa API

---

Built with ❤️ using FastMCP and Exa AI

Happy MCP discovering! 🚀
