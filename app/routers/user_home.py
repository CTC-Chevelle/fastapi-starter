from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import status
from app.dependencies.session import SessionDep
from app.dependencies.auth import AuthDep
from app.models.todo import Todo
from sqlmodel import select
from typing import Annotated
from . import router, templates

@router.get("/app", response_class=HTMLResponse)
async def user_home_view(
    request: Request,
    user: AuthDep,
    db: SessionDep
):
    todos = db.exec(select(Todo).where(Todo.user_id == user.id)).all()
    return templates.TemplateResponse(
        request=request,
        name="todos.html",
        context={
            "user": user,
            "todos": todos
        }
    )

@router.post("/todos")
def create_todo(
    request: Request,
    text: Annotated[str, Form()],
    user: AuthDep,
    db: SessionDep
):
    todo = Todo(text=text, user_id=user.id)
    db.add(todo)
    db.commit()
    return RedirectResponse(url="/app", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/todos/toggle/{todo_id}")
def toggle_todo(
    request: Request,
    todo_id: int,
    user: AuthDep,
    db: SessionDep
):
    todo = db.exec(select(Todo).where(Todo.id == todo_id, Todo.user_id == user.id)).one_or_none()
    if todo:
        todo.done = not todo.done
        db.add(todo)
        db.commit()
    return RedirectResponse(url="/app", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/todos/delete/{todo_id}")
def delete_todo(
    request: Request,
    todo_id: int,
    user: AuthDep,
    db: SessionDep
):
    todo = db.exec(select(Todo).where(Todo.id == todo_id, Todo.user_id == user.id)).one_or_none()
    if todo:
        db.delete(todo)
        db.commit()
    return RedirectResponse(url="/app", status_code=status.HTTP_303_SEE_OTHER)