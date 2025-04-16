from fastapi import FastAPI
from app.api import auth, todo
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles
from app.db.init import init_db


templates = Jinja2Templates(directory="app/templates")
app = FastAPI()
init_db()
app.include_router(auth.router)
app.include_router(todo.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})