# import os
# import asyncio
# from dotenv import load_dotenv

from pydantic import BaseModel
from typing import List, Literal

# from langchain_google_genai import ChatGoogleGenerativeAI
# from python_a2a import A2AClient

# load_dotenv()


# ---------------------------
# Structured Planner Output
# ---------------------------

class Step(BaseModel):
    agent: Literal["search", "knowledge", "analysis", "environment"]
    task: str


class Plan(BaseModel):
    steps: List[Step]

# # ---------------------------
# # Coordinator Agent
# # ---------------------------

# class Coordinator:

#     def __init__(self):

#         # A2A Clients
#         self.search = A2AClient("http://localhost:8001")
#         self.knowledge = A2AClient("http://localhost:8002")
#         self.analysis = A2AClient("http://localhost:8003")
#         self.environment = A2AClient("http://localhost:8004")

#         # LLM Planner
#         self.llm = ChatGoogleGenerativeAI(
#             model="gemini-3.1-flash-lite",
#             google_api_key=os.getenv("GOOGLE_API_KEY"),
#             temperature=0
#         )

#     # -----------------------
#     # PLANNING
#     # -----------------------

#     async def plan(self, query: str) -> Plan:

#         prompt = f"""
# You are a planning agent.

# Decompose the user request into steps.

# Available agents:
# - search
# - knowledge
# - analysis
# - environment

# Rules:
# - Output ONLY valid JSON
# - Each step must be minimal and executable
# - If single step, return one item list

# User request:
# {query}

# Return format:
# {{
#   "steps": [
#     {{
#       "agent": "search",
#       "task": "..."
#     }}
#   ]
# }}
# """

#         response = self.llm.invoke(prompt)
#         rs = response.content[0]["text"]
#         print(f"response\t\t:{rs}")

#         return Plan.model_validate_json(response.content[0]["text"])

#     # -----------------------
#     # EXECUTION
#     # -----------------------

#     async def execute(self, plan: Plan):

#         results = []

#         for step in plan.steps:

#             if step.agent == "search":
#                 result = self.search.ask(step.task)

#             elif step.agent == "knowledge":
#                 result = self.knowledge.ask(step.task)

#             elif step.agent == "analysis":
#                 result = self.analysis.ask(step.task)

#             elif step.agent == "environment":
#                 result = self.environment.ask(step.task)

#             else:
#                 result = {"error": "unknown agent"}

#             results.append({
#                 "agent": step.agent,
#                 "task": step.task,
#                 "result": result
#             })

#         return results

#     # -----------------------
#     # FINAL ANSWER
#     # -----------------------

#     async def finalize(self, query: str, results):

#         prompt = f"""
# You are a final answer synthesizer.

# User question:
# {query}

# Agent results:
# {results}

# Return a clean, human-readable final answer.
# """

#         response = self.llm.invoke(prompt)

#         return response.content[0]["text"]

#     # -----------------------
#     # MAIN ENTRY
#     # -----------------------

#     async def chat(self, query: str):

#         plan = await self.plan(query)

#         results = await self.execute(plan)

#         final = await self.finalize(query, results)

#         return final


import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from python_a2a import A2AClient

load_dotenv()


class Coordinator:

    def __init__(self):

        self.clients = {
            "search": A2AClient("http://localhost:8001"),
            "knowledge": A2AClient("http://localhost:8002"),
            "analysis": A2AClient("http://localhost:8003"),
            "environment": A2AClient("http://localhost:8004"),
        }
        self.search = A2AClient("http://localhost:8001")
        print(self.search.get_agent_card())

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.1-flash-lite",
            temperature=0,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

        self.registry = {}

    # -------------------------
    # DISCOVERY PHASE (REAL A2A)
    # -------------------------

    # async def load_registry(self):

    #     for name, client in self.clients.items():

    #         card = client.get_agent_card()

    #         self.registry[name] = {
    #             "client": client,
    #             "card": card
    #         }

    async def load_registry(self):
        for name, client in self.clients.items():
            try:
                card = await client.get_agent_card()   # بهتره async باشه اگر ساپورت کنه
                print(f"✅ Loaded card for {name}: {card.name} - {card.description}")
                self.registry[name] = {"client": client, "card": card}
            except Exception as e:
                print(f"❌ Failed to load card for {name}: {e}")
    # -------------------------
    # ROUTER
    # -------------------------
    async def plan(self, query: str):

        context = ""

        for name, data in self.registry.items():

            card = data["card"]

            skills = ", ".join([s.name for s in card.skills]) if card.skills else ""
            print(f"card name\t\t{card}")
            print(f"agent skill\t\t{skills}")

            context += f"""
    Agent: {card.name}
    Skills: {skills}
    Description: {card.description}
    ---
    """

        prompt = f"""
    You are a multi-agent planner.

    Break the user request into steps.

    You MUST:
    - assign correct agent
    - assign task for each step
    - you can use multiple steps

    Available agents:
    {context}

    User query:
    {query}

    Return format:
    {{
      "steps": [
        {{
          "agent": "search",
          "task": "..."
        }}
      ]
    }}
    """

        response = self.llm.invoke(prompt)

        return Plan.model_validate_json(response.content[0]["text"])
    
    async def execute(self, plan: Plan):
    
        results = []
    
        for step in plan.steps:
        
            client = self.registry[step.agent]["client"]
    
            result = client.ask(step.task)
    
            results.append({
                "agent": step.agent,
                "task": step.task,
                "result": result
            })
    
        return results


    # -----------------------
    # FINAL ANSWER
    # -----------------------

    # -----------------------
    # MAIN ENTRY
    # -----------------------
    async def chat(self, query: str):

        if not self.registry:
            await self.load_registry()

        plan = await self.plan(query)

        results = await self.execute(plan)

        return results