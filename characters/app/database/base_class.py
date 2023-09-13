from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext import asyncio


class Base(asyncio.AsyncAttrs, DeclarativeBase):
    pass
