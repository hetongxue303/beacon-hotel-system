from fastapi import FastAPI
from core.config import settings
from core.events import events_listen

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESC,
    version=settings.APP_VERSION,
    debug=settings.APP_DEBUG,
    openapi_url=f'{settings.APP_API_PREFIX}/openapi.json'
)

events_listen(app)
