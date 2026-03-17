from fastapi import Depends, HTTPException, Query, APIRouter
from sqlalchemy.orm import Session
from typing import List

from app.DB.database import get_db
from app.DB import crud
from app import auth
from app.schemas import schemas_organization

router = APIRouter(tags=["Organization"])

@router.get("/buildings/{building_id}/organizations",
         response_model=List[schemas_organization.Organization],
         dependencies=[Depends(auth.verify_api_key)])
def read_organizations_by_building(building_id: int, db: Session = Depends(get_db)):
    """Список всех организаций, находящихся в конкретном здании"""
    return crud.get_orgs_by_building(db, building_id=building_id)


@router.get("/organizations/category/{category_id}",
         response_model=List[schemas_organization.Organization],
         dependencies=[Depends(auth.verify_api_key)])
def read_organizations_by_category(category_id: int, db: Session = Depends(get_db)):
    """
    Поиск организаций по виду деятельности.
    Включает все вложенные подкатегории (рекурсивно).
    """
    return crud.get_orgs_by_category_recursive(db, category_id=category_id)


@router.get("/organizations/search/geo",
         response_model=List[schemas_organization.Organization],
         dependencies=[Depends(auth.verify_api_key)])
def search_organizations_geo(
    lat: float = Query(..., description="Широта"),
    lon: float = Query(..., description="Долгота"),
    radius_km: float = Query(..., description="Радиус поиска в км"),
    db: Session = Depends(get_db)
):
    """Список организаций в заданном радиусе от точки"""
    return crud.get_orgs_in_radius(db, lat=lat, lon=lon, radius_km=radius_km)


@router.get("/organizations/{org_id}",
         response_model=schemas_organization.Organization,
         dependencies=[Depends(auth.verify_api_key)])
def read_organization(org_id: int, db: Session = Depends(get_db)):
    """Вывод информации об организации по её идентификатору"""
    db_org = crud.get_organization(db, org_id=org_id)
    if db_org is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return db_org


@router.get("/organizations/search/name",
         response_model=List[schemas_organization.Organization],
         dependencies=[Depends(auth.verify_api_key)])
def search_organizations_by_name(name: str = Query(...), db: Session = Depends(get_db)):
    """Поиск организации по названию"""
    return crud.search_orgs_by_name(db, name=name)