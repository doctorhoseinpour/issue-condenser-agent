from wrappers.commit_wrapper import CommitWrapper
from wrappers.issue_wrapper import IssueWrapper
from typing import Any


class DataExtractor:
    def __init__(
            self,
            issue_wrapper: IssueWrapper,
            commit_wrapper: CommitWrapper
    ):
        """Initialize the Data Extractor instance.
        Args:
            issue_wrapper (IssueWrapper): The issue wrapper instance.
            git_wrapper (GitWrapper): The git wrapper instance.
            code_wrapper (CodeWrapper): The code wrapper instance.
        """
        self.issue_wrapper = issue_wrapper
        self.commit_wrapper = CommitWrapper
        self.wrappers = [issue_wrapper, commit_wrapper]

    def __getattr__(self, item) -> Any:
        """
        outsource function call to one of the wrappers that has the desired function
        Args:
            item (): function name

        Returns: function

        """
        for wrapper in self.wrappers:
            if hasattr(wrapper, item):
                return getattr(wrapper, item)
        return None
