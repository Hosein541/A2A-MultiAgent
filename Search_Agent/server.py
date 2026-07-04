import asyncio
from python_a2a import AgentCard, AgentSkill, run_server, A2AServer
from agent import SearchA2AServer

def build_card():
    return AgentCard(
        name="Search Agent",
        description="AI agent specialized in web search using MCP tools.",
        url="http://localhost:8001",     
        version="1.0.0",
        skills=[
            AgentSkill(
                name="web_search",
                description="Search internet and return structured results.",
                tags=["search", "web"],
            )
        ],
        capabilities={"streaming": True},
    )
async def main():

    card = build_card()

    a2a_server = SearchA2AServer(card)

    await a2a_server.search.initialize()

    run_server(
        a2a_server,
        host="0.0.0.0",
        port=8001,
    )

if __name__ == "__main__":
    asyncio.run(main())