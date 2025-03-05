from typing import List

import requests
import os
import tempfile

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredExcelLoader
from urllib.parse import urlparse


from langchain_core.documents import Document


class DocuLoader:
    """
    Loads a document from given source location.
    """

    def load(self, path: str) -> List[Document]:

        if path.lower().startswith("http"):
            path = self._download_file(path)

        extension = self._get_file_extension(path).lower()

        if extension == "pdf":
            loader = PyPDFLoader(path)
        elif extension == "xlsx":
            loader = UnstructuredExcelLoader(path)
        else:
            raise Exception(f"Unsupported file format (.{extension}).")

        return loader.load()

    def _get_file_extension(self, file_path: str) -> str:
        # Split the file path and get the file name
        file_name = os.path.basename(file_path)

        # Split the file name and extension
        _, extension = os.path.splitext(file_name)

        # Remove the dot from the extension and return

        if extension:
            return extension[1:]
        else:
            raise Exception("Invalid file (extension is missing).")

    def _download_file(self, url: str) -> str:
        """
        Downloads file to local temp dir
        """

        # Send a GET request to the URL
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Extract the filename from the URL
        filename = os.path.basename(urlparse(url).path)
        if not filename:
            raise Exception("File name is missing.")

        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create the full file path in the temporary directory
            filepath = os.path.join(temp_dir, filename)

            # Open the file in binary write mode and write the content
            with open(filepath, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            print(f"File downloaded successfully: {filepath}")

            # Here you can process the file as needed
            # The file will be automatically deleted when we exit this block

            # If you need to keep the file, you should copy it to a permanent location here

            return filepath
