from pydantic import BaseModel


class PlantCreate(BaseModel):
    name: str
    scientific_name: str | None = None
    category: str | None = None
    description: str | None = None
    image_path: str | None = None


class PlantOut(BaseModel):
    id: int
    name: str
    scientific_name: str | None = None
    category: str | None = None
    description: str | None = None
    image_path: str | None = None

    class Config:
        from_attributes = True
