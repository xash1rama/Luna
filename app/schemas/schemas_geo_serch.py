from pydantic import BaseModel

class GeoSearch(BaseModel):
    lat: float
    lon: float
    radius_km: float
