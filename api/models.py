from app import db
import datetime
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID


class Tasks(db.Model):
    """ Таблица Результаты парсинга """
    __tablename__ = "tasks"

    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, nullable=False, default=uuid4)
    date_created = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow())
    task = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False, default='pending')
