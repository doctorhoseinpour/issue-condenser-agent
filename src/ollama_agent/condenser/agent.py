from typing import List, Callable

from llama_index.core.agent import AgentStream, ToolCallResult, ToolCall
from llama_index.core.base.llms.types import ChatMessage, MessageRole
from llama_index.core.tools import FunctionTool
from ollama_agent.wrappers.commit_wrapper import CommitWrapper
from ollama_agent.wrappers.issue_wrapper import IssueWrapper
from llama_index.core.agent.workflow import FunctionAgent
from openai_agent.prompt import PROBLEM_EXPLANATION_PROMPT, MAX_ITERATIONS
from llama_index.core.workflow import Context
from llama_index.llms.ollama import Ollama


class Agent:
    def __init__(self):
        self.tools = []

    def register_tools(self, tools: List[Callable]):
        for tool in tools:
            if tool.__name__ == "finish":
                self.tools.append(FunctionTool.from_defaults(tool, return_direct=True))
            else:
                self.tools.append(FunctionTool.from_defaults(tool))

    async def call_all_tools(self) -> str:
        agent = FunctionAgent(
            name="condenser agent",
            description="an agent that condenses the issue",
            tools=self.tools,
            system_prompt=PROBLEM_EXPLANATION_PROMPT,
            llm=Ollama(model="qwen3:4b"),

        )
        context = Context(agent)
        handler = agent.run(
            user_msg=ChatMessage(
                role=MessageRole.USER, content="please summarize the issue for me"
            ),
            ctx=context,
            max_iterations=50,
        )

        async for ev in handler.stream_events():
            if isinstance(ev, AgentStream):
                print(f"{ev.delta}", end="", flush=True)
                print("==============================================")

            elif isinstance(ev, ToolCallResult):
                print(
                    f"\nCall {ev.tool_name} with {ev.tool_kwargs}\nReturned: {ev.tool_output}"
                )
                print("==============================================")
            elif isinstance(ev, ToolCall):
                print(
                    f"\nCalling {ev.tool_name} with {ev.tool_kwargs}"
                )
                print("==============================================")

        response = await handler
        return str(response)
