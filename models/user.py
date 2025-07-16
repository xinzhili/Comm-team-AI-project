import bcrypt
from fastapi import HTTPException
from sqlalchemy.dialects.postgresql import JSONB
from starlette import status

from models.base import Base
from sqlalchemy import (
    Column,
    DateTime,
    func,
    CHAR,
    Integer,
    select,
)

from schemas.user import UserCreate
from utils.logger import logger
from utils.session import get_async_session


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'testing'}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(CHAR(50), unique=True, index=True, nullable=False)
    email = Column(CHAR(100), unique=True, index=True, nullable=False)
    phone_number = Column(CHAR(11), unique=True, index=True, nullable=False)
    hashed_password = Column(CHAR(200), nullable=False)
    details = Column(JSONB, name='details', default=lambda: {})
    created_at = Column(DateTime(timezone=False), server_default=func.timezone('UTC', func.now()))
    last_modified_ts = Column(DateTime(timezone=False), server_default=func.timezone('UTC', func.now()),
                              onupdate=func.timezone('UTC', func.now()))
    password_reset_token = Column(CHAR(100), nullable=True)
    reset_token_expiry = Column(DateTime(timezone=False), nullable=True)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @classmethod
    async def get_user_by_user_name(cls, user_name) -> 'User':
        async with get_async_session() as session:
            result = await session.execute(
                select(cls)
                .where(cls.username == user_name)
                .order_by(cls.created_at.desc())
                .limit(1)
            )

            return result.scalars().first()

    @classmethod
    async def get_user_by_email(cls, email) -> 'User':
        async with get_async_session() as session:
            result = await session.execute(
                select(cls)
                .where(cls.username == email)
                .order_by(cls.created_at.desc())
                .limit(1)
            )

            return result.scalars().first()

    @classmethod
    async def get_by_user_id(cls, user_id: int) -> 'User':
        logger.info(f'Getting user details, user id: {user_id}')

        async with get_async_session() as session:
            user = await session.get(cls, user_id)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f'User Id {{{user_id}}} not existing')

        logger.info(f'Get User details successfully, user id: {user_id}')
        return user

    @classmethod
    async def get_all(cls) -> list['User']:
        logger.info(f'Getting all users')

        async with get_async_session() as session:
            result = await session.execute(
                select(cls)
                .order_by(cls.created_at.desc())
            )
            users = result.scalars().all()

        logger.info(f'Get all Users successfully')
        return users

    @classmethod
    async def register(cls, user_register_request: UserCreate, details: dict=None) -> 'User':
        user = await cls.get_user_by_user_name(user_name=user_register_request.username)
        if user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Username {user_register_request.username} already registered')

        existing_user = await cls.get_user_by_email(email=user_register_request.email)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Email {user_register_request.email} already registered')

        hashed_password = cls.get_password_hash(user_register_request.password)
        async with get_async_session() as session:
            new_user = cls(
                username=user_register_request.username,
                email=user_register_request.email,
                phone_number=user_register_request.phone_number,
                hashed_password=hashed_password,
                details=details if details else {},
            )

            session.add(new_user)
            await session.flush()
            await session.refresh(new_user)

        logger.info(f'User: {new_user.username} created')
        return new_user

    @classmethod
    async def change_password(cls, user_name: str, current_password: str, new_password: str) -> dict:
        user = await cls.get_user_by_user_name(user_name=user_name)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'User: {user_name} not existing'
            )

        if not cls.verify_password(current_password, str(user.hashed_password)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Current password incorrect"
            )

        user.hashed_password = cls.get_password_hash(new_password)

        async with get_async_session() as session:
            session.add(user)
            await session.flush()
            await session.refresh(user)

        logger.info(f'Password changed for user: {user_name}')

        return {
            'message': 'Password changed successfully'
        }
