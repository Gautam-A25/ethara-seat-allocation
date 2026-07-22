from fastapi import APIRouter

from app.schemas.ai import (
    AIQueryRequest,
    AIQueryResponse,
)
from app.services.ai_service import process_ai_query

router = APIRouter(
    prefix="/ai",
    tags=["AI Assistant"],
)


@router.post(
    "/query",
    response_model=AIQueryResponse,
    summary="AI Assistant Query",
)
def ai_query(
    request: AIQueryRequest,
):
    answer = process_ai_query(request.query)

    return AIQueryResponse(
        answer=answer,
    )