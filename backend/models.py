from sqlalchemy import Column, Integer, String, Text

from database import Base


class Plant(Base):
    __tablename__ = "plants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    scientific_name = Column(String, nullable=True)
    category = Column(String, index=True, nullable=True)
    description = Column(Text, nullable=True)
    image_path = Column(String, nullable=True)
