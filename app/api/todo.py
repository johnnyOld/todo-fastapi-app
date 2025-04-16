from fastapi import APIRouter, Request,Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.todo import ToDo
from app.core.security import get_current_user_from_cookie
from app.dependencies import get_db

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/todo", response_class=HTMLResponse)
async def read_todo(request: Request, db: Session = Depends(get_db)):
    try:
        username = get_current_user_from_cookie(request)
    except:
        return RedirectResponse(url="/", status_code=302)

    user = db.query(User).filter(User.email == username).first()
    if not user:
        return RedirectResponse(url="/", status_code=302)

    priority = request.query_params.get("priority")

    todos_query = db.query(ToDo).filter(ToDo.user_id == user.id)

    if priority:
        try:
            todos_query = todos_query.filter(ToDo.priority == int(priority))
        except ValueError:
            pass  # Если priority был не числом — игнорируем

    todos = todos_query.order_by(ToDo.created_at.desc()).all()

    return templates.TemplateResponse("todos.html", {
        "request": request,
        "username": username,
        "todos": todos
    })

@router.post("/todo/create")
async def add_todo(request: Request,title: str = Form(...),description: str = Form(...),priority: str = Form(...),due_date: str = Form(None),db: Session = Depends(get_db)):
    try:
        email = get_current_user_from_cookie(request)
    except:
        return RedirectResponse(url="/", status_code=302)

    user = db.query(User).filter(User.email == email).first()
    if not user:
        return RedirectResponse(url="/", status_code=302)
    try:
        parsed_due_date = datetime.strptime(due_date, "%Y-%m-%d") if due_date else None
    except ValueError:
        return {"error": "Неверный формат даты. Используй ГГГГ-ММ-ДД."}

    new_todo = ToDo(
        title=title,
        description=description,
        due_date=parsed_due_date,
        priority=priority,
        user_id=user.id
    )
    db.add(new_todo)
    db.commit()

    return RedirectResponse(url="/todo", status_code=302)

@router.post("/todo/{todo_id}/delete")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(ToDo).filter(ToDo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    db.delete(todo)
    db.commit()
    return RedirectResponse(url="/todo", status_code=302)

@router.post("/todo/{todo_id}/toggle")
async def toggle_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(ToDo).filter(ToDo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    todo.completed = not todo.completed  # переключаем
    db.commit()
    return RedirectResponse(url="/todo", status_code=302)

