import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from api.user_router import user_router
from middlewares.auth_middleware import get_api_key
from utils.config import init_config
from utils.session import init_orm

APP_DESCRIPTION = """
Generative AI Technologies Research
"""

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_config()
    init_orm()
    yield

app: FastAPI = FastAPI(
    title='AI Copilot',
    description=APP_DESCRIPTION,
    version='0.0.1',
    lifespan=lifespan,
)

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(user_router, dependencies=[Depends(get_api_key)])

@app.get('/api/health')
async def health_check():
    return {'status': 'OK'}

@app.get('/', include_in_schema=False)
async def docs_redirect() -> RedirectResponse:
    return RedirectResponse(url='/docs')

def start(host='0.0.0.0', port=8000, reload=False, config_file=None):
    if config_file:
        os.environ['COMM-TEAM-AI-PROJECT'] = config_file

    uvicorn.run('main:app', host=host, port=port, reload=reload, workers=1)

if __name__ == '__main__':
    start()
