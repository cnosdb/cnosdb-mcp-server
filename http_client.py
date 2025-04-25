import httpx
from typing import Optional, Dict, Any
import logging

from config import config
import utils


class CnosDBClient:
    """A synchronous client for interacting with CnosDB's HTTP API.

    Args:
        base_url: The base URL of the CnosDB server (default: "http://localhost:8902")
        username: Username for authentication (default: "root")
        password: Password for authentication (default: "")
        timeout: Request timeout in seconds (default: 30)
    """

    def __init__(
            self,
            base_url: str = f"http://{config.host}:{config.port}",
            username: str = f"{config.username}",
            password: str = f"{config.password}",
            timeout: int = 30
    ) -> None:
        """Initialize the CnosDB client."""
        self.base_url = base_url.rstrip("/")
        self.auth = (username, password)
        self.timeout = timeout
        self.client = httpx.Client(
            auth=self.auth,
            timeout=timeout,
            headers={"Accept": "application/json"}
        )
        self.logger = logging.getLogger("cnosdb.http")

    def execute_sql(self, sql: str, db: Optional[str] = None) -> Dict[str, Any]:

        if not utils.validate_sql(sql):
            return {}
        """Execute SQL query.

        Args:
            sql: The SQL query string to execute
            db: Optional database name to use for the query

        Returns:
            Dictionary containing the query results

        Raises:
            ValueError: If the query fails
            httpx.HTTPError: For network-related errors
        """
        url = f"{self.base_url}/api/v1/sql"
        if db:
            url += f"?db={db}"

        try:
            resp = self.client.post(
                url,
                content=sql,
                headers={"Content-Type": "text/plain"}
            )
            resp.raise_for_status()

            if resp.text == "":
                self.logger.warning("Empty response from CnosDB")
                return {}
            return resp.json()
        except httpx.HTTPStatusError as e:
            error_msg = e.response.text[:200]
            self.logger.error(f"Query failed: {error_msg}")
            raise ValueError(f"Query failed: {error_msg}")
        except httpx.RequestError as e:
            self.logger.error(f"Network error during query: {str(e)}")
            raise

    def close(self) -> None:
        """Close the HTTP client connection."""
        self.client.close()

    def __enter__(self):
        """Enable usage in context managers."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensure connection is closed when exiting context."""
        self.close()