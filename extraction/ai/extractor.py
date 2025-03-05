from abc import ABC, abstractmethod
from typing import Optional, List, Dict

from langchain_core.documents import Document
from pydantic import BaseModel, Field


class Value(BaseModel):
    int_value: Optional[int] = Field(default=None)
    float_value: Optional[float] = Field(default=None)
    string_value: Optional[str] = Field(default=None)


class ValueItems(BaseModel):
    items: List[Dict[str, Value]]
    title: str


class Extractor(ABC):
    """
    Base/Abstract class for extracting insurance values
    """

    @abstractmethod
    def extract(self, documents: List[Document]) -> ValueItems:
        """
        Extracts values from documents
        """
        pass