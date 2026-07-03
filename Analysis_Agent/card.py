from python_a2a import AgentCard, AgentSkill

agent_card = AgentCard(
    name="Analysis Agent",
    description=(
        "An AI agent specialized in mathematics, numerical reasoning, "
        "financial calculations, and market analysis."
    ),
    url="http://localhost:8003",
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
            id="analysis",
            name="Analysis",
            description="Perform mathematical and market analysis.",
            tags=[
                "math",
                "finance",
                "market",
                "analysis",
            ],
            examples=[
                "Calculate compound interest.",
                "Analyze Apple stock.",
                "Solve this equation.",
            ],
        )
    ],
)