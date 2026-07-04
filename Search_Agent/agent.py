import os
from dotenv import load_dotenv
load_dotenv()
import asyncio
from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from python_a2a import A2AServer
from python_a2a import TaskStatus, TaskState
import uuid 

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


class SearchAgent:

    def __init__(self):

        self.client = MultiServerMCPClient(
        {
            "math": {
                "transport": "stdio",
                "command": "python",
                "args": ["-m", "servers.search_server"],   
                "cwd": str(Path(__file__).parent),       
            }
        }
    )
        self.memory = MemorySaver()

        self.config = {
            "configurable": {
                # "thread_id": "search-agent"
                "thread_id": str(uuid.uuid4())
            }
        }

        self.agent = None
        self.llm = None
        self.tools = None


    async def initialize(self):
        print("🔄 Getting tools from MCP servers...")
        try:
            tools = await self.client.get_tools()
            self.tools = tools 
            print(f"✅ Successfully loaded {len(tools)} tools")
            # print tools names for debug
            for t in tools:
                print(f"   - {t.name}")

            llm = ChatGoogleGenerativeAI(
                model="gemini-3.1-flash-lite",
                google_api_key=os.getenv("GOOGLE_API_KEY"),
                temperature=0.2,
            )

            self.agent = create_react_agent(
                model=llm,
                tools=tools,
                checkpointer=self.memory,
            )
        except Exception as e:
            print(f"❌ MCP Error: {e}")
            raise

    
    async def ainvoke(self, query: str):
        if not self.agent:
            await self.initialize()

        try:
            result = await self.agent.ainvoke({
                "messages": [{"role": "user", "content": query}]
            }, config=self.config)
            
            # extract the response
            if isinstance(result, dict) and "messages" in result:
                last = result["messages"][-1]
                return last.content if hasattr(last, "content") else str(last)
            return str(result)
        except Exception as e:
            return f"Error: {str(e)}"
        



class SearchA2AServer(A2AServer):


    def __init__(self, agent_card):
        super().__init__(agent_card=agent_card)
        self.search = SearchAgent()

    def handle_task(self, task):

        text = task.message["content"]["text"]

        result = asyncio.run(
            self.search.ainvoke(text)
        )

        task.artifacts = [{
            "parts":[
                {
                    "type":"text",
                    "text":result
                }
            ]
        }]

        task.status = TaskStatus(
            state=TaskState.COMPLETED
        )

        return task
    

