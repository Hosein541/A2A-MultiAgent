from python_a2a import AgentCard, AgentSkill

agent_card = AgentCard(
    name="Environment Agent",
    description=(
        "An AI agent specialized in weather forecasting and environmental data."
    ),
    url="http://localhost:8004",
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
            id="weather",
            name="Weather",
            description="Provide weather forecasts and current conditions.",
            tags=[
                "weather",
                "forecast",
                "temperature",
            ],
            examples=[
                "Weather in Tehran.",
                "Will it rain tomorrow?",
                "Current temperature in London.",
            ],
        )
    ],
)