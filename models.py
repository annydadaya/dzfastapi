
from menu_db import Base
from sqlalchemy import String, Integer, Column, Text, Float, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.orm import query



def get_count(q):
    count_q = q.statement.with_only_columns([func.count()]).order_by(None)
    count = q.session.execute(count_q).scalar()
    return count


class Dish(Base):
    __tablename__ = 'dishc'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)

    submenu_id = Column(Integer, ForeignKey("submenu.id", ondelete='CASCADE'), nullable=False)

    submenuc = relationship("SubMenu", back_populates='dishs', cascade="all, delete")


class SubMenu(Base):
    __tablename__ = 'submenuc'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    dishes_count = Column(Integer, default=0)

    menu_id = Column(Integer, ForeignKey("menu.id", ondelete='CASCADE'), nullable=False)

    dishs = relationship("Dish", back_populates='submenuc', cascade="all, delete")
    menus = relationship("Menu", back_populates='subm', cascade="all, delete")


class Menu(Base):
    __tablename__ = 'menuc'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    submenus_count = Column(Integer, default=0)
    dishes_count = Column(Integer, default=0)

    subm = relationship("SubMenu", back_populates='menus', cascade="all, delete")
