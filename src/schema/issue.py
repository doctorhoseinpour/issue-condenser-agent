from pydantic import BaseModel, Field
from conderser.data_extractor import DataExtractor
from wrappers.issue_wrapper import CommentMeta, Pagination, LabelMeta
from typing import List
from datetime import datetime


class IssueAuthor(BaseModel):
    """username or handel of the issue author"""

    def __call__(self, extractor: DataExtractor) -> str:
        return extractor.issue_author()


class IssueTitleAndDescription(BaseModel):
    """
        Returns: a formated string with the issue title and description
    """

    def __call__(self, extractor: DataExtractor) -> str:
        return extractor.issue_title_and_description()


class IssueComments(BaseModel):
    """Retrieve paginated list of issue comments"""

    pagination: Pagination = Field(...,
                                   description="specify pagination from offset"
                                               " to at least offset + limit to retrieve comments slice")

    def __call__(self, extractor: DataExtractor) -> List[CommentMeta]:
        return extractor.issue_comments(pagination=self.pagination)


class IssueLabels(BaseModel):
    """get list of issue labels with their description"""

    def __call__(self, extractor: DataExtractor) -> List[LabelMeta]:
        return extractor.issue_labels()


class IssueCreatedAt(BaseModel):
    """get issue creation time"""

    def __call__(self, extractor: DataExtractor) -> datetime:
        return extractor.issue_created_at()


class IssueClosedAt(BaseModel):
    """get issue resolution time"""

    def __call__(self, extractor: DataExtractor) -> datetime:
        return extractor.issue_closed_at()


TOOLS = [
    IssueAuthor,
    IssueTitleAndDescription,
    IssueComments,
    IssueLabels,
    IssueCreatedAt,
    IssueClosedAt
]