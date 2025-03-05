from langchain_community.chat_models import ChatOpenAI

from extraction.ai.extractor import Extractor
from extraction.ai.rates_extractor import RatesExtractor
from extraction.loader.docu_loader import DocuLoader
from extraction.services.extraction_service import ExtractionService
from langchain.llms import OpenAI


class Factory:
    """
    Single class to where all functional objects are instantiated.
    """

    @staticmethod
    def create_loader() -> DocuLoader:
        return DocuLoader()

    @staticmethod
    def extractor() -> Extractor:
        # Initialize the language model
        llm = ChatOpenAI(temperature=0)

        return RatesExtractor(llm=llm)

    @staticmethod
    def create_service() -> ExtractionService:
        """
        Creates ExtractionService instance.

        :return: service object
        """
        return ExtractionService(
            loader=Factory.create_loader(),
            extractors=[Factory.extractor()]
        )
