from fastapi import HTTPException
from passlib.context import CryptContext
from asyncpg import UniqueViolationError

from db import database
from managers.auth import AuthManager
from models import user, RoleType

pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')  # set up for hashing password


class UserManager:

    @staticmethod
    async def register(user_data):
        user_data["password"] = pwd_context.hash(user_data['password'])  # hashing password
        try:
            id_ = await database.execute(user.insert().values(**user_data))
        except UniqueViolationError:
            raise HTTPException(400, "user with this email already exists")

        user_object = await database.fetch_one(user.select().where(user.c.id == id_))
        return AuthManager.encode_token(user_object)

    @staticmethod
    async def login(user_data):
        user_object = await database.fetch_one(user.select().where(user.c.email == user_data['email']))
        if not user_object:
            raise HTTPException(400, "wrong email or password")
        elif not pwd_context.verify(user_data['password'], user_object['password']):
            raise HTTPException(400, "wrong email or password")
        return AuthManager.encode_token(user_object)

    @staticmethod
    async def get_all_users():
        return await database.fetch_all(user.select())

    @staticmethod
    async def get_users_by_email(email):
        return await database.fetch_one(user.select().where(user.c.email == email))

    @staticmethod
    async def change_role(role: RoleType, user_id):
        return await database.execute(user.update().where(user.c.id == user_id).values(role=role))


