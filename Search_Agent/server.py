import asyncio

from python_a2a import (
    AgentCard,
    AgentSkill,
    run_server,
)

from agent import search_agent

import asyncio
from python_a2a import AgentCard, AgentSkill, run_server, A2AServer
from agent import search_agent

def build_card():
    return AgentCard(
        name="Search Agent",
        description="AI agent specialized in web search using MCP tools.",
        url="http://localhost:8001",      # ← این خیلی مهمه
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
    # await search_agent.initialize()   # فعلاً کامنت

    a2a_server = A2AServer(url="https://localhost:8001")
    a2a_server.agent_card = build_card()

    print("✅ AgentCard attached!")
    print(f"Name : {a2a_server.agent_card.name}")
    print(f"URL  : {a2a_server.agent_card.url}")

    print("\n🚀 Starting A2A Server...")
    run_server(a2a_server, host="0.0.0.0", port=8001)

if __name__ == "__main__":
    asyncio.run(main())