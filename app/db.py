from datetime import datetime

from sqlalchemy import DateTime, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.config import DB_URL


class Base(DeclarativeBase):
    pass


class WebPage(Base):
    __tablename__ = "webpages"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    url: Mapped[str] = mapped_column(String(255))

    crawled_at: Mapped[datetime] = mapped_column(DateTime, default_factory=datetime.now)


engine = create_engine(DB_URL, echo=True)
