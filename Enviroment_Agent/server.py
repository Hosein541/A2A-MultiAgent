import asyncio

from python_a2a import (
    AgentCard,
    AgentSkill,
    run_server,
)

from python_a2a.langchain import to_a2a_server

from agent import env_agent


async def create_server():

    # Initialize LangGraph Agent
    await env_agent.initialize()

    # Convert LangGraph/LangChain agent to A2A Server
    a2a_server = to_a2a_server(env_agent.agent)

    # Agent Card
    a2a_server.agent_card = AgentCard(
        name="Environment Agent",
        description=("Weather and environmental information."),
        url="http://localhost:8004",
        port=8004,
        skills=[
            AgentSkill(
                name="Weather",
                description="Weather forecasting and current conditions.",
                tags=[
                    "weather",
                    "forecast",
                ],
                examples=[
                    "Weather in Tokyo",
                    "Will it rain tomorrow?",
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