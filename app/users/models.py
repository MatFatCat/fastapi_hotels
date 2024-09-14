from app.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    token_refresh = Column(String, nullable=True)

    booking = relationship("Bookings", back_populates="user")

    def __str__(self):
        return f"User {self.name} ({self.email})"
