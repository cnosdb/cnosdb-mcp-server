import pandas as pd
from typing import List

from mcp.types import TextContent


def format_result(df: pd.DataFrame, max_rows: int = 200) -> List[TextContent]:

    """Enhanced Result Formatting"""
    if df.empty:
        return [TextContent(text="No records found")]

    # Auto-detect time columns
    time_cols = [col for col in df.columns if 'time' in col.lower()]
    if time_cols:
        # Non-time columns
        other_cols = [col for col in df.columns if col not in time_cols]

        # New column order: time columns first, followed by others
        new_columns = time_cols + other_cols
        df = df[new_columns]

        # Sort by the first time column in descending order
        df = df.sort_values(time_cols[0], ascending=False)

    # Smart Truncation
    if len(df) > max_rows:
        sample = df.head(max_rows)
        info = f"Showing first {max_rows} rows（of {len(df)} total）\n"
    #     return [TextContent(text=df.to_html(index=False))]
    # return [TextContent(text=df.to_html(index=False))]

        return [TextContent(type="text",text=info + sample.to_markdown(index=False))]
    return [TextContent(type="text",text=df.to_markdown(index=False))]


def validate_sql(sql: str) -> bool:
    """SQL Security Validation"""
    forbidden = ["drop ", "delete ", "insert ", "alter ", "create ", "grant "]
    sql_lower = sql.lower()
    return not any(cmd in sql_lower for cmd in forbidden)

