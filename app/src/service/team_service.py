from typing import Any, Dict, Optional
import httpx

from datetime import datetime, timezone

from models.team_model import Team
from models.player_model import Player

from resolver.team_schema import (
    TeamDataInput,
    TeamDataType,
)
from resolver.player_schema import (
    PlayerDataInput,
    PlayerDataOutput,
    PlayerDataType,
    PlayerDataListType,
)

from repository.team_repository import TeamRepository
from repository.player_repository import PlayerRepository

from events.publisher import publish_event, Publisher

from utils.logger import logger_config
from utils.config import get_settings

log = logger_config(__name__)
settings = get_settings()


class TeamService:
    @staticmethod
    async def send_to_api_gateway(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            log.debug(
                f"Sending request to {settings.API_GATEWAY_URL} with payload: {payload}"
            )
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.API_GATEWAY_URL}", json=payload
                )
                response.raise_for_status()
                log.debug(f"Response received: {response.json()}")
                return response.json().get("data")
        except httpx.HTTPStatusError as e:
            log.error(
                f"Request failed with status {e.response.status_code}: {e.response.text}"
            )
        except httpx.RequestError as e:
            log.error(f"An error occurred while requesting {e.request.url!r}.")
        except Exception as e:
            log.error(f"Unexpected error: {e}")
        return None

    @staticmethod
    async def team_exists_by_name(team_name: str) -> bool:
        return await TeamRepository.team_exists_by_name(team_name)

    @staticmethod
    async def player_exists_by_name_in_team(player_name: str, team_id: int) -> bool:
        return await PlayerRepository.player_exists_by_name_in_team(
            player_name, team_id
        )

    @staticmethod
    async def authenticate_team(team_data: TeamDataInput) -> Optional[TeamDataType]:
        team = await TeamRepository.get_by_name(team_data.team_name)
        if not team:
            raise ValueError("Team does not exist")
        team_dict = team.to_dict()
        if team_dict["team_password"] != team_data.team_password:
            raise ValueError("Invalid password")
        return TeamDataType(
            team_id=team_dict["team_id"],
            team_name=team_dict["team_name"],
        )

    @staticmethod
    async def create_team(
        team_data: TeamDataInput, publisher: Publisher
    ) -> TeamDataType:
        log.info(f"Creating team: {team_data}")

        if await TeamService.team_exists_by_name(team_data.team_name):
            raise ValueError(f"Team with name {team_data.team_name} already exists")

        new_team = Team(
            team_name=team_data.team_name,
            team_password=team_data.team_password,
            created_at=datetime.now(timezone.utc),
        )

        try:
            team = (await TeamRepository.create(new_team)).to_dict()
            team_created = TeamDataType(
                team_id=team["team_id"],
                team_name=team["team_name"],
            )

            await publish_event(
                publisher,
                "team_created",
                {"team_id": team_created.team_id, "team_name": team_created.team_name},
            )
            return team_created
        except Exception as e:
            log.error(f"Error creating team: {e}")
            raise e

    @staticmethod
    async def create_player(
        player_data: PlayerDataInput, publisher: Publisher
    ) -> Optional[PlayerDataType]:
        log.info(f"Creating player: {player_data}")

        team = await TeamRepository.get_by_name(player_data.team_name)

        if not team:
            raise ValueError(f"Team with name {player_data.team_name} does not exist")

        team_dict = team.to_dict()
        team_id = team_dict["team_id"]
        if await TeamService.player_exists_by_name_in_team(
            player_data.player_name, team_id
        ):
            raise ValueError(
                f"Player with name {player_data.player_name} already exists in team {player_data.team_name}"
            )

        new_player = Player(
            player_name=player_data.player_name,
            team_id=team_id,
            created_at=datetime.now(timezone.utc),
        )

        try:
            player = (await PlayerRepository.create(new_player)).to_dict()
            player_created = PlayerDataType(
                player_id=player["player_id"],
                team_id=player["team_id"],
                player_name=player["player_name"],
            )

            await publish_event(
                publisher,
                "player_created",
                {
                    "player_id": player_created.player_id,
                    "player_name": player_created.player_name,
                    "team_id": player_created.team_id,
                },
            )
            return player_created
        except Exception as e:
            log.error(f"Error creating player: {e}")
            raise e

    @staticmethod
    async def join_team(
        team_data: TeamDataInput, publisher: Publisher
    ) -> Optional[TeamDataType]:
        log.info(f"Joining team: {team_data}")
        try:
            team = await TeamService.authenticate_team(team_data)
            if not team:
                raise ValueError("Invalid team name or password")
            await publish_event(
                publisher,
                "team_joined",
                {"team_id": team.team_id, "team_name": team.team_name},
            )
            return team
        except Exception as e:
            log.error(
                f"Error joining team: {e} - Team does not exist or invalid password"
            )
            raise e

    @staticmethod
    async def get_players(team_name: str) -> Optional[PlayerDataListType]:
        log.info(f"Getting players for team {team_name}")
        team = await TeamRepository.get_by_name(team_name)
        if not team:
            raise ValueError(f"Team with name {team_name} does not exist")
        team_dict = team.to_dict()
        team_id = team_dict["team_id"]
        players = await PlayerRepository.get_players(team_id)
        players_dict = [player.to_dict() for player in players]
        if players:
            players_data_output = [
                PlayerDataOutput(
                    player_id=player["player_id"],
                    player_name=player["player_name"],
                )
                for player in players_dict
            ]
            return PlayerDataListType(
                team_id=team_id,
                team_name=team_name,
                players_data=players_data_output,
            )
        raise ValueError(f"No players found for team {team_name}")
