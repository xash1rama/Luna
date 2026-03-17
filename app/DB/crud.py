from sqlalchemy.orm import Session
from sqlalchemy import text
from app.DB import models


# Поиск всех организаций в конкретном здании
def get_orgs_by_building(db: Session, building_id: int):
    return db.query(models.Organization).filter(models.Organization.building_id == building_id).all()


# Поиск организации по ID
def get_organization(db: Session, org_id: int):
    return db.query(models.Organization).filter(models.Organization.id == org_id).first()


# Поиск по названию
def search_orgs_by_name(db: Session, name: str):
    return db.query(models.Organization).filter(models.Organization.name.contains(name)).all()


# Поиск в радиусе (используем формулу Гаверсинуса для MariaDB)
def get_orgs_in_radius(db: Session, lat: float, lon: float, radius_km: float):
    # 6371 - средний радиус Земли в км
    distance_formula = text("""
        (6371 * acos(cos(radians(:lat)) * cos(radians(latitude)) * 
        cos(radians(longitude) - radians(:lon)) + 
        sin(radians(:lat)) * sin(radians(latitude))))
    """)

    return db.query(models.Organization).join(models.Building).filter(
        distance_formula.bindparams(lat=lat, lon=lon) <= radius_km
    ).all()


# Поиск по категории (включая вложенные)
def get_orgs_by_category_recursive(db: Session, category_id: int):
    # Рекурсивный запрос (CTE) для получения ID всех подкатегорий
    query = text("""
        WITH RECURSIVE cat_tree AS (
            SELECT id FROM categories WHERE id = :cat_id
            UNION ALL
            SELECT c.id FROM categories c 
            INNER JOIN cat_tree ct ON c.parent_id = ct.id
        )
        SELECT id FROM cat_tree
    """)
    category_ids = db.execute(query, {"cat_id": category_id}).scalars().all()

    return db.query(models.Organization).join(models.Organization.categories).filter(
        models.Category.id.in_(category_ids)
    ).distinct().all()