
from ollama_agent.wrappers.issue_wrapper import CommentMeta, Pagination, LabelMeta
from ollama_agent.wrappers.commit_wrapper import CommitMeta, CommitWrapper


class CommitToolBox:

    def __init__(self, commit_wrapper: CommitWrapper):
        self.wrapper = commit_wrapper

    def commit_metadata(self) -> CommitMeta:
        """

        Returns: commit metadata including author and commiter info, commit message, commit timestamp

        """
        return self.wrapper.metadata()

    def commit_code_diff(self) -> str:
        """

        Returns: retrieve commit code diff

        """
        return self.wrapper.code_diff()

    def get_tools(self):
        return [
            self.commit_metadata,
            self.commit_code_diff,
        ]
