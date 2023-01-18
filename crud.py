from sqlalchemy.orm import Session
import models
import schemas as _schema


def get_all_menus(db: Session):
    return db.query(models.Menu).all()


def create_menu(db: Session, menu: _schema.MenuBase):
    new_menu = models.Menu(
        title=menu.title,
        description=menu.description
    )
    db.add(new_menu)
    db.commit()
    return new_menu


def check_menu(db: Session, menu_id: int):
    return db.query(models.Menu).filter(models.Menu.id == menu_id).first()


def update_menu(db: Session, menu_id: int, menu: _schema.MenuBase):
    menu_to_update = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    menu_to_update.title = menu.title
    menu_to_update.description = menu.description
    db.commit()
    db.refresh(menu_to_update)
    return menu_to_update


def delete_menu(db: Session, menu_id: int):
    db.query(models.Menu).filter(models.Menu.id == menu_id).delete()
    db.commit()
    return {
        "status": "true",
        "message": "The menu has been deleted"
        }


def get_all_subs(db: Session, menu_id: int):
    return db.query(models.SubMenu).filter(models.SubMenu.menu_id == menu_id).all()


def check_submenu(db: Session, sub_id: int):
    return db.query(models.SubMenu).filter(models.SubMenu.id == sub_id).first()


def get_submenu(db: Session, menu_id: int, sub_id: int):
    return db.query(models.SubMenu).filter(models.SubMenu.menu_id == menu_id and
                                           models.SubMenu.id == sub_id).first()


def create_sub_menu(db: Session, item: _schema.SubBase, menu_id: int):
    db_item = models.SubMenu(**item.dict(), menu_id=menu_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_sub(db: Session, menu_id: int, sub_id: int, menu: _schema.SubBase):
    menu_to_update = db.query(models.SubMenu).filter(models.SubMenu.menu_id == menu_id and
                                                     models.SubMenu.id == sub_id).first()
    menu_to_update.title = menu.title
    menu_to_update.description = menu.description
    db.commit()
    db.refresh(menu_to_update)
    return menu_to_update


def delete_sub(db: Session, menu_id: int, sub_id: int):
    db.query(models.SubMenu).filter(models.SubMenu.menu_id == menu_id and
                                    models.SubMenu.id == sub_id).delete()
    db.commit()
    return {
        "status": "true",
        "message": "The submenu has been deleted"
        }


def get_all_dish(db: Session, sub_id: int, menu_id):
    return db.query(models.Dish).join(models.SubMenu).join(models.Menu).filter(
        models.Dish.submenu_id == sub_id and models.SubMenu.menu_id == menu_id).all()


def get_dish(db: Session, sub_id: int, dish_id: int, menu_id: int):
    return db.query(models.Dish).join(models.SubMenu).join(models.Menu).filter(
        models.Dish.submenu_id == sub_id and models.SubMenu.menu_id == menu_id and
        models.Dish.id == dish_id).first()


def create_dish(db: Session, item: _schema.Dishes, sub_id: int):
    db_item = models.Dish(**item.dict(), submenu_id=sub_id)
    db.add(db_item)
    db.commit()
    return db_item


def update_dish(db: Session, item: _schema.Dishes, sub_id: int, dish_id: int, menu_id: int):
    db_item = db.query(models.Dish(**item.dict())).join(models.SubMenu.dishs).join(models.Menu.subm).filter(
        submenu_id=sub_id, id=dish_id, menu_id=menu_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_dish(db: Session, sub_id: int, dish_id: int, menu_id:int):
    db.query(models.Dish).filter(models.Dish.submenu_id == sub_id and
                                 models.Dish.id == dish_id and
                                 models.SubMenu.menu_id == menu_id).delete()
    db.commit()
    return {
        "status": "true",
        "message": "The dish has been deleted"
        }
