from app.DB import models
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text


async def get_orgs_by_building(db: AsyncSession, building_id: int):
    result = await db.execute(
        select(models.Organization).filter(models.Organization.building_id == building_id)
    )
    return result.scalars().all()


async def get_organization(db: AsyncSession, org_id: int):
    result = await db.execute(
        select(models.Organization).filter(models.Organization.id == org_id)
    )
    return result.scalars().first()


async def search_orgs_by_name(db: AsyncSession, name: str):
    result = await db.execute(
        select(models.Organization).filter(models.Organization.name.contains(name))
    )
    return result.scalars().all()


async def get_orgs_in_radius(db: AsyncSession, lat: float, lon: float, radius_km: float):
    distance_clause = text("""
        (6371 * acos(cos(radians(:lat)) * cos(radians(latitude)) * 
        cos(radians(longitude) - radians(:lon)) + 
        sin(radians(:lat)) * sin(radians(latitude)))) <= :radius
    """)

    query = select(models.Organization).join(models.Building).filter(
        distance_clause.bindparams(lat=lat, lon=lon, radius=radius_km)
    )

    result = await db.execute(query)
    return result.scalars().all()


async def get_orgs_by_category_recursive(db: AsyncSession, category_id: int):
    cte_query = text("""
        WITH RECURSIVE cat_tree AS (
            SELECT id FROM categories WHERE id = :cat_id
            UNION ALL
            SELECT c.id FROM categories c 
            INNER JOIN cat_tree ct ON c.parent_id = ct.id
        )
            SELECT id FROM cat_tree
    """)

    res_ids = await db.execute(cte_query, {"cat_id": category_id})
    category_ids = res_ids.scalars().all()

    query = (
        select(models.Organization)
        .join(models.Organization.categories)
        .filter(models.Category.id.in_(category_ids))
        .distinct()
    )

    result = await db.execute(query)
    return result.scalars().all()
