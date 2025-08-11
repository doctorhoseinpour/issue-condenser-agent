
from ollama_agent.wrappers.issue_wrapper import CommentMeta, Pagination, LabelMeta
from ollama_agent.wrappers.commit_wrapper import CommitMeta


class ControlToolBox:

    @staticmethod
    def finish(summary: str):
        """

        Args:
            summary (str): the resulting issue summary from the condensation process

        Returns: the final summary paragraph, finishing the process

        """
        return summary

    def get_tools(self):
        return [
            self.finish
        ]