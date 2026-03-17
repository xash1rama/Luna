import random

from fastapi import FastAPI
from app.routers.routers_organization import router
from app.DB.database import SessionLocal, Base, engine
from app.DB import models
import time

app = FastAPI(
    title="Справочник Организаций API",
    description="REST API для работы с организациями, зданиями и деятельностью",
    version="1.0.0"
)

app.include_router(router)


def seed_db():
    time.sleep(10)
    db = SessionLocal()
    if db.query(models.Building).first():
        db.close()
        return

    categories = []
    for i in range(5):
        cat = models.Category(name=f"Сфера {i + 1}", parent_id=None)
        db.add(cat)
        db.flush()  # Получаем ID
        categories.append(cat)

    l2_categories = []
    for i in range(10):
        parent = random.choice(categories)
        cat = models.Category(name=f"Подсфера {i + 1}", parent_id=parent.id)
        db.add(cat)
        db.flush()
        l2_categories.append(cat)

    all_leaf_categories = []
    for i in range(5):
        parent = random.choice(l2_categories)
        cat = models.Category(name=f"Услуга {i + 1}", parent_id=parent.id)
        db.add(cat)
        db.flush()
        all_leaf_categories.append(cat)

    all_categories = categories + l2_categories + all_leaf_categories

    buildings = []
    for i in range(40):
        # Генерируем координаты вокруг условного центра (Москва)
        lat = 55.75 + random.uniform(-0.1, 0.1)
        lon = 37.61 + random.uniform(-0.1, 0.1)
        b = models.Building(
            address=f"ул. Тестовая {i + 1}, д. {random.randint(1, 100)}",
            latitude=lat,
            longitude=lon
        )
        db.add(b)
        db.flush()
        buildings.append(b)

    for i in range(500):
        org = models.Organization(
            name=f"Компания {i + 1} (ООО {random.choice(['Альфа', 'Бета', 'Гамма'])})",
            building_id=random.choice(buildings).id
        )
        org.categories = random.sample(all_categories, k=random.randint(1, 2))
        db.add(org)
        db.flush()

        for _ in range(2):
            phone = models.Phone(
                number=f"8-900-{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}",
                organization_id=org.id
            )
            db.add(phone)

    db.commit()
    db.close()

seed_db()


