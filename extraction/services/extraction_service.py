from typing import Optional, List

from pydantic import BaseModel

from extraction.ai.extractor import ValueItems, Extractor
from extraction.loader.docu_loader import DocuLoader


class ExtractionRequest(BaseModel):
    url: str


class ExtractionResponse(BaseModel):
    values: List[ValueItems]


class ExtractionService:
    """
    Contains business logic pertaining to value extraction.

    The class has single request/response based `handle` method.
    """

    def __init__(
        self,
        loader: DocuLoader,
        extractors: List[Extractor]
    ):
        self._loader = loader
        self._extractors = extractors

    def handle(
        self,
        request: ExtractionRequest
    ) -> Optional[ExtractionResponse]:

        documents = self._loader.load(request.url)

        if documents is None:
            return None

        values = []

        for extractor in self._extractors:
            value_items = extractor.extract(documents)
            values.append(value_items)

        return ExtractionResponse(
            values=values
        )
