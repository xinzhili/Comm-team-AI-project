from typing import Optional

from cachetools.func import ttl_cache
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

EXCLUDED_PATHS = ['/', '/docs', '/redoc', '/openapi.json']

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == 'OPTIONS' or request.url.path in EXCLUDED_PATHS:
            return await call_next(request)

        authorization = request.headers.get('authorization')
        if not authorization:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                                content={'message': 'authorization header is missing!!'})

        token = authorization.replace('Bearer', '')

        return await call_next(request)

    @staticmethod
    @ttl_cache(maxsize=128, ttl=1795) #30-min token expiry
    def verify_token(token):
        pass

api_key_header = APIKeyHeader(name='Authorization', auto_error=False)

async def get_api_key(api_authorization_header: Optional[str] = Depends(api_key_header)):
    if not api_authorization_header:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='authorization header is required')

    return api_authorization_header
