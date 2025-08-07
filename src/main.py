from conderser.data_extractor import DataExtractor
from conderser.agent import Agent
from wrappers.commit_wrapper import CommitWrapper
from wrappers.issue_wrapper import IssueWrapper

from schema.issue import TOOLS as ISSUE_TOOLS
from schema.commit import TOOLS as COMMIT_TOOLS
from schema.control import TOOLS as CONTROL_TOOLS

import re

if __name__ == "__main__":
    url = "https://github.com/kubernetes/kubernetes/issues/129138"
    match = re.search(r"github\.com/([^/]+)/([^/]+)/issues/(\d+)", url)

    if not match:
        raise ValueError("Invalid GitHub issue URL format.")

    owner = match.group(1)
    repo_name = match.group(2)
    issue_number = int(match.group(3))

    agent = Agent(
        owner=owner,
        repo_name=repo_name,
        issue_number=issue_number,
        commit_hash="d76f40d2f3999ea6953bb780e686a0148166b265"
    )

    agent.register_tools(ISSUE_TOOLS)
    agent.register_tools(COMMIT_TOOLS)
    agent.register_tools(CONTROL_TOOLS)

    print(agent.condense())
    print(agent.function_calls)
