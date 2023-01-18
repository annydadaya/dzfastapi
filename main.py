import fastapi
from fastapi import FastAPI, Depends, status
from typing import List
from sqlalchemy.orm import Session
import models
import schemas as _schema
import crud
from menu_db import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/v1/menus", response_model=List[_schema.Menus], status_code=200)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_all_menus(db)
    return users


@app.get("/api/v1/menus/{menu_id}", response_model=_schema.Menus, status_code=200)
def get_menu(menu_id: int, db: Session = Depends(get_db)):
    check = crud.check_menu(db, menu_id=menu_id)
    if check is None:
        raise fastapi.HTTPException(status_code=404, detail='menu not found')
    return check


@app.post("/api/v1/menus", response_model=_schema.Menus, status_code=201)
def read_menu(menu: _schema.MenuBase, db: Session = Depends(get_db)):
    new = crud.create_menu(db=db, menu=menu)
    return new


@app.patch("/api/v1/menus/{menu_id}", response_model=_schema.Menus, status_code=200)
def update_menu(menu_id: int, menu: _schema.MenuBase, db: Session = Depends(get_db)):
    check = crud.check_menu(db, menu_id=menu_id)
    if check is None:
        raise fastapi.HTTPException(status_code=404, detail='menu not found')
    return crud.update_menu(db, menu_id=menu_id, menu=menu)


@app.delete("/api/v1/menus/{menu_id}", status_code=200)
def read_delete_menu(menu_id: int, db: Session = Depends(get_db)):
    check = crud.check_menu(db, menu_id=menu_id)
    if check is None:
        raise fastapi.HTTPException(status_code=404, detail='menu not found')
    return crud.delete_menu(db, menu_id=menu_id)


@app.get("/api/v1/menus/{menu_id}/submenus", response_model=List[_schema.Subs], status_code=200)
def read_subs(menu_id: int, db: Session = Depends(get_db)):
    users = crud.get_all_subs(db, menu_id=menu_id)
    return users


@app.post("/api/v1/menus/{menu_id}/submenus", response_model=_schema.Subs, status_code=201)
def create_submenu(menu_id: int, item: _schema.SubBase, db: Session = Depends(get_db)):
    return crud.create_sub_menu(db=db, item=item, menu_id=menu_id)


@app.get("/api/v1/menus/{menu_id}/submenus/{sub_id}", response_model=_schema.Subs, status_code=200)
def read_submenu(menu_id: int, sub_id: int, db: Session = Depends(get_db)):
    check = crud.check_submenu(db, sub_id=sub_id)
    if check is None:
        raise fastapi.HTTPException(status_code=404, detail='submenu not found')
    return crud.get_submenu(db, menu_id=menu_id, sub_id=sub_id)


@app.patch("/api/v1/menus/{menu_id}/submenus/{sub_id}", response_model=_schema.Subs, status_code=200)
def read_sub(menu_id: int, sub_id: int, menu: _schema.SubBase, db: Session = Depends(get_db)):
    return crud.update_sub(db=db, menu_id=menu_id, sub_id=sub_id, menu=menu)


@app.delete("/api/v1/menus/{menu_id}/submenus/{sub_id}", status_code=200)
def delete_sub(menu_id: int, sub_id: int, db: Session = Depends(get_db)):
    check = crud.check_submenu(db, sub_id=sub_id)
    if check is None:
        raise fastapi.HTTPException(status_code=404, detail='submenu not found')
    return crud.delete_sub(db, menu_id=menu_id, sub_id=sub_id)


@app.get("/api/v1/menus/{menu_id}/submenus/{sub_id}/dishes", response_model=List[_schema.Dishes], status_code=200)
def read_all_d(menu_id: int, sub_id: int, db: Session = Depends(get_db)):
    return crud.get_all_dish(db=db, sub_id=sub_id, menu_id=menu_id)


@app.get("/api/v1/menus/{menu_id}/submenus/{sub_id}/dishes/{dish_id}", response_model=_schema.Dishes, status_code=200)
def get_dish(sub_id: int, dish_id: int, menu_id: int, db: Session = Depends(get_db)):
    return crud.get_dish(db=db, sub_id=sub_id, dish_id=dish_id, menu_id=menu_id)


@app.post("/api/v1/menus/{menu_id}/submenus/{sub_id}/dishes", response_model=_schema.Dishes, status_code=201)
def read_dish(item: _schema.Dishes, sub_id: int, db: Session = Depends(get_db)):
    return crud.create_dish(db=db, sub_id=sub_id, item=item)


@app.patch("/api/v1/menus/{menu_id}/submenus/{sub_id}/dishes/{dish_id}", response_model=_schema.Dishes, status_code=201)
def update_dish(item: _schema.Dishes, menu_id: int, sub_id: int, dish_id: int, db: Session = Depends(get_db)):
    return crud.update_dish(db=db, item=item, sub_id=sub_id, dish_id=dish_id, menu_id=menu_id)


@app.delete("/api/v1/menus/{menu_id}/submenus/{sub_id}/dishes/{dish_id}", status_code=200)
def delete_dish(dish_id: int, sub_id: int, db: Session = Depends(get_db)):
    return crud.delete_dish(db=db, dish_id=dish_id, sub_id=sub_id)
