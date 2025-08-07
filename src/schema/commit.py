from pydantic import BaseModel
from conderser.data_extractor import DataExtractor
from wrappers.commit_wrapper import CommitMeta


class CommitMetaData(BaseModel):
    """retrieve commit metadata including author and commiter info, commit message, commit timestamp"""

    def __call__(self, extractor: DataExtractor) -> CommitMeta:
        return extractor.metadata()


class CommitCodeDiff(BaseModel):
    """retrieve commit code diff"""

    def __call__(self, extractor: DataExtractor) -> str:
        return extractor.code_diff()


TOOLS = [
    CommitMetaData,
    CommitCodeDiff
]
