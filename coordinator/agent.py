import os
import asyncio
import subprocess
from dotenv import load_dotenv
load_dotenv()
from pydantic import BaseModel
from typing import List, Literal
from python_a2a import A2AClient
from langchain_google_genai import ChatGoogleGenerativeAI
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
    await run_agent("Analysis_Agent", 8005)
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
    depends_on: list[int] | None = None


class Plan(BaseModel):
    steps: List[Step]

class Coordinator:
    def __init__(self):
        self.clients = {
            "Search Agent": A2AClient("http://localhost:8001"),
            "Analysis Agent": A2AClient("http://localhost:8005"),
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
You are the Coordinator Planner of a multi-agent AI system.

Your responsibility is to decide WHICH agent(s) should handle the user's request.

IMPORTANT:
Each available agent is already an autonomous ReAct agent.
Each agent can reason, decide which of its own tools to use, call multiple tools if necessary, and produce a final answer.

Therefore:

- NEVER plan at the tool level.
- NEVER mention tool names, APIs, functions, MCP servers, or implementation details.
- NEVER decompose a task into multiple steps if a single agent can complete it independently.
- Create the minimum number of steps possible.
- Each task should describe the desired outcome, NOT the procedure.

Available Agents:
{context}

Planning Rules:

1. Select the most appropriate agent for each responsibility.
2. Use a single step whenever one agent is sufficient.
3. Use multiple steps ONLY when multiple agents have distinct responsibilities.
4. Tasks should be high-level objectives.
5. Do not describe how the agent should solve the task.
6. Keep tasks concise and unambiguous.

User Query:
{query}

Return ONLY valid JSON.

Output Schema:

{{
    "steps": [
        {{
            "agent": "<Exact Agent Name>",
            "task": "<High-level objective>"
        }}
    ]
}}

The "agent" field MUST exactly match one of the available agent names.

Good Examples:

User:
"What is today's Tesla stock price?"

Output:
{{
    "steps": [
        {{
            "agent": "Analysis Agent",
            "task": "Provide today's Tesla stock price."
        }}
    ]
}}

--------------------------------

User:
"What's the weather in Paris tomorrow?"

Output:
{{
    "steps": [
        {{
            "agent": "Environment Agent",
            "task": "Provide tomorrow's weather forecast for Paris."
        }}
    ]
}}

--------------------------------

User:
"Find the latest news about OpenAI and summarize it."

Output:
{{
    "steps": [
        {{
            "agent": "Search Agent",
            "task": "Find and summarize the latest news about OpenAI."
        }}
    ]
}}

--------------------------------

User:
"Find the latest AI regulations in Europe and compare them with the indexed documents."

Output:
{{
    "steps": [
        {{
            "agent": "Search Agent",
            "task": "Find the latest AI regulations in Europe."
        }},
        {{
            "agent": "Knowledge Agent",
            "task": "Compare the retrieved regulations with the indexed documents and summarize the differences."
        }}
    ]
}}

Return ONLY the JSON object.
"""

        response = self.llm.invoke(prompt)
        content = response.content[0]["text"] if isinstance(response.content, list) else response.content

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
                result = normalize_result(result)
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
        print(results)

        final = await self.finalize(query, results)


        return final