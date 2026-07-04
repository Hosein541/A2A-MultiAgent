import os
import asyncio
from dotenv import load_dotenv

from pydantic import BaseModel
from typing import List, Literal

from langchain_google_genai import ChatGoogleGenerativeAI
from python_a2a import A2AClient

load_dotenv()
import asyncio
import subprocess
import time
from utils.cli import *


async def run_agent(folder: str, port: int):
    print(f"🚀 Starting {folder} on port {port}")
    subprocess.Popen(
        ["poetry", "run", "python", f"{folder}/server.py"],
        cwd=".",
        shell=True
    )
    await asyncio.sleep(2)  # give it time to start

async def main():
    await run_agent("Search_Agent", 8001)
    await run_agent("Analysis_Agent", 8002)
    await run_agent("Environment_Agent", 8003)
    await run_agent("Knowledge_Agent", 8004)
    
    print("\n✅ All agents started in background!")
    print("Now you can run Coordinator.")

asyncio.run(main())

# ---------------------------
# Structured Planner Output
# ---------------------------

class Step(BaseModel):
    agent: Literal["Search Agent", "Knowledge Agent", "Analysis Agent", "Environment Agent"]
    task: str


class Plan(BaseModel):
    steps: List[Step]

class Coordinator:
    def __init__(self):
        self.clients = {
            "Search Agent": A2AClient("http://localhost:8001"),
            "Analysis Agent": A2AClient("http://localhost:8002"),
            "Environment Agent": A2AClient("http://localhost:8003"),
            "Knowlege Agent": A2AClient("http://localhost:8004"),
        }
        


        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.1-flash-lite",
            temperature=0,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        self.registry = {}

    # ===================== DISCOVERY =====================
    async def load_registry(self):
        """Load Agent Cards from all agents using real A2A discovery"""
        for name, client in self.clients.items():
            try:
                card = client.get_agent_card()   
                # print(f"✅ Loaded card for {name}: {card.name}")
                agent_loaded(card)
                self.registry[name] = {"client": client, "card": card}
            except Exception as e:
                print(f"❌ Failed to load card for {name}: {e}")

    # ===================== PLANNING =====================
    async def plan(self, query: str):
        """Create plan using real agent capabilities from Agent Cards"""
        context = ""
        for name, data in self.registry.items():
            card = data["card"]
            skills = ", ".join([s.name for s in card.skills]) if card.skills else "No skills defined"

            
            context += f"""
Agent: {card.name}
Description: {card.description}
Skills: {skills}
---
"""

        prompt = f"""
You are an intelligent multi-agent planner.
Break down the user request into the minimum number of steps needed.

Available Agents:
{context}

Rules:
- Assign the most suitable agent for each step
- Make tasks clear and executable
- You can use one or multiple steps

User Query: {query}

Return ONLY valid JSON in this format:
{{
  "steps": [
    {{
      "agent": "search",
      "task": "detailed task description"
    }}
  ]
}}
"""

        response = self.llm.invoke(prompt)
        content = response.content[0]["text"] if isinstance(response.content, list) else response.content

        # print(f"output of the planner:{content}")
        planner_output(content)
        return Plan.model_validate_json(content)

    # ===================== EXECUTION =====================
    async def execute(self, plan: Plan):
        results = []
        for step in plan.steps:
            if step.agent not in self.registry:
                results.append({"agent": step.agent, "task": step.task, "result": "Agent not found"})
                continue
                
            client = self.registry[step.agent]["client"]
            try:
                running_step(step.agent, step.task)
                result = client.ask(step.task)
                results.append({
                    "agent": step.agent,
                    "task": step.task,
                    "result": result
                })

                agent_result(step.agent, result)
            except Exception as e:
                results.append({
                    "agent": step.agent,
                    "task": step.task,
                    "result": f"Error: {str(e)}"
                })
        return results

    # -----------------------
    # FINAL ANSWER
    # -----------------------

    async def finalize(self, query: str, results):

        prompt = f"""
You are a final answer synthesizer.

User question:
{query}

Agent results:
{results}

Return a clean, human-readable final answer.
"""

        response = self.llm.invoke(prompt)

        return response.content[0]["text"]
    
    # -----------------------
    # MAIN ENTRY
    # -----------------------
    async def chat(self, query: str):

        if not self.registry:
            await self.load_registry()



        plan = await self.plan(query)

        results = await self.execute(plan)

        # print(f"result of the agents:\t\t\t{results}")

        final = await self.finalize(query, results)


        return final