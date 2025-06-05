#!/usr/bin/env python3
"""
Setup script for MCP Search Server
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="mcp-search-server",
    version="1.0.0",
    author="AI Assistant",
    description="An intelligent MCP server for discovering and researching MCP servers using Exa AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["mcp_search_server"],
    python_requires=">=3.10",
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="mcp, model context protocol, search, exa, ai, fastmcp",
    entry_points={
        "console_scripts": [
            "mcp-search-server=mcp_search_server:main",
        ],
    },
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
        ]
    },
    project_urls={
        "Documentation": "https://github.com/your-username/mcp-search-server",
        "Source": "https://github.com/your-username/mcp-search-server",
        "Tracker": "https://github.com/your-username/mcp-search-server/issues",
    },
) 