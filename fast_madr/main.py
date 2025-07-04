from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from fast_madr.core.config import templates
from fast_madr.routers import books, profile_user, token, upload, users

app = FastAPI()
app.include_router(users.router)
app.include_router(books.router)
app.include_router(token.router)
app.include_router(profile_user.router)
app.include_router(upload.router)


app.mount('/static', StaticFiles(directory='fast_madr/static'), name='static')


@app.get('/', response_class=HTMLResponse)
async def read_rot(request: Request):
    return templates.TemplateResponse(
        'home.html', {'request': request, 'title': 'page test'}
    )
