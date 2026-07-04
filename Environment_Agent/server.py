import asyncio
from python_a2a import AgentCard, AgentSkill, run_server, A2AServer
from agent import EnvironmentA2AServer

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

    card = build_card()

    a2a_server = EnvironmentA2AServer(card)

    await a2a_server.env.initialize()

    run_server(
        a2a_server,
        host="0.0.0.0",
        port=8003,
    )

if __name__ == "__main__":
    asyncio.run(main())