from datetime import datetime
import json
import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from faker import Faker
from model.team_model import Team
from model.player_model import Player
from utils.logger import logger_config

log = logger_config(__name__)
faker = Faker()

current_directory = os.path.dirname(os.path.abspath(__file__))


async def insert_sample_data(session: AsyncSession, model, sample_data):
    result = await session.execute(select(model))
    records = result.scalars().all()
    if not records:
        session.add_all(sample_data)
        await session.commit()


async def insert_sample_teams(session: AsyncSession):
    with open(os.path.join(current_directory, "teams.json")) as f:
        sample_teams = json.load(f)
    for team in sample_teams:
        team["created_at"] = datetime.fromisoformat(team["created_at"])
    teams = [Team(**team) for team in sample_teams]
    await insert_sample_data(session, Team, teams)


async def insert_sample_players(session: AsyncSession):
    with open(os.path.join(current_directory, "players.json")) as f:
        sample_players = json.load(f)
    for player in sample_players:
        player["created_at"] = datetime.fromisoformat(player["created_at"])
    players = [Player(**player) for player in sample_players]
    await insert_sample_data(session, Player, players)
