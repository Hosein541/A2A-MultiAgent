from python_a2a import AgentCard, AgentSkill

agent_card = AgentCard(
    name="Knowledge Agent",
    description=(
        "An AI agent specialized in Retrieval-Augmented Generation (RAG). "
        "It answers questions using internal documents and vector search."
    ),
    url="http://localhost:8002",
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
            id="knowledge_retrieval",
            name="Knowledge Retrieval",
            description="Answer questions using an internal RAG knowledge base.",
            tags=[
                "rag",
                "vector-search",
                "knowledge-base",
                "documents",
            ],
            examples=[
                "Summarize the uploaded PDF.",
                "Search our internal documentation.",
                "Answer using the company knowledge base.",
            ],
        )
    ],
)