from pydantic import BaseModel, Field

from conderser.data_extractor import DataExtractor


class Finish(BaseModel):
    """Finishes the process by returning the summary paragraph"""

    summary: str = Field(..., description="the resulting issue summary from the condensation process")

    def __call__(self, _: DataExtractor):
        return self.summary


TOOLS = [Finish]