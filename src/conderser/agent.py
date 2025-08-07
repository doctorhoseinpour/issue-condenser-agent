from typing import List, Callable, Any
from openai.types.chat import ChatCompletionToolParam as Tool
from openai.types.chat import ChatCompletionMessageParam as Message
from openai.types.chat import ParsedChatCompletion
from openai import NotGiven, NOT_GIVEN
import openai
from pydantic import BaseModel
from conderser.data_extractor import DataExtractor
from wrappers.commit_wrapper import CommitWrapper
from schema.control import Finish
from prompt import MAX_ITERATIONS
from wrappers.issue_wrapper import IssueWrapper
import prompt


class Agent:
    def __init__(self,
                 owner: str,
                 repo_name: str,
                 issue_number: int,
                 commit_hash: str,
                 api_key: str = None,
                 ):
        self.client = openai.OpenAI(api_key=api_key) if api_key else openai.OpenAI()
        self.extractor = DataExtractor(
            IssueWrapper(
                owner=owner,
                repo_name=repo_name,
                issue_number=issue_number
            ),
            CommitWrapper(
                owner=owner,
                repo_name=repo_name,
                commit_hash=commit_hash
            )
        )
        self.tools = []
        self.function_calls: dict[str, int] = {}

    def register_tools(self, tools: List[type[BaseModel]]):
        """register all the tool function as openAI functions"""
        for tool in tools:
            self.tools.append(openai.pydantic_function_tool(tool))
            self.function_calls[tool.__name__] = 0

    def prompt(
            self,
            messages: List[Message],
            tools: List[Tool] | NotGiven = NOT_GIVEN,
    ) -> ParsedChatCompletion:
        """Communicate with the OpenAI API."""

        return self.client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=messages,
            tools=tools,
        )

    def condense(self) -> str | None:

        messages = [
            prompt.problem_explanation_prompt()
        ]

        for i in range(MAX_ITERATIONS - 1):
            print(len(messages))
            response = self.prompt(
                messages=messages,
                tools=self.tools
            ).choices[0].message

            messages.append(response)

            print(response.content)
            if response.tool_calls is None or len(response.tool_calls) == 0:
                messages.append(prompt.should_call_function())
                continue

            for tool_call in response.tool_calls:
                function: Callable[[DataExtractor], Any] = tool_call.function.parsed_arguments  # type: ignore

                if isinstance(function, Finish):
                    return function(self.extractor)
                else:
                    messages.append(prompt.function_call_result_prompt(tool_call, function(self.extractor)))
                    self.function_calls[tool_call.function.name] += 1
        else:
            messages.append(prompt.force_finish_prompt())
            response = self.prompt(
                messages=messages,
                tools=self.tools
            ).choices[0].message

            for tool_call in response.tool_calls:
                function: Callable[[DataExtractor], Any] = tool_call.function.parsed_arguments  # type: ignore
                if isinstance(function, Finish):
                    return function(self.extractor)

        return None


