from mcp.server.fastmcp import FastMCP
from google.cloud import storage
import os

mcp = FastMCP("Antigravity-Engine")

@mcp.tool()
def list_my_buckets() -> str:
    """List all Google Cloud Storage buckets in the current project."""
    client = storage.Client()
    buckets = list(client.list_buckets())
    return f"Found {len(buckets)} buckets: " + ", ".join([b.name for b in buckets])

@mcp.tool()
async def list_project_files():
    """Lists the files in the local antigravity-mcp-setup directory."""
    # Added the leading / and closed the quotes/parenthesis
    files = os.listdir("/home/john/antigravity-mcp-setup")
    return {"local_files": files}


if __name__ == "__main__":
    mcp.run()
