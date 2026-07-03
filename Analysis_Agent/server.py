import asyncio

from python_a2a import (
    AgentCard,
    AgentSkill,
    run_server,
)

from python_a2a.langchain import to_a2a_server

from agent import analysis_agent


async def create_server():

    # Initialize LangGraph Agent
    await analysis_agent.initialize()

    # Convert LangGraph/LangChain agent to A2A Server
    a2a_server = to_a2a_server(analysis_agent.agent)

    # Agent Card
    a2a_server.agent_card = AgentCard(
        name="Analysis Agent",
        description="Math and Market Analysis.",
        url="http://localhost:8003",
        port=8003,
        skills=[
            AgentSkill(
                name="Analysis",
                description="Mathematical reasoning and market analysis.",
                tags=[
                    "math",
                    "market",
                    "analysis",
                ],
                examples=[
                    "Calculate CAGR.",
                    "Analyze stock trends.",
                ],
            )
        ],
        capabilities={
            "streaming": True,
        },
    )

    return a2a_server


async def main():

    server = await create_server()

    run_server(
        server,
        host="0.0.0.0",
        port=8001,
    )


if __name__ == "__main__":
    asyncio.run(main())