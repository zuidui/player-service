from typing import Any, Dict, Optional
import httpx

from datetime import datetime, timezone

from model.team_model import Team
from model.player_model import Player

from resolver.team_schema import TeamCreateType, TeamCreateInput, TeamDataInput, TeamDataType
from resolver.player_schema import PlayerCreateType, PlayerCreateInput

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
    async def handle_message(message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        event_type = message["event_type"]
        data = message["data"]
        if event_type == "create_team":
            team_name = data["team_name"]
            team_id = data["team_id"]
            mutation = f"""
            mutation {{
                team_created(new_team: {{ 
                    team_name: "{team_name}"
                    team_id: "{team_id}"
                }}) {{
                    team_id
                    team_name
                }}
            }}
            """
            payload = {"query": mutation}
        elif event_type == "create_player":
            player_name = data["player_name"]
            player_team_id = data["player_team_id"]
            mutation = f"""
            mutation {{
                player_created(new_player: {{ 
                    player_name: "{player_name}"
                    player_team_id: {player_team_id}
                }}) {{
                    player_name
                    player_team_name
                    player_team_id
                }}
            }}
            """
            payload = {"query": mutation}
        elif event_type == "join_team":
            team_name = data["team_name"]
            team_id = data["team_id"]
            mutation = f"""
            mutation {{
                team_joined(team_data: {{ 
                    team_name: "{team_name}"
                    team_id: {team_id}
                }}) {{
                    team_id
                    team_name
                }}
            }}
            """
            payload = {"query": mutation}
        else:
            log.info(f"Event type {event_type} consumed but not handled.")
            return data
        log.debug(f"Sending GraphQL mutation: {payload['query']}")
        return await TeamService.send_to_api_gateway(payload)

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
        if team and team.team_password == team_data.team_password:
            return TeamDataType(
                team_id=team.team_id,
                team_name=team.team_name,
            )
        raise ValueError("Invalid team name or password")

    @staticmethod
    async def create_team(
        team_data: TeamCreateInput, publisher: Publisher
    ) -> TeamCreateType:
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
            team_created = TeamCreateType(
                team_id=team["team_id"],
                team_name=team["team_name"],
            )

            await publish_event(
                publisher,
                "create_team",
                {"team_id": team_created.team_id, "team_name": team_created.team_name},
            )
            return team_created
        except Exception as e:
            log.error(f"Error creating team: {e}")
            raise e

    @staticmethod
    async def create_player(
        player_data: PlayerCreateInput, publisher: Publisher
    ) -> Optional[PlayerCreateType]:
        log.info(f"Creating player: {player_data}")

        if await TeamService.player_exists_by_name_in_team(
            player_data.player_name, player_data.player_team_id
        ):
            raise ValueError(
                f"Player with name {player_data.player_name} already exists in team {player_data.player_team_id}"
            )

        new_player = Player(
            player_name=player_data.player_name,
            team_id=player_data.player_team_id,
            created_at=datetime.now(timezone.utc),
        )

        try:
            player = (await PlayerRepository.create(new_player)).to_dict()
            player_created = PlayerCreateType(
                player_id=player["player_id"],
                player_team_id=player["team_id"],
                player_name=player["player_name"],
            )

            await publish_event(
                publisher,
                "create_player",
                {
                    "player_id": player_created.player_id,
                    "player_team_id": player_created.player_team_id,
                    "player_name": player_created.player_name,
                },
            )
            return player_created
        except Exception as e:
            log.error(f"Error creating player: {e}")
            raise e
        
    @staticmethod
    async def join_team(
        team_data: TeamDataInput,
        publisher: Publisher
    ) -> Optional[TeamDataType]:
        log.info(f"Joining team: {team_data}")
        try:
            team = await TeamService.authenticate_team(team_data)
            await publish_event(
                publisher,
                "join_team",
                {"team_id": team.team_id, "team_name": team.team_name},
            )
            return team
        except Exception as e:
            log.error(f"Error joining team: {e} - Team does not exist or invalid password")
            raise e
