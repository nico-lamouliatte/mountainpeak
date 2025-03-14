from sqlalchemy import Column, Integer, String, Float

from app.database import Base


class Peak(Base):
    __tablename__ = "peaks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    lat = Column(Float)
    lng = Column(Float)
    altitude = Column(Integer)
