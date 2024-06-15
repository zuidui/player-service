from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from data.session import Base


class Team(Base):
    __tablename__ = "teams"

    team_id = Column(Integer, primary_key=True, index=True)
    team_name = Column(String, index=True, unique=True)
    team_password = Column(String)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    players = relationship("Player", back_populates="team")

    def to_dict(self):
        return {
            "team_id": self.team_id,
            "team_name": self.team_name,
            "team_password": self.team_password,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
