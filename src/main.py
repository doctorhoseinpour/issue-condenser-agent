from ollama_agent.condenser.agent import Agent
from ollama_agent.wrappers.issue_wrapper import IssueWrapper
from ollama_agent.wrappers.commit_wrapper import CommitWrapper
from ollama_agent.toolbox.issue_toolbox import IssueToolBox
from ollama_agent.toolbox.commit_toolbox import CommitToolBox
from ollama_agent.toolbox.control_toolbox import ControlToolBox
import re
import asyncio

async def main():
    url = "https://github.com/kubernetes/kubernetes/issues/129138"
    match = re.search(r"github\.com/([^/]+)/([^/]+)/issues/(\d+)", url)

    if not match:
        raise ValueError("Invalid GitHub issue URL format.")

    owner = match.group(1)
    repo_name = match.group(2)
    issue_number = int(match.group(3))

    issue_toolbox = IssueToolBox(
        issue_wrapper=IssueWrapper(
            owner=owner,
            repo_name=repo_name,
            issue_number=issue_number
        )
    )

    commit_toolbox = CommitToolBox(
        commit_wrapper=CommitWrapper(
            owner=owner,
            repo_name=repo_name,
            commit_hash="d76f40d2f3999ea6953bb780e686a0148166b265"
        )
    )

    control_toolbox = ControlToolBox()

    agent = Agent()
    agent.register_tools(issue_toolbox.get_tools())
    agent.register_tools(commit_toolbox.get_tools())
    agent.register_tools(control_toolbox.get_tools())

    res = await agent.call_all_tools()

    print(res)

if __name__ == "__main__":
    asyncio.run(main())
