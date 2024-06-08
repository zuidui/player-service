from typing import Any, Dict, Optional
import httpx

from datetime import datetime, timezone

from model.team_model import Team

from resolver.team_schema import TeamCreateRequest, TeamCreateResponse

from repository.team_repository import TeamRepository

from events.publisher import publish_event, Publisher

from utils.logger import logger_config
from utils.config import get_settings

log = logger_config(__name__)
settings = get_settings()


class TeamService:
    @staticmethod
    async def handle_message(message: dict):
        log.info(f"Handling message: {message}")
        event_type = message["event_type"]
        data = message["data"]
        if event_type == "create_team":
            team_name = data["team_name"]
            team_id = data["team_id"]
            mutation = f"""
            mutation {{
                create_team(new_team: {{ 
                    team_name: "{team_name}"
                    team_id: "{team_id}"
                }}) {{
                    team_id
                    team_name
                }}
            }}
            """
        payload = {"query": mutation}
        log.debug(f"Sending GraphQL mutation: {payload['query']}")
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
    async def create_team(
        team_data: TeamCreateRequest, publisher: Publisher
    ) -> TeamCreateResponse:
        log.info(f"Creating team: {team_data}")

        if await TeamService.team_exists_by_name(team_data.team_name):
            raise ValueError(f"Team with name {team_data.team_name} already exists")

        new_team = Team(
            team_name=team_data.team_name,
            team_password=team_data.team_password,
            created_at=datetime.now(timezone.utc),
        )

        team = (await TeamRepository.create(new_team)).to_dict()

        team_created = TeamCreateResponse(
            team_id=team["team_id"],
            team_name=team["team_name"],
        )

        log.info(f"Team created in service: {team_created}")
        log.debug(
            f"Publishing event: create_team with data: {{'team_id': {team_created.team_id}, 'team_name': {team_created.team_name}}}"
        )
        await publish_event(
            publisher,
            "create_team",
            {"team_id": team_created.team_id, "team_name": team_created.team_name},
        )

        return team_created

    @staticmethod
    async def team_exists_by_name(team_name: str) -> bool:
        return await TeamRepository.team_exists_by_name(team_name)
