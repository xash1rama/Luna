from fastapi import Header, HTTPException, status
from app.core.conf import settings

async def verify_api_key(api_key: str = Header(..., alias="X-API-KEY")):
    if api_key != settings.STATIC_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing API Key"
        )
    return api_key