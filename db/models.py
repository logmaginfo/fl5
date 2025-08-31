import datetime
import secrets
import os
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship, Session, sessionmaker
from sqlalchemy import ForeignKey, String, BigInteger, text, Text, func, DateTime, create_engine, Boolean
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from flask_login import UserMixin
from sqlalchemy import select

from login.flaks_login import login_manager

load_dotenv()
USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

engine = create_async_engine(url=f"postgresql+asyncpg://{USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
                             echo=True, pool_pre_ping=True)
sync_engine = create_engine(url=f"postgresql+psycopg://{USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
                             echo=True)

async_session = async_sessionmaker(engine)
sync_session = sessionmaker(sync_engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Songs(Base):
    __tablename__ = 'songs'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    letter: Mapped[str] = mapped_column(String(5), nullable=True)
    group: Mapped[str] = mapped_column(String(200), nullable=True)
    album: Mapped[str] = mapped_column(String(200), nullable=True)
    albumru: Mapped[str] = mapped_column(String(200), nullable=True)
    name: Mapped[str] = mapped_column(String(200), nullable=True)
    nameru: Mapped[str] = mapped_column(String(200), nullable=True)
    url: Mapped[str] = mapped_column(String(200), nullable=True)
    text: Mapped[str] = mapped_column(Text, nullable=True)
    textru: Mapped[str] = mapped_column(Text, nullable=True)
    ln: Mapped[str] = mapped_column(String(10), nullable=True)

class Reading(Base):
    __tablename__ = 'reading'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    level: Mapped[str] = mapped_column(String(5), nullable=True)
    phonetics: Mapped[str] = mapped_column(String(50), nullable=True)
    title: Mapped[str] = mapped_column(String(300), nullable=True)
    titleru: Mapped[str] = mapped_column(String(300), nullable=True)
    text: Mapped[str] = mapped_column(Text, nullable=True)
    textru: Mapped[str] = mapped_column(Text, nullable=True)

class Words(Base):
    __tablename__ = 'words'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    level: Mapped[str] = mapped_column(String(5), nullable=True)
    theme: Mapped[str] = mapped_column(String(200), nullable=True)
    themeru: Mapped[str] = mapped_column(String(200), nullable=True)
    phonetics: Mapped[str] = mapped_column(String(50), nullable=True)
    word: Mapped[str] = mapped_column(String(200), nullable=True)
    trl: Mapped[str] = mapped_column(String(200), nullable=True)
    trt: Mapped[str] = mapped_column(String(300), nullable=True)
    past: Mapped[str] = mapped_column(String(200), nullable=True)
    past_trl: Mapped[str] = mapped_column(String(200), nullable=True)
    comm: Mapped[str] = mapped_column(String(200), nullable=True)
    comm_trl: Mapped[str] = mapped_column(String(200), nullable=True)
    comm_trt: Mapped[str] = mapped_column(String(200), nullable=True)

class Authors(Base):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    author: Mapped[str] = mapped_column(String(200), nullable=True)
    authoreng: Mapped[str] = mapped_column(String(200), nullable=True)

class Books(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_author: Mapped[int] = mapped_column(nullable=True)
    book: Mapped[str] = mapped_column(String(200), nullable=True)
    bookru: Mapped[str] = mapped_column(String(200), nullable=True)
    level: Mapped[str] = mapped_column(String(5), nullable=True)
    url: Mapped[str] = mapped_column(String(300), nullable=True)

class Booktexts(Base):
    __tablename__ = 'booktexts'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_book: Mapped[int] = mapped_column(nullable=True)
    texten: Mapped[str] = mapped_column(Text, nullable=True)
    textru: Mapped[str] = mapped_column(Text, nullable=True)

class Userseng3(Base, UserMixin):
# class Userseng3(Base):
    __tablename__ = 'userseng3'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nic: Mapped[str] = mapped_column(String(100), nullable=True)
    email: Mapped[str] = mapped_column(String(100), nullable=True)
    password: Mapped[str] = mapped_column(String(300), nullable=True)
    logo: Mapped[str] = mapped_column(String(200), nullable=True)
    phone: Mapped[str] = mapped_column(String(100), nullable=True)
    email_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    date_create: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

    reset_token : Mapped[str] = mapped_column(String(200), nullable=True)
    reset_token_expiry: Mapped[DateTime] =  mapped_column(DateTime, nullable=True)


    def set_reset_token(self):
        """Generate a secure token and set its expiration time (valid for 1 hour)"""
        self.reset_token = secrets.token_urlsafe(32)  # Generate a secure random token
        self.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
        return self.reset_token


    def verify_reset_token(self, token):
        """Verify if the reset token is valid and not expired"""
        if token != self.reset_token:
            return False
        if datetime.utcnow() > self.reset_token_expiry:
            return False
        return True

class UserWishList(Base):
    __tablename__ = 'userwishlist'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_user: Mapped[int] = mapped_column(nullable=True)
    wishlist: Mapped[str] = mapped_column(String(50), nullable=True)
    id_wishlist: Mapped[int] = mapped_column(nullable=True)


@login_manager.user_loader
def load_user(user_id):
    user_id = int(user_id)
    with sync_session() as session:
        return session.scalar(select(Userseng3).where(Userseng3.id == user_id))


Base.metadata.create_all(sync_engine)
