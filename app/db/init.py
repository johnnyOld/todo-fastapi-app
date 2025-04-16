from app.models.user import User
from app.models.todo import ToDo
from app.db.session import engine, Base



def init_db():
    Base.metadata.create_all(bind=engine)