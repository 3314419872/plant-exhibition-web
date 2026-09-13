from database import Base, SessionLocal, engine
import models


Base.metadata.create_all(bind=engine)

sample_plants = [
    {
        "name": "绿萝",
        "scientific_name": "Epipremnum aureum",
        "category": "观叶植物",
        "description": "常见室内观叶植物，耐阴性强，适合水培或土培。",
    },
    {
        "name": "吊兰",
        "scientific_name": "Chlorophytum comosum",
        "category": "观叶植物",
        "description": "叶片细长，适应性强，常用于室内净化空气。",
    },
    {
        "name": "仙人掌",
        "scientific_name": "Opuntia dillenii",
        "category": "多肉植物",
        "description": "耐旱植物，茎干肉质，适合阳光充足的环境。",
    },
    {
        "name": "常春藤",
        "scientific_name": "Hedera nepalensis",
        "category": "攀援植物",
        "description": "攀援植物，可用于垂直绿化。",
    },
    {
        "name": "龟背竹",
        "scientific_name": "Monstera deliciosa",
        "category": "观叶植物",
        "description": "叶片具有独特裂纹，是常见室内大型观叶植物。",
    },
]


def seed():
    db = SessionLocal()
    try:
        if db.query(models.Plant).count() == 0:
            for item in sample_plants:
                db.add(models.Plant(**item))
            db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
