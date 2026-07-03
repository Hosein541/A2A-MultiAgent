> ## Documentation Index
>
> Fetch the complete documentation index at: [/llms.txt](https://docs.langchain.com/llms.txt)
>
> Use this file to discover all available pages before exploring further.

[Skip to main content](https://docs.langchain.com/oss/python/langchain/agents#content-area)

An agent is a model calling tools in a loop until a given task is complete.![Core agent loop diagram](https://mintcdn.com/langchain-5e9cc07a/jtty0O--UJOKG0nK/oss/images/core_agent_loop.svg?fit=max&auto=format&n=jtty0O--UJOKG0nK&q=85&s=4b4cbb497b6273758a565de1bc90ece0)

**Agent = Model + Harness**The job of a harness: get the model the right context at the right time for the given task.

A harness is everything around that loop: the model, its prompt, its tools, and any middleware that shapes its behavior.[`create_agent`](https://reference.langchain.com/python/langchain/agents/factory/create_agent) is a highly configurable harness. At its simplest, you can create one with:

Google

OpenAI

Anthropic

OpenRouter

Fireworks

Baseten

Ollama

```
from langchain.agents import create_agent

agent = create_agent(model="google_genai:gemini-3.5-flash", tools=tools)
```

Building on that, you can configure the basics directly with the `model=`, `tools=`, and `system_prompt=` parameters. For more advanced capabilities, extend the harness with [middleware](https://docs.langchain.com/oss/python/langchain/agents#configure-the-harness).

## [​](https://docs.langchain.com/oss/python/langchain/agents\#core-components)  Core components

![Agent model and harness components diagram](https://mintcdn.com/langchain-5e9cc07a/jtty0O--UJOKG0nK/oss/images/agent_model_harness.svg?fit=max&auto=format&n=jtty0O--UJOKG0nK&q=85&s=5ac6a7e0343af7cb5ba3ca632e2224af)

### [​](https://docs.langchain.com/oss/python/langchain/agents\#model)  Model

Pass a model identifier string (`"provider:model"`) or an initialized model instance to select the model for your agent. See [Models](https://docs.langchain.com/oss/python/langchain/models) for parameters, provider setup, and dynamic model selection.

Google

OpenAI

Anthropic

OpenRouter

Fireworks

Baseten

Ollama

```
from langchain.agents import create_agent

agent = create_agent(model="google_genai:gemini-3.5-flash", tools=tools)
```

### [​](https://docs.langchain.com/oss/python/langchain/agents\#tools)  Tools

To provide the agent with tools, pass any Python callable, LangChain tool, or tool dict. See [Tools](https://docs.langchain.com/oss/python/langchain/tools) for tool definition, context access, and dynamic tool selection.

Google

OpenAI

Anthropic

OpenRouter

Fireworks

Baseten

Ollama

```
from langchain.agents import create_agent
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

agent = create_agent(model="google_genai:gemini-3.5-flash", tools=[search])
```

### [​](https://docs.langchain.com/oss/python/langchain/agents\#system-prompt)  System prompt

Shape how the agent approaches tasks. The system prompt parameter accepts a string or `SystemMessage`. For dynamic prompts at runtime, use [middleware](https://docs.langchain.com/oss/python/langchain/middleware).

Google

OpenAI

Anthropic

OpenRouter

Fireworks

Baseten

Ollama

```
agent = create_agent(
    model="google_genai:gemini-3.5-flash",
    tools=tools,
    system_prompt="You are a helpful assistant. Be concise and accurate.",
)
```

### [​](https://docs.langchain.com/oss/python/langchain/agents\#structured-output)  Structured output

Return a validated schema from the agent using `response_format=`. See [Structured output](https://docs.langchain.com/oss/python/langchain/structured-output) for strategies and examples.

Google

OpenAI

Anthropic

OpenRouter

Fireworks

Baseten

Ollama

```
from pydantic import BaseModel
from langchain.agents import create_agent

class Answer(BaseModel):
    summary: str
    confidence: float

agent = create_agent(model="google_genai:gemini-3.5-flash", tools=tools, response_format=Answer)
result = agent.invoke({"messages": [{"role": "user", "content": "Summarize AI trends"}]})
result["structured_response"]  # Answer(summary=..., confidence=...)
```

## [​](https://docs.langchain.com/oss/python/langchain/agents\#invocation)  Invocation

Trace each step of this loop, debug tool calls, and evaluate agent outputs with [LangSmith](https://smith.langchain.com/?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=oss-langchain-agents). Follow the [tracing quickstart](https://docs.langchain.com/langsmith/trace-with-langchain) to get set up. We recommend you also set up [LangSmith Engine](https://docs.langchain.com/langsmith/engine) which monitors your traces, detects issues, and proposes fixes.

You can invoke an agent with a message. Behind the scenes that passes an update to the agent’s [`State`](https://docs.langchain.com/oss/python/langgraph/graph-api#state). All agents include a [sequence of messages](https://docs.langchain.com/oss/python/langgraph/use-graph-api#messagesstate) in their state; to invoke the agent, pass a new message along with a `thread_id` so the agent can persist and resume conversation history:

Google

OpenAI

Anthropic

OpenRouter

Fireworks

Baseten

Ollama

```
from langchain.agents import create_agent
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    model="google_genai:gemini-3.5-flash",
    tools=[],
    checkpointer=InMemorySaver(),
)

config = {"configurable": {"thread_id": str(uuid7())}}

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]},
    config=config,
)

# A follow-up turn on the same conversation: reuse the same thread_id to keep history
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What about tomorrow?"}]},
    config=config,
)
```

Persisting conversation history with `thread_id` requires the agent to be configured with a [checkpointer](https://docs.langchain.com/oss/python/langchain/long-term-memory). When deployed on [LangSmith](https://docs.langchain.com/langsmith/deployment), a checkpointer is provisioned automatically. Locally, pass one explicitly, for example `create_agent(..., checkpointer=InMemorySaver())`.

If you also need to pass per-run configuration (such as a user ID, API keys, or feature flags) to tools and middleware, pass it as `context` alongside `config`. Define the shape of that data with `context_schema` and access it through `runtime.context`:

Google

OpenAI

Anthropic

OpenRouter

Fireworks

Baseten

Ollama

```
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver

@dataclass
class Context:
    user_id: str

agent = create_agent(
    model="google_genai:gemini-3.5-flash",
    tools=[],
    context_schema=Context,
    checkpointer=InMemorySaver(),
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]},
    config={"configurable": {"thread_id": str(uuid7())}},
    context=Context(user_id="user-123"),
)
```

`thread_id` scopes the _conversation_ (message history, checkpoints), while `context` carries _per-run_ data your tools and middleware read at invocation time. Both are commonly passed together. See [tool context](https://docs.langchain.com/oss/python/langchain/tools#context) and [Runtime](https://docs.langchain.com/oss/python/langchain/runtime) for more.

## [​](https://docs.langchain.com/oss/python/langchain/agents\#streaming)  Streaming

`invoke` returns the final response at the end of a run. If an agent executes multiple tool calls, users often need progress updates before completion. Use streaming to surface intermediate messages and tool activity as they happen.

```
from langchain.messages import AIMessage, HumanMessage

stream = agent.stream_events(
    {"messages": [{"role": "user", "content": "Search for AI news and summarize the findings"}]},
    version="v3",
)
for snapshot in stream.values:
    # Each snapshot contains the full state at that point
    latest_message = snapshot["messages"][-1]
    if latest_message.content:
        if isinstance(latest_message, HumanMessage):
            print(f"User: {latest_message.content}")
        elif isinstance(latest_message, AIMessage):
            print(f"Agent: {latest_message.content}")
    elif latest_message.tool_calls:
        print(f"Calling tools: {[tc['name'] for tc in latest_message.tool_calls]}")
```

For streaming modes, event types, and UI patterns, see [Streaming](https://docs.langchain.com/oss/python/langchain/streaming).

## [​](https://docs.langchain.com/oss/python/langchain/agents\#configure-the-harness)  Configure the harness

`create_agent` is highly extensible. Middleware is the primitive for customization: each piece handles one concern, hooks into the agent loop at the right moment, and composes freely with any other. Take exactly what your use case needs and skip the rest.Common patterns are prebuilt as first-class middleware. You can build anything else as [custom middleware](https://docs.langchain.com/oss/python/langchain/middleware/custom).![Agent harness capabilities by category](https://mintcdn.com/langchain-5e9cc07a/jtty0O--UJOKG0nK/oss/images/agent_harness_capabilities.svg?fit=max&auto=format&n=jtty0O--UJOKG0nK&q=85&s=0ff671d72badd0844826660dfcb04391)As agents take on complex work, they need support across a few key areas. The middleware ecosystem provides:

[**Execution environment** \\
\\
Tools, filesystem, sandboxes, and code execution](https://docs.langchain.com/oss/python/langchain/agents#execution-environment)

[**Context management** \\
\\
Summarization, memory, skills, and prompt caching](https://docs.langchain.com/oss/python/langchain/agents#context-management)

[**Planning and delegation** \\
\\
Todo lists and subagents for parallel, isolated work](https://docs.langchain.com/oss/python/langchain/agents#planning-and-delegation)

[**Fault tolerance** \\
\\
Retries, fallbacks, and call limits](https://docs.langchain.com/oss/python/langchain/agents#fault-tolerance)

[**Guardrails** \\
\\
PII detection and content controls](https://docs.langchain.com/oss/python/langchain/agents#guardrails)

[**Steering** \\
\\
Human-in-the-loop approval before high-impact actions](https://docs.langchain.com/oss/python/langchain/agents#steering)

`create_deep_agent` pre-assembles this stack for long-running coding and research tasks (filesystem, summarization, subagents, and prompt caching included by default). See [Deep Agents](https://docs.langchain.com/oss/python/deepagents/harness) for the full prebuilt harness.

### [​](https://docs.langchain.com/oss/python/langchain/agents\#execution-environment)  Execution environment

Agents are especially useful when they can take action rather than just generate text. The execution environment gives the agent a workspace: tools it can call, a filesystem for reading and writing files across turns, and code execution for running scripts or shell commands.

Google

OpenAI

Anthropic

OpenRouter

Fireworks

Baseten

Ollama

```
from langchain.agents import create_agent
from deepagents.backends import StateBackend
from deepagents.middleware import FilesystemMiddleware

agent = create_agent(
    model="google_genai:gemini-3.5-flash",
    tools=[search],
    middleware=[FilesystemMiddleware(backend=StateBackend())],
)
```

See [`FilesystemMiddleware`](https://reference.langchain.com/python/deepagents/middleware/filesystem/FilesystemMiddleware), [Sandboxes](https://docs.langchain.com/oss/python/deepagents/sandboxes), [Interpreters](https://docs.langchain.com/oss/python/deepagents/interpreters).

### [​](https://docs.langchain.com/oss/python/langchain/agents\#context-management)  Context management

Every model call has a fixed context window. As an agent runs, that window fills with accumulating history, tool results, and intermediate steps. Summarization compresses history before overflow hits; memory loads persistent instructions at startup so knowledge carries across sessions; skills surface domain knowledge on demand rather than loading everything upfront.

Google

OpenAI

Anthropic

OpenRouter

Fireworks

Baseten

Ollama

```
from deepagents.backends import StateBackend
from deepagents.middleware import FilesystemMiddleware, MemoryMiddleware, SkillsMiddleware, SummarizationMiddleware

backend = StateBackend()
model="google_genai:gemini-3.5-flash"

agent = create_agent(
    model=model,
    tools=[search],
    middleware=[\
        FilesystemMiddleware(backend=backend),\
        SummarizationMiddleware(model=model, backend=backend),\
        MemoryMiddleware(backend=backend, sources=["./AGENTS.md"]),\
        SkillsMiddleware(backend=backend, sources=["./skills/"]),\
    ],
)
```

See [`SummarizationMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/summarization/SummarizationMiddleware), [`MemoryMiddleware`](https://reference.langchain.com/python/deepagents/middleware/memory/MemoryMiddleware), [Skills](https://docs.langchain.com/oss/python/langchain/multi-agent/skills), [Context engineering](https://docs.langchain.com/oss/python/deepagents/context-engineering).

### [​](https://docs.langchain.com/oss/python/langchain/agents\#planning-and-delegation)  Planning and delegation

Complex tasks often exceed what one context window can handle. Delegation lets the main agent break work into pieces, hand them to subagents that each run in their own isolated context, and stay focused on coordination rather than execution. Work can run in parallel; the main agent’s context stays clean.

Google

OpenAI

Anthropic

OpenRouter

Fireworks

Baseten

Ollama

```
from deepagents.backends import StateBackend
from deepagents.middleware import FilesystemMiddleware
from deepagents.middleware.subagents import SubAgentMiddleware
from langchain.agents import create_agent
from langchain.agents.middleware import TodoListMiddleware
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for a query and return a short summary."""
    return f"Search results for: {query}"

backend = StateBackend()

agent = create_agent(
    model="google_genai:gemini-3.5-flash",
    tools=[search],
    middleware=[\
        FilesystemMiddleware(backend=backend),\
        TodoListMiddleware(),\
        SubAgentMiddleware(\
            backend=backend,\
            subagents=[\
                {\
                    "name": "researcher",\
                    "description": "Searches and returns a structured summary.",\
                    "system_prompt": "Use the search tool to research the question and summarize key points.",\
                    "tools": [search],\
                    "model": "anthropic:claude-sonnet-4-6",\
                    "middleware": [],\
                }\
            ],\
        ),\
    ],
)
```

See [Subagents](https://docs.langchain.com/oss/python/langchain/multi-agent/subagents).

### [​](https://docs.langchain.com/oss/python/langchain/agents\#name-your-agent)  Name your agent

Optionally use an identifier for the agent. This is especially useful when embedding the agent as a subgraph in [multi-agent](https://docs.langchain.com/oss/python/langchain/multi-agent) systems.

Google

OpenAI

Anthropic

OpenRouter

Fireworks

Baseten

Ollama

```
agent = create_agent(model="google_genai:gemini-3.5-flash", tools=tools, name="research_assistant")
```

### [​](https://docs.langchain.com/oss/python/langchain/agents\#fault-tolerance)  Fault tolerance

Agents in production encounter failures that rarely appear in development: rate limits, model timeouts, transient API errors. Fault tolerance middleware handles these at the infrastructure level so your tools and business logic don’t need try/catch around every call.

Google

OpenAI

Anthropic

OpenRouter

Fireworks

Baseten

Ollama

```
from langchain.agents import create_agent
from langchain.agents.middleware import ModelRetryMiddleware, ToolRetryMiddleware
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for a query and return a short summary."""
    return f"Search results for: {query}"

agent = create_agent(
    model="google_genai:gemini-3.5-flash",
    tools=[search],
    middleware=[\
        ModelRetryMiddleware(max_retries=3),\
        ToolRetryMiddleware(max_retries=2),\
    ],
)
```

See [`ModelRetryMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/model_retry/ModelRetryMiddleware), [`ToolRetryMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/tool_retry/ToolRetryMiddleware), [Prebuilt middleware](https://docs.langchain.com/oss/python/langchain/middleware/built-in).

### [​](https://docs.langchain.com/oss/python/langchain/agents\#guardrails)  Guardrails

Some policies can’t live in a prompt—they need to be enforced deterministically regardless of what the model does. Guardrails intercept data as it flows through the agent loop, applying compliance rules or content policies before tool results reach the model’s context.

Google

OpenAI

Anthropic

OpenRouter

Fireworks

Baseten

Ollama

```
from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for a query and return a short summary."""
    return f"Search results for: {query}"

agent = create_agent(
    model="google_genai:gemini-3.5-flash",
    tools=[search],
    middleware=[PIIMiddleware("email")],
)
```

See [`PIIMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/pii/PIIMiddleware), [Prebuilt middleware](https://docs.langchain.com/oss/python/langchain/middleware/built-in).

### [​](https://docs.langchain.com/oss/python/langchain/agents\#steering)  Steering

Full autonomy isn’t always appropriate. Steering lets you place humans at specific decision points—before destructive writes, expensive API calls, or anything requiring judgment—without restructuring your agent. The agent pauses and waits; a human approves, edits, or rejects; execution continues.

Google

OpenAI

Anthropic

OpenRouter

Fireworks

Baseten

Ollama

```
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """Search for a query and return a short summary."""
    return f"Search results for: {query}"

agent = create_agent(
    model="google_genai:gemini-3.5-flash",
    tools=[search],
    middleware=[HumanInTheLoopMiddleware(interrupt_on={"write_file": True})],
)
```

See [`HumanInTheLoopMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/human_in_the_loop/HumanInTheLoopMiddleware), [Human-in-the-loop](https://docs.langchain.com/oss/python/langchain/human-in-the-loop).

### [​](https://docs.langchain.com/oss/python/langchain/agents\#middleware-resources)  Middleware resources

[**Middleware overview** \\
\\
How the middleware stack works and when hooks fire](https://docs.langchain.com/oss/python/langchain/middleware/overview)

[**Prebuilt middleware** \\
\\
Full reference with configuration examples](https://docs.langchain.com/oss/python/langchain/middleware/built-in)

[**Custom middleware** \\
\\
Write your own hooks for business logic, PII scrubbing, and more](https://docs.langchain.com/oss/python/langchain/middleware/custom)

* * *

[Connect these docs](https://docs.langchain.com/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/agents.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

Was this page helpful?

YesNo

[Philosophy\\
\\
Previous](https://docs.langchain.com/oss/python/langchain/philosophy) [Models\\
\\
Next](https://docs.langchain.com/oss/python/langchain/models)

Ctrl+I

![Core agent loop diagram](https://mintcdn.com/langchain-5e9cc07a/jtty0O--UJOKG0nK/oss/images/core_agent_loop.svg?w=840&fit=max&auto=format&n=jtty0O--UJOKG0nK&q=85&s=5125947eb7307291580c343ee42de1c9)

![Agent model and harness components diagram](https://mintcdn.com/langchain-5e9cc07a/jtty0O--UJOKG0nK/oss/images/agent_model_harness.svg?w=840&fit=max&auto=format&n=jtty0O--UJOKG0nK&q=85&s=563567a285b524b80a1bd4d6230d1b6c)

![Agent harness capabilities by category](https://mintcdn.com/langchain-5e9cc07a/jtty0O--UJOKG0nK/oss/images/agent_harness_capabilities.svg?w=840&fit=max&auto=format&n=jtty0O--UJOKG0nK&q=85&s=b7b3863805722939afaa657b427c8ba5)