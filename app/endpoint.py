from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
from .agent import run

router = APIRouter(prefix="/assistant", tags=["assistant"])


class AskAssistantRequest(BaseModel):
    question: str


@router.post("/ask")
async def ask_assistant(request: AskAssistantRequest) -> StreamingResponse:
    async def generate():
        async for message in run(request.question):
            yield json.dumps(message.model_dump()) + "\n"

    return StreamingResponse(
        generate(),
        media_type="application/x-ndjson",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )
