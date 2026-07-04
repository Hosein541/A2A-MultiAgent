from agent import AnalysisA2AServer
import asyncio
from python_a2a.langchain import to_a2a_server
from python_a2a import AgentCard, AgentSkill, run_server, A2AServer


def build_card():
    """Build AgentCard for the Analysis Agent (Market + Calculator tools)"""
    return AgentCard(
        name="Analysis Agent",
        description="Specialized financial analysis agent. Provides real-time market data, historical prices, symbol search, and advanced mathematical calculations.",
        url="http://localhost:8002",   # Change to your actual port
        version="1.0.0",
        skills=[
            AgentSkill(
                name="get_market_data",
                description="Retrieve current price, volume, market cap and key statistics for stocks, ETFs, crypto, or commodities.",
                tags=["finance", "market", "real-time"],
                examples=[
                    "What is the current price of Apple?",
                    "How much is Bitcoin worth right now?",
                    "Show me Tesla stock details"
                ]
            ),
            AgentSkill(
                name="get_historical_data",
                description="Get historical price data for any financial asset with custom period and interval.",
                tags=["finance", "history", "chart"],
                examples=[
                    "Show Tesla stock performance last month",
                    "Bitcoin price history for the past week"
                ]
            ),
            AgentSkill(
                name="search_symbol",
                description="Search for ticker symbols by company name or asset name when the exact symbol is unknown.",
                tags=["finance", "search"],
                examples=[
                    "What is Apple's ticker?",
                    "Find symbol for Gold"
                ]
            ),
            AgentSkill(
                name="add",
                description="Add two numbers.",
                tags=["math", "basic"]
            ),
            AgentSkill(
                name="subtract",
                description="Subtract second number from first.",
                tags=["math"]
            ),
            AgentSkill(
                name="multiply",
                description="Multiply two numbers.",
                tags=["math"]
            ),
            AgentSkill(
                name="divide",
                description="Divide first number by second.",
                tags=["math"]
            ),
            AgentSkill(
                name="power",
                description="Calculate exponentiation (x^y).",
                tags=["math", "advanced"]
            ),
            AgentSkill(
                name="sqrt",
                description="Calculate square root of a number.",
                tags=["math"]
            ),
            AgentSkill(
                name="factorial",
                description="Compute factorial of a non-negative integer.",
                tags=["math"]
            )
        ],
        capabilities={
            "streaming": False,
            "mcp_enabled": True
        }
    )

async def main():

    card = build_card()

    a2a_server = AnalysisA2AServer(card)

    await a2a_server.analysis.initialize()

    run_server(
        a2a_server,
        host="0.0.0.0",
        port=8002,
    )

if __name__ == "__main__":
    asyncio.run(main())
