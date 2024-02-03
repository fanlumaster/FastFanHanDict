from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class TaiwanChineseDict(Base):
    __tablename__ = "taiwan_chinese_dict"

    id = Column(Integer, primary_key=True)
