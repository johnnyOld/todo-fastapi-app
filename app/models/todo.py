from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime, timezone
from app.db.session import Base

class ToDo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    due_date = Column(DateTime, nullable=True)  # срок дедлайна
    priority = Column(Integer, default=1)  # 1 - низкий, 2 - средний, 3 - высокий
    user_id = Column(Integer, ForeignKey("users.id"))  # связь с пользователем

    user = relationship("User", back_populates="todos")