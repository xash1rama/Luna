from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.DB.database import Base

org_category_association = Table(
    "org_category",
    Base.metadata,
    Column("organization_id", Integer, ForeignKey("organizations.id")),
    Column("category_id", Integer, ForeignKey("categories.id"))
)


class Building(Base):
    __tablename__ = "buildings"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    organizations = relationship("Organization", back_populates="building")


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    children = relationship("Category", backref="parent", remote_side=[id])


class Organization(Base):
    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    building_id = Column(Integer, ForeignKey("buildings.id"))

    building = relationship("Building", back_populates="organizations")
    phones = relationship("Phone", back_populates="organization")
    categories = relationship("Category", secondary=org_category_association)


class Phone(Base):
    __tablename__ = "phones"
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(20), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"))

    organization = relationship("Organization", back_populates="phones")
