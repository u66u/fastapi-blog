from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from sqlalchemy.orm import Session

from core import auth, blog, user
from database.config import engine, get_db
from models import models


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.include_router(auth.router)
app.include_router(blog.router)
app.include_router(user.router)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    blogs = blog.get_all_blogs(db)
    return templates.TemplateResponse("index.html", {"request": request, "blogs": blogs})