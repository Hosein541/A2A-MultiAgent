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
from agent import env_agent

from python_a2a import AgentCard, AgentSkill

def build_card():
    """Build AgentCard for the Environment Agent (Weather tools)"""
    return AgentCard(
        name="Environment Agent",
        description="Provides current weather, forecasts, and historical weather data for any location worldwide.",
        url="http://localhost:8003",   # Change to your actual port
        version="1.0.0",
        skills=[
            AgentSkill(
                name="get_current_weather",
                description="Get current weather conditions including temperature, humidity, wind speed, precipitation, etc.",
                tags=["weather", "current", "real-time"],
                examples=[
                    "Weather in Tehran right now",
                    "Is it raining in New York?",
                    "Current temperature in Tokyo"
                ]
            ),
            AgentSkill(
                name="get_weather_forecast",
                description="Get weather forecast for the next few days (default 7 days).",
                tags=["weather", "forecast"],
                examples=[
                    "Weather forecast for Paris next week",
                    "Will it rain this weekend in London?",
                    "7-day forecast for Dubai"
                ]
            ),
            AgentSkill(
                name="get_historical_weather",
                description="Retrieve historical weather data between specific start and end dates.",
                tags=["weather", "history"],
                examples=[
                    "Weather in London on January 1st",
                    "Temperature last week in Dubai",
                    "Historical weather data for Tehran"
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

    a2a_server = A2AServer(url="https://localhost:8003")
    a2a_server.agent_card = build_card()

    print("✅ AgentCard attached!")
    print(f"Name : {a2a_server.agent_card.name}")
    print(f"URL  : {a2a_server.agent_card.url}")

    print("\n🚀 Starting A2A Server...")
    run_server(a2a_server, host="0.0.0.0", port=8003)

if __name__ == "__main__":
    asyncio.run(main())