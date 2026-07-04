import asyncio
from python_a2a import AgentCard, AgentSkill, run_server, A2AServer
from agent import KnowledgeA2AServer



def build_card():
    """Build AgentCard for the Knowledge Agent (RAG / Vector Database)"""
    return AgentCard(
        name="Knowledge Agent",
        description="Intelligent knowledge base agent using RAG. Can search and retrieve information from indexed document collections.",
        url="http://localhost:8004",   # Change to your actual port
        version="1.0.0",
        skills=[
            AgentSkill(
                name="list_collections",
                description="List all available knowledge base collections that are currently indexed.",
                tags=["knowledge", "rag", "list"],
                examples=[
                    "What knowledge bases do you have?",
                    "Show me all collections"
                ]
            ),
            AgentSkill(
                name="collection_info",
                description="Get metadata about a specific collection including document count.",
                tags=["knowledge", "info"],
                examples=[
                    "How many documents are in the MCP collection?",
                    "Tell me about the LangChain collection"
                ]
            ),
            AgentSkill(
                name="retrieve",
                description="Retrieve the most relevant document chunks from a knowledge base using semantic search.",
                tags=["knowledge", "rag", "search", "retrieval"],
                examples=[
                    "What is an MCP Resource?",
                    "Explain LangChain Runnables",
                    "Tell me about Agent Cards in A2A"
                ]
            )
        ],
        capabilities={
            "streaming": False,
            "mcp_enabled": True
        }
    )

async def main():

    card = build_card()

    a2a_server = KnowledgeA2AServer(card)

    await a2a_server.rag.initialize()

    run_server(
        a2a_server,
        host="0.0.0.0",
        port=8004,
    )

if __name__ == "__main__":
    asyncio.run(main())