from pathlib import Path

from mcp.server.fastmcp import FastMCP
from langchain_community.vectorstores import Chroma
import chromadb

from langchain_ollama import OllamaEmbeddings

mcp = FastMCP("RAG Server")

BASE_DIR = Path(__file__).parent.parent

VECTOR_DB = BASE_DIR / "vector_db"

embedding = OllamaEmbeddings(
    model="embeddinggemma"
)

@mcp.tool()
def list_collections() -> list[str]:
    """
    List all available knowledge base collections.

    Use this tool to discover which document collections are currently indexed and
    available for retrieval.
    """


    client = chromadb.PersistentClient(
        path=str(VECTOR_DB)
    )

    return [
        c.name
        for c in client.list_collections()
    ]

@mcp.tool()
def collection_info(collection: str) -> dict:
    """
    Retrieve metadata about a document collection.

    Returns information such as the collection name and the number of indexed
    documents.

    Use this tool when the user requests information about the available knowledge
    bases.
    """


    client = chromadb.PersistentClient(
        path=str(VECTOR_DB)
    )

    col = client.get_collection(collection)

    return {
        "name": collection,
        "documents": col.count(),
    }


@mcp.tool()
def retrieve(
    collection: str,
    query: str,
    k: int = 5,
) -> list[dict]:
    """
    Retrieve the most relevant document chunks from a knowledge base.
    
    Use this tool whenever the user asks questions about the indexed collections.
    
    Returns the most relevant passages together with their metadata.
    
    Examples:
    - What is an MCP Resource?
    - Explain LangChain Runnables.
    """

    vectorstore = Chroma(
        persist_directory=str(VECTOR_DB),
        collection_name=collection,
        embedding_function=embedding,
    )

    docs = vectorstore.similarity_search(
        query,
        k=k,
    )

    return [
        {
            "content": doc.page_content,
            "metadata": doc.metadata,
        }
        for doc in docs
    ]

if __name__ == "__main__":
    mcp.run()