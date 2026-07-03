import asyncio

from python_a2a import (
    AgentCard,
    AgentSkill,
    run_server,
)

# from python_a2a.langchain import to_a2a_server

# from agent import search_agent


# def build_card():

#     return AgentCard(
#         name="Search Agent",
#         description="AI agent specialized in web search using MCP tools.",
#         url="http://localhost:8001",
#         version="1.0.0",
#         skills=[
#             AgentSkill(
#                 name="web_search",
#                 description="Search internet and return structured results.",
#                 tags=["search", "web", "tavily"],
#             )
#         ],
#         capabilities={
#             "streaming": True,
#         },
#     )


# async def main():

#     await search_agent.initialize()

#     card = build_card()

#     a2a_server = to_a2a_server(
#         search_agent.agent,
#         agent_card=card   # 🔥 مهم‌ترین fix
#     )

#     run_server(
#         a2a_server,
#         host="0.0.0.0",
#         port=8001,
#     )

import asyncio
from python_a2a import AgentCard, AgentSkill, run_server, A2AServer
from agent import knowledge_agent

from python_a2a import AgentCard, AgentSkill

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
    # await search_agent.initialize()   # فعلاً کامنت

    a2a_server = A2AServer(url="https://localhost:8004")
    a2a_server.agent_card = build_card()

    print("✅ AgentCard attached!")
    print(f"Name : {a2a_server.agent_card.name}")
    print(f"URL  : {a2a_server.agent_card.url}")

    print("\n🚀 Starting A2A Server...")
    run_server(a2a_server, host="0.0.0.0", port=8004)

if __name__ == "__main__":
    asyncio.run(main())