from typing import List

from langchain.chains.openai_functions import create_extraction_chain
from langchain_core.documents import Document
from langchain_core.language_models import BaseLLM
from langchain_core.prompts import PromptTemplate

from extraction.ai.extractor import ValueItems, Extractor, Value


class RatesExtractor(Extractor):

    def __init__(self, llm: BaseLLM):
        self._llm = llm

    def extract(self, documents: List[Document]) -> ValueItems:
        # Define the schema for table extraction
        schema = {
            "properties": {
                "plan_names": {"type": "array", "items": {"type": "string", "description": "Plan Names"}},
                "plan_rates": {"type": "array", "items": {"type": "string", "description": "Plan Rates"}},
                "deductibles": {"type": "array", "items": {"type": "string", "description": "Deductibles"}},
            },
            "required": ["plan_names", "plan_rates", "deductibles"]
        }

        # Create a prompt template
        prompt_template = PromptTemplate(
            input_variables=["text"],
            template="Extract health insurance policy records from the following text:\n\n{text}\n\nProvide the headers and table data as separate lists."
        )

        extraction_chain = create_extraction_chain(schema, self._llm, prompt=prompt_template)

        items = []

        # Extract table data from each document
        for document in documents:
            results = extraction_chain.run(document.page_content)
            print(document.page_content)
            print("---")
            if results:
                print(f"Headers: {results}")
                values_dict = {}
                for result_item in results:
                    if result_item["plan_names"] and len(result_item["plan_names"]) > 0:
                        values_dict["plan_name"] = Value(string_value=result_item["plan_names"][0])
                    if result_item["plan_rates"] and len(result_item["plan_rates"]) > 0:
                        values_dict["plan_rate"] = Value(string_value=result_item["plan_rates"][0])
                    if result_item["deductibles"] and len(result_item["deductibles"]) > 0:
                        values_dict["deductible"] = Value(string_value=result_item["deductibles"][0])

                    if len(values_dict) > 0:
                        items.append(values_dict)

        return ValueItems(title="Plans & Rates", items=items)
