from fast_madr.routers import users, books, token
from fastapi import FastAPI



app = FastAPI()
app.include_router(users.router)
app.include_router(books.router)
app.include_router(token.router)


@app.get("/")
def read_rot():
    return {"Hello": "Wold"}

