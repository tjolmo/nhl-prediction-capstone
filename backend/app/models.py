from .database import Base
from sqlalchemy.orm import Mapped, mapped_column

class Team(Base):
    __tablename__ = "teams"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    franchise_id: Mapped[int] = mapped_column(nullable=False)
    tri_code: Mapped[str] = mapped_column(nullable=False)