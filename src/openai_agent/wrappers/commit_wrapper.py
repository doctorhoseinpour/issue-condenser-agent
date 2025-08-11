from typing import Optional

from pydantic import BaseModel, Field
from github import Github, Commit


class CommitMeta(BaseModel):
    """Commit metadata format"""
    author_name: Optional[str] = Field(..., description="commit author name")
    author_email: Optional[str] = Field(..., description="commit author email")
    commiter_name: Optional[str] = Field(..., description="committer name")
    commiter_email: Optional[str] = Field(..., description="committer email")
    message: Optional[str] = Field(..., description="the commit message text")
    timestamp: str = Field(..., description="commit creation timestamp")


class CommitWrapper:
    def __init__(self, owner: str, repo_name: str, commit_hash: str, token: str | None = None):

        """
        Initialize the wrapper using the GitHub commit url
        Args:
            url (str): GitHub commit url
            token (str): the user's GitHub token (optional)
        """
        gh = Github(token) if token else Github()
        self.commit: Commit.Commit = gh.get_repo(f"{owner}/{repo_name}").get_commit(sha=commit_hash)

    def metadata(self) -> CommitMeta:
        """

        Returns: the commit metadata including author, commiter, message, and timestamp

        """
        return CommitMeta(
            author_name=self.commit.commit.author.name,
            author_email=self.commit.commit.author.email,
            commiter_name=self.commit.commit.committer.name,
            commiter_email=self.commit.commit.committer.email,
            message=self.commit.commit.message.strip(),
            timestamp=self.commit.commit.author.date.isoformat()
        )

    def code_diff(self) -> str:
        """

        Returns: commits code diff

        """
        diffs = []
        for file in self.commit.files:
            if file.patch:
                diffs.append(file.patch)

        return "\n\n".join(diffs)

