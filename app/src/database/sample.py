from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from model.team_model import Team
from model.player_model import Player


async def insert_sample_data(session: AsyncSession, model, sample_data):
    result = await session.execute(select(model))
    records = result.scalars().all()

    if not records:
        session.add_all(sample_data)
        await session.commit()


async def insert_sample_teams(session: AsyncSession):
    now = datetime.now(timezone.utc)
    sample_teams = [
        Team(team_name="Team1", team_password="team1pass", created_at=now),
        Team(team_name="Team2", team_password="team2pass", created_at=now),
        Team(team_name="Team3", team_password="team3pass", created_at=now),
    ]
    await insert_sample_data(session, Team, sample_teams)


async def insert_sample_players(session: AsyncSession):
    now = datetime.now(timezone.utc)
    sample_players = [
        Player(
            team_id=1,
            player_name="Player1",
            created_at=now,
        ),
        Player(
            team_id=1,
            player_name="Player2",
            created_at=now,
        ),
        Player(
            team_id=2,
            player_name="Player3",
            created_at=now,
        ),
    ]
    await insert_sample_data(session, Player, sample_players)
