import asyncio
import os
from utils.cli import *
from rich.console import Console
console = Console()


from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI

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

# -----------------------
# MCP Client
# -----------------------

client = MultiServerMCPClient(
    {
        "rag": {
            "transport": "stdio",
            "command": "python",
            "args": ["servers/rag_server.py"],
        },
    }
)


async def main():

    loading()

    tools = await client.get_tools()

    loaded(len(tools))

    llm = ChatGoogleGenerativeAI(
            model="gemini-3.1-flash-lite",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.2,
        )

    memory = MemorySaver()

    agent = create_react_agent(
        model=llm,
        tools=tools,
        checkpointer=memory,
    )

    config = {
        "configurable": {
            "thread_id": "demo-session"
        }
    }
    title()
    ready()

    while True:
        user()

        question = input()

        if question.lower() in {"exit", "quit"}:
            break

        print()
        assistant()

        async for event in agent.astream_events(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": question,
                    }
                ]
            },
            config=config,
            version="v2",
        ):

            event_type = event["event"]

            # --------------------
            # Tool Start
            # --------------------

            if event_type == "on_tool_start":

                tool = event["name"]

                tool_cli(event["name"])

            # --------------------
            # Tool End
            # --------------------

            elif event_type == "on_tool_end":

                tool_done()

            # --------------------
            # Stream Tokens
            # --------------------

            elif event_type == "on_chat_model_stream":

                chunk = event["data"]["chunk"]

                if hasattr(chunk, "content") and chunk.content:

                    piece = extract_text(chunk.content)
                    console.out(
                        piece,
                        end=""
                    )

        print("\n")


if __name__ == "__main__":
    asyncio.run(main())