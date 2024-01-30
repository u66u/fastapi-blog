from typing import List

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session


router = APIRouter(tags=["Blogs"], prefix="/blog")
db = database.connect()

@router.get("/", response_model=List[schemas.ShowBlog])
def get_all_blogs(
    db: Session = Depends(get_db)):
    return blog.get_all(db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(
    request: schemas.Blog,
    db: Session = Depends(get_db),
):
    return blog.create(request, db)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def get_blog_by_id(
    id: int,
    response: Response,
    current_user: schemas.User = Depends(get_current_user),
):
    ...
