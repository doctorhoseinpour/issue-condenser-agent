from datetime import datetime
from typing import List

from github import Github
from pydantic import BaseModel, Field


class Pagination(BaseModel):
    """Pagination for listing comments"""

    offset: int = Field(..., description="offset from 0")
    limit: int = Field(..., description="limit of number of items to return. limit should not be less than 10")


class CommentMeta(BaseModel):
    """Comments metadata format"""
    author: str = Field(..., description="comment authors name or handel")
    body: str = Field(..., description="actual text body of the comment")
    created_at: str = Field(..., description="creation date of the comment")

    def __str__(self):
        return f"{self.author} {self.created_at}\nMessage:\n{self.body})"


class LabelMeta(BaseModel):
    """Issue label metadata format"""
    name: str = Field(..., description="name of the issue label")
    description: str = Field(..., description="full description of the issue label")


class IssueWrapper:
    def __init__(self, owner: str, repo_name: str, issue_number: int, token: str | None = None):
        """
        initialize the issue wrapper using the issue url from GitHub
        Args:
            url (str): the issue url from GitHub
            token (str): the users GitHub token (optional)
        """

        gh = Github(token) if token else Github()
        self.issue_data = (
            gh.get_repo(f"{owner}/{repo_name}").get_issue(number=issue_number)
        )

    def issue_author(self) -> str:
        """

        Returns: username or handel of the issue author

        """
        return self.issue_data.user.login

    def issue_title_and_description(self) -> str:
        """
        Returns: a formated string with the issue title and description included
        """
        return f"Title: {self.issue_data.title}\n Description: {self.issue_data.body}"

    def issue_comments(self, pagination: Pagination) -> List[CommentMeta]:
        """
        Args:
            pagination (Pagination): specifies desired slice from the list of comments

        Returns: The selected slice from the full list of comments
        """
        result = []
        comments = self.issue_data.get_comments()[pagination.offset: pagination.offset + pagination.limit]
        for c in comments:
            result.append(
                CommentMeta(
                    author=c.user.login,
                    body=c.body,
                    created_at=str(c.created_at)
                )
            )
        return result

    def issue_labels(self) -> List[LabelMeta]:
        """

        Returns: full list of labels attributed to the issue

        """
        result = []
        for label in self.issue_data.labels:
            result.append(
                LabelMeta(
                    name=label.name,
                    description=label.description
                )
            )
        return result

    def issue_created_at(self) -> datetime:
        """

        Returns: issue creation time

        """
        return self.issue_data.created_at

    def issue_closed_at(self) -> datetime:
        """

        Returns: issue resolution time

        """
        return self.issue_data.closed_at
