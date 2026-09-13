from pathlib import Path

from fastapi import Depends, FastAPI, File, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

import image_features
import models
from database import Base, engine, get_db
from schemas import PlantCreate
from seed import seed as seed_database


BASE_DIR = Path(__file__).resolve().parent
if (BASE_DIR / "index.html").exists():
    FRONTEND_DIR = BASE_DIR
elif (BASE_DIR.parent / "frontend" / "index.html").exists():
    FRONTEND_DIR = BASE_DIR.parent / "frontend"
else:
    FRONTEND_DIR = BASE_DIR / "frontend"

Base.metadata.create_all(bind=engine)
seed_database()

app = FastAPI(title="植物馆展览系统")
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


def plant_to_dict(plant):
    return {
        "id": plant.id,
        "name": plant.name,
        "scientific_name": plant.scientific_name,
        "category": plant.category,
        "description": plant.description,
        "image_path": plant.image_path,
    }


@app.get("/")
def index():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/api/image")
def get_image(path: str):
    image_path = Path(path)
    if not image_path.is_absolute():
        image_path = BASE_DIR / image_path

    try:
        image_path = image_path.resolve()
        image_path.relative_to(BASE_DIR)
    except ValueError:
        raise HTTPException(status_code=403, detail="非法图片路径")

    if not image_path.exists() or image_path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
        raise HTTPException(status_code=404, detail="图片不存在")

    return FileResponse(image_path)


@app.get("/api/plants")
def list_plants(
    q: str | None = Query(default=None),
    category: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(models.Plant)

    if q:
        keyword = f"%{q}%"
        query = query.filter(
            models.Plant.name.ilike(keyword)
            | models.Plant.scientific_name.ilike(keyword)
            | models.Plant.description.ilike(keyword)
        )

    if category:
        query = query.filter(models.Plant.category == category)

    plants = query.all()
    return [plant_to_dict(plant) for plant in plants]


@app.get("/api/plants/{plant_id}")
def get_plant(plant_id: int, db: Session = Depends(get_db)):
    plant = db.query(models.Plant).filter(models.Plant.id == plant_id).first()
    if plant is None:
        raise HTTPException(status_code=404, detail="植物不存在")
    return plant_to_dict(plant)


@app.post("/api/plants")
def create_plant(plant: PlantCreate, db: Session = Depends(get_db)):
    db_plant = models.Plant(**plant.model_dump())
    db.add(db_plant)
    db.commit()
    db.refresh(db_plant)
    return plant_to_dict(db_plant)


@app.post("/api/identify")
async def identify_plant(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    try:
        uploaded_image = image_features.load_image_from_bytes(contents)
        uploaded_feature = image_features.extract_features(uploaded_image)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="图片解析失败") from exc

    candidates = []
    for plant in db.query(models.Plant).all():
        if not plant.image_path:
            continue
        image_path = Path(plant.image_path)
        if not image_path.exists():
            continue

        try:
            db_image = image_features.load_image_from_path(str(image_path))
            db_feature = image_features.extract_features(db_image)
            score = image_features.cosine_similarity(uploaded_feature, db_feature)
            candidates.append(
                {
                    "plant": plant_to_dict(plant),
                    "score": score,
                }
            )
        except Exception:
            continue

    if not candidates:
        raise HTTPException(status_code=404, detail="数据库中暂无可匹配的植物图片")

    candidates.sort(key=lambda item: item["score"], reverse=True)
    return candidates[:5]
