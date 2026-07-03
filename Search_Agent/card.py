from python_a2a import AgentCard, AgentSkill

agent_card = AgentCard(
    name="Search Agent",
    description=(
        "An AI agent specialized in searching the public web. "
        "It retrieves up-to-date information, news, technical documentation, "
        "articles, and other online resources using Tavily."
    ),
    url="http://localhost:8001",
    version="1.0.0",

    capabilities={
        "streaming": True,
        "pushNotifications": False,
        "stateTransitionHistory": False,
        "google_a2a_compatible": True,
        "parts_array_format": True,
    },

    default_input_modes=["text/plain"],

    default_output_modes=["text/plain"],

    skills=[
        AgentSkill(
            id="web_search",
            name="Web Search",
            description=(
                "Search the public internet and return factual, "
                "up-to-date information with relevant sources."
            ),
            tags=[
                "search",
                "web",
                "internet",
                "research",
                "news",
                "documentation",
            ],
            examples=[
                "Search the latest AI news.",
                "Find information about MCP protocol.",
                "Who founded OpenAI?",
            ],
        )
    ],
)