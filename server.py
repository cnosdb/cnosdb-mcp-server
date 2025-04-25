from fastmcp import FastMCP
from mcp.types import TextContent

from http_client import CnosDBClient
from config import CnosDBConfig
from utils import format_result
from typing import List, Optional
import pandas as pd

mcp = FastMCP("cnosdb_mcp_server")
config = CnosDBConfig()

# Initialize HTTP Client
client = CnosDBClient(
    base_url=f"http://{config.host}:{config.port}",
    username=config.username,
    password=config.password
)


@mcp.tool()
def query(sql: str, db: Optional[str] = None) -> List[TextContent]:
    """
    Execute query (automatically identifies SQL)
    Parameters:
    - sql: Query statement
    - db: Specify database (optional)
    """
    if not db:
        db = config.database

    try:
        result = client.execute_sql(sql, db)
        df = pd.DataFrame(result)
        return format_result(df)
    except Exception as e:
        raise ValueError(f"Query '{sql[:50]}...' failed: {str(e)}")


@mcp.tool()
def list_databases() -> List[TextContent]:
    """List all databases"""
    try:
        result = client.execute_sql("SHOW DATABASES")
        return [TextContent(type="text",text=item['database_name']) for item in result]
    except Exception as e:
        raise ValueError(f"Failed to retrieve the database list: {str(e)}")

@mcp.tool()
def list_tables(db: str) -> List[TextContent]:
    """List tables in database"""
    try:
        result = client.execute_sql("SHOW TABLES", db)
        return [TextContent(type="text",text=item['table_name']) for item in result]
    except Exception as e:
        raise ValueError(f"Failed to list tables in the specified database: {str(e)}")

@mcp.tool()
def describe_table(table_name: str, db: str) -> list[TextContent]:
    """Display table schema for [table_name]"""
    try:
        result = client.execute_sql(f"describe table '{table_name}'",db)
        df = pd.DataFrame(result)
        return format_result(df)
    except Exception as e:
        raise ValueError(f"Failed to retrieve columns from the specified table: {str(e)}")


if __name__ == "__main__":
    print("Starting CnosDB HTTP MCP Server...")
    mcp.run(transport="stdio")