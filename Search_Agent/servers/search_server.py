import os
from dotenv import load_dotenv
from pathlib import Path
# ROOT_DIR = Path(__file__).resolve().parent.parent
# load_dotenv(ROOT_DIR / ".env")
load_dotenv()


from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient

mcp = FastMCP("Search Server")

client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


@mcp.tool()
def search_web(query: str, max_results: int = 5) -> dict:
    """
    Search the web using Tavily.

    Args:
        query: Search query.
        max_results: Number of search results to return.

    Returns:
        search results.
    """
    response = client.search(
        query=query,
        max_results=max_results,
        
    )

    return {
        "query": query,
        "answer": response.get("answer"),
        "results": [
            {
                "title": result["title"],
                "url": result["url"],
                "content": result["content"],
                "score": result.get("score"),
            }
            for result in response.get("results", [])
        ],
    }


if __name__ == "__main__":
    mcp.run()