
from ollama_agent.wrappers.issue_wrapper import CommentMeta, Pagination, LabelMeta, IssueWrapper
from ollama_agent.wrappers.commit_wrapper import CommitMeta
from datetime import datetime
from typing import List


class IssueToolBox:

    def __init__(self, issue_wrapper: IssueWrapper):
        self.wrapper = issue_wrapper

    def issue_author(self) -> str:
        """username or handel of the issue author"""

        return self.wrapper.issue_author()

    def issue_title_and_description(self) -> str:
        """
            Returns: a formated string with the issue title and description
        """

        return self.wrapper.issue_title_and_description()

    def issue_comments(self, pagination: Pagination) -> List[CommentMeta]:
        """

        Args:
            pagination (Pagination):  specify pagination from
            offset to at least offset + limit to retrieve comments slice

        Returns: Retrieve paginated list of issue comments

        """

        return self.wrapper.issue_comments(pagination=pagination)

    def issue_labels(self) -> List[LabelMeta]:
        """

        Returns: list of issue labels with their description

        """
        return self.wrapper.issue_labels()

    def issue_created_at(self) -> datetime:
        """

        Returns: get issue creation time

        """
        return self.wrapper.issue_created_at()

    def issue_closed_at(self) -> datetime:
        """

        Returns: get issue resolution time

        """
        return self.wrapper.issue_closed_at()

    def get_tools(self):
        return [
            self.issue_author,
            self.issue_title_and_description,
            self.issue_comments,
            self.issue_labels,
            self.issue_created_at,
            self.issue_closed_at,
        ]
