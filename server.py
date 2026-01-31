from mcp.server.fastmcp import FastMCP
from google.cloud import storage
import os

mcp = FastMCP("Google Cloud")

@mcp.tool()
def list_my_buckets() -> str:
    """List all Google Cloud Storage buckets in the current project."""
    client = storage.Client()
    buckets = list(client.list_buckets())
    return f"Found {len(buckets)} buckets: " + ", ".join([b.name for b in buckets])

if __name__ == "__main__":
    mcp.run()
