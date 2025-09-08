from datetime import date
from sqlalchemy import Date, Numeric, text
from sqlalchemy.orm import Mapped, mapped_column, Session, DeclarativeBase


# Optional: coerce NUMERIC(38,0) <-> int transparently
from sqlalchemy.types import TypeDecorator

# Snowflake NUMBER(38,0) maps to NUMERIC(38, 0). Without IntNumeric, SQLAlchemy returns Decimal;
# Pydantic can handle it, but the decorator keeps it a plain int.


class IntNumeric(TypeDecorator):
    impl = Numeric
    cache_ok = True

    def __init__(self, precision=38, scale=0, **kw):
        super().__init__(precision=precision, scale=scale, **kw)

    def process_bind_param(self, value, dialect):
        return None if value is None else int(value)

    def process_result_value(self, value, dialect):
        return None if value is None else int(value)


class Base(DeclarativeBase):
    pass


class RepoCommitsByWeekModel(Base):
    __tablename__ = "repo_commits_by_week"

    # The table has no PK in DDL; ORM needs one. Using week as PK.
    week: Mapped[date] = mapped_column(
        Date, primary_key=True, nullable=False)

    # Use IntNumeric to get Python int instead of Decimal from Snowflake
    repo_commits_count: Mapped[int] = mapped_column(
        IntNumeric(38, 0), nullable=False, server_default=text("0")
    )
