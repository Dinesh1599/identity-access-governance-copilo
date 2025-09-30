from sqlalchemy import Integer, String, Boolean, ForeignKey, Table, Text, Column
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .db import Base


user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    external_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    upn: Mapped[str] = mapped_column(String(200), index=True) 
    display_name: Mapped[str] = mapped_column(String(200))
    department: Mapped[str] = mapped_column(String(100), default="")
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    roles: Mapped[list["Role"]] = relationship(
        "Role", secondary=user_roles, back_populates="users"
    )


class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[str] = mapped_column(Text, default="")

    users: Mapped[list[User]] = relationship(
        "User", secondary=user_roles, back_populates="roles"
    )


class Permission(Base):
    __tablename__ = "permissions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    resource: Mapped[str] = mapped_column(String(100), index=True)
    action: Mapped[str] = mapped_column(String(50))
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id"))


class Anomaly(Base):
    __tablename__ = "anomalies"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    raw_json: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), default="new")