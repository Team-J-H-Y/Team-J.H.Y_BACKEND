from sqlalchemy import select

from database.connection import SessionLocal
from database.models.users import Users


with SessionLocal() as db:
    statement = select(Users)

    result = db.scalars(statement).all()

    for row in result:
        print(row.id, row.name)