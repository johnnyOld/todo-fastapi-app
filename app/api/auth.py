from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import Token
from app.core.security import authenticate_user, create_access_token, get_password_hash
from app.core.config import ACCESS_TOKEN_EXPIRE_DELTA
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.models.user import User
from app.dependencies import get_db

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login")
async def login_with_cookie(request: Request, email: str = Form(...), password: str = Form(...),db: Session = Depends(get_db) ):
    user = authenticate_user(db,email, password)
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Неверные данные"})

    access_token = create_access_token(data={"sub": user.email})
    response = RedirectResponse(url="/todo", status_code=302)
    # response.set_cookie("access_token", value=f"Bearer {access_token}", httponly=True)
    response.set_cookie(key="access_token",value=access_token,httponly=True,samesite="lax")
    return response

@router.post("/register")
async def register(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    username = form["username"]
    full_name = form["full_name"]
    email = form["email"]
    password = form["password"]
    hashed_password = get_password_hash(password)

    user = db.query(User).filter(User.username == username).first()
    if user:
        return HTMLResponse("Пользователь уже существует", status_code=400)

    new_user = User(username=username,full_name=full_name, email=email,hashed_password=hashed_password)
    db.add(new_user)
    db.commit()

    return RedirectResponse(url="/login", status_code=302)

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/logout", response_class=HTMLResponse)
async def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("access_token")
    response.headers["Cache-Control"] = "no-store"  # Отключаем кэширование страницы
    response.headers["Pragma"] = "no-cache"
    return response

@router.get("/register")
async def logout(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

