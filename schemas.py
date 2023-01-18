from pydantic import BaseModel  # сериализация для pydantic в json
import models
from models import get_count
from sqlalchemy.orm import Session


q = Session.query(models.Dish.id)
q1 = Session.query(models.SubMenu.id)

class MenuBase(BaseModel):
    title: str
    description: str


class Menus(MenuBase):
    id: str
    submenus_count: q1
    dishes_count: q

    class Config:           # для автоматической работы
        orm_mode = True


class SubBase(BaseModel):
    title: str
    description: str


class Subs(SubBase):
    id: str
    dishes_count: q

    class Config:
        orm_mode = True


class Dishes(BaseModel):
    title: str
    description: str
    price: str

    class Config:
        orm_mode = True
