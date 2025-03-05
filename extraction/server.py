import os
from typing import Optional

import uvicorn

from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

from extraction.factory import Factory
from extraction.services.extraction_service import (
    ExtractionRequest, ExtractionResponse)

load_dotenv()
extraction_service = Factory.create_service()
app = FastAPI(title="Extraction API")


@app.post("/extract/{url}",
         response_model=ExtractionResponse)
async def extract_values(
        request: ExtractionRequest
) -> Optional[ExtractionRequest]:

    response = extraction_service.handle(
        request
    )

    if response is None:
        raise HTTPException(status_code=404, detail="Prospect not found")

    return response


def start():
    uvicorn.run(
        "extraction.server:app",
        host=os.getenv("HOST"),
        port=int(os.getenv("PORT"))
    )


if __name__ == "__main__":
    start()
