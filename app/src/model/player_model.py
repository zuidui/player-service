from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from data.session import Base


class Player(Base):
    __tablename__ = "players"

    player_id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.team_id"))
    player_name = Column(String, index=True)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    team = relationship("Team", back_populates="players")

    def to_dict(self):
        return {
            "player_id": self.player_id,
            "team_id": self.team_id,
            "player_name": self.player_name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
