from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fast_madr.routers import books, token, users
from fastapi.templating import Jinja2Templates



app = FastAPI()
app.include_router(users.router)
app.include_router(books.router)
app.include_router(token.router)


templates = Jinja2Templates(directory='fast_madr/templates')
app.mount("/static", StaticFiles(directory='fast_madr/static'), name='static')


@app.get('/', response_class=HTMLResponse)
async def read_rot(request: Request):
    return templates.TemplateResponse('index.html', {'request': request, 'title': 'page test'})

