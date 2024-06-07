from typing import Any, Dict, Optional
import httpx

from datetime import datetime, timezone

from model.player_model import Player
from model.team_model import Team

from resolver.player_schema import PlayerType, PlayerInput
from resolver.team_schema import TeamType, TeamInput

from repository.team_repository import TeamRepository
from repository.player_repository import PlayerRepository

from events.publisher import publish_event, Publisher

from utils.logger import logger_config
from utils.config import get_settings
from utils.converters import (
    convert_player_to_playertype,
    convert_team_to_teamtype,
)

log = logger_config(__name__)
settings = get_settings()


class TeamService:
    @staticmethod
    async def handle_message(message: dict):
        log.info(f"Handling message: {message}")
        event_type = message["event_type"]
        data = message["data"]
        if event_type == "createTeam":
            mutation = f"""
            mutation {{
                createTeam(teamId: "{data['teamId']}", teamName: "{data['teamName']}") {{
                    teamId
                    teamName
                }}
            }}
            """
        elif event_type == "createPlayer":
            mutation = f"""
            mutation {{
                createPlayer(playerId: "{data['playerId']}", playerName: "{data['playerName']}") {{
                    playerId
                    playerName
                }}
            }}
            """
        payload = {"query": mutation}
        return await TeamService.send_to_api_gateway(payload)

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
    async def create_team(team_data: TeamInput, publisher: Publisher) -> TeamType:
        log.info(f"Creating team: {team_data}")

        new_team = Team(
            team_name=team_data.teamName,
            team_password=team_data.teamPassword,
            created_at=datetime.now(timezone.utc),
        )

        team_created = convert_team_to_teamtype(await TeamRepository.create(new_team))

        log.info(f"Team created in service: {team_created.__dict__}")

        await publish_event(publisher, "createTeam", team_created.__dict__)

        return team_created

    @staticmethod
    async def get_team_by_name(team_name: str) -> TeamType:
        log.info(f"Getting team by name: {team_name}")

        team = await TeamRepository.get_by_name(team_name)

        log.info(f"Team found: {team}")

        return convert_team_to_teamtype(team)

    @staticmethod
    async def create_player(
        player_data: PlayerInput, publisher: Publisher
    ) -> PlayerType:
        log.info(f"Creating player: {player_data}")

        player = Player(
            team_id=player_data.teamId,
            player_name=player_data.playerName,
            created_at=datetime.now(timezone.utc),
        )

        player_created = await PlayerRepository.create(player)
        log.info(f"Player created: {player_created.to_dict()}")

        await publish_event(publisher, "createPlayer", player_created.to_dict())

        return convert_player_to_playertype(player_created)

    @staticmethod
    async def get_player_by_name(player_name: str) -> PlayerType:
        log.info(f"Getting player by name: {player_name}")

        player = await PlayerRepository.get_by_name(player_name)

        log.info(f"Player found: {player}")

        return convert_player_to_playertype(player)
