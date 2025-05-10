# CnosDB MCP Server

[![Python 3.8](https://img.shields.io/badge/python-3.12-blue?logo=python&logoColor=white)](https://docs.python.org/3.12/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![smithery badge](https://smithery.ai/badge/@cnosdb/cnosdb-mcp-server)](https://smithery.ai/server/@cnosdb/cnosdb-mcp-server)

An MCP server for CnosDB.

## Features

 - query

    Execute query (automatically identifies SQL) 

 - list_databases

    List all databases

 - list_tables

    List tables in database

 - describe_table

    Display table schema for [table_name]


## Development

```shell
# Clone the repository
git clone https://github.com/cnosdb/cnosdb-mcp-server.git
cd cnosdb-mcp-server

# Create virtual environment
uv .venv
source .venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install development dependencies
pip install -r requirements.txt
```


### Configuration

> For alternative MCP clients, see: https://github.com/punkpeye/awesome-mcp-clients

1. Open the Claude Desktop configuration file located at:

   - On macOS: ~/Library/Application Support/Claude/claude_desktop_config.json

   - On Windows: %APPDATA%/Claude/claude_desktop_config.json

2. Add the following:

```json
{
  "name": "CnosDB",
  "key": "CnosDBMCPServer",
  "command": "uv",
  "args": [
    "--directory",
    "REPO_PATH/cnosdb-mcp-server",
    "run",
    "server.py"
  ],
  "env": {
    "CNOSDB_HOST": "127.0.0.1",
    "CNOSDB_PORT": "8902",
    "CNOSDB_USERNAME": "root",
    "CNOSDB_PASSWORD": "CnosDB#!"
  }
}
```
Update the environment variables to point to your own CnosDB service.

### Installing via Smithery

To install CnosDB Server for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@cnosdb/cnosdb-mcp-server):

```bash
npx -y @smithery/cli install @cnosdb/cnosdb-mcp-server --client claude
```
