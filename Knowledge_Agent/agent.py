import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()


def extract_text(content):

    if isinstance(content, str):
        return content

    if isinstance(content, list):

        text = ""

        for item in content:

            if isinstance(item, dict):

                text += item.get("text", "")

        return text

    return ""


class KnowledgeAgent:

    def __init__(self):

        self.client = MultiServerMCPClient(
            {
            "rag": {
                "transport": "stdio",
                "command": "python",
                "args": ["servers/rag_server.py"],
            },
            }
        )

        self.memory = MemorySaver()

        self.config = {
            "configurable": {
                "thread_id": "search-agent"
            }
        }

        self.agent = None

    async def initialize(self):

        tools = await self.client.get_tools()

        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.2,
        )

        self.agent = create_react_agent(
            model=llm,
            tools=tools,
            checkpointer=self.memory,
        )

    async def invoke(self, query: str):

        final_answer = ""

        tool_calls = []

        async for event in self.agent.astream_events(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": query,
                    }
                ]
            },
            config=self.config,
            version="v2",
        ):

            event_type = event["event"]

            # Tool Started
            if event_type == "on_tool_start":

                tool_calls.append(
                    {
                        "tool": event["name"],
                        "status": "started",
                    }
                )

            # Tool Finished
            elif event_type == "on_tool_end":

                tool_calls.append(
                    {
                        "tool": event["name"],
                        "status": "finished",
                    }
                )

            # LLM Streaming
            elif event_type == "on_chat_model_stream":

                chunk = event["data"]["chunk"]

                if hasattr(chunk, "content") and chunk.content:

                    final_answer += extract_text(chunk.content)

        return {
            "answer": final_answer,
            "tool_calls": tool_calls,
        }
    
knowledge_agent=KnowledgeAgent()