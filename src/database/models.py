from .connect import Base
from sqlalchemy import Column, String, Integer, DateTime, Boolean
from datetime import date, datetime
from sqlalchemy.inspection import inspect


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(25), nullable=False, unique=True)
    first_name = Column(String(25), nullable=False)
    last_name = Column(String(25), nullable=False)
    gender = Column(String(10), nullable=False, default="")
    profile = Column(String, nullable=False)
    password = Column(String(100), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    friends_list = Column(String, nullable=False, default="[]")
    dob = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


def model_to_dict(model):
    data = {c.key: getattr(model, c.key) for c in inspect(model).mapper.column_attrs}
    for key, value in data.items():
        data[key] = format_value(value)
    return data


def format_value(value):
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(value, date):
        return value.strftime("%Y-%m-%d")
    return value
