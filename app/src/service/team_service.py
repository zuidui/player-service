from datetime import datetime, timezone

from model.player_model import Player
from model.team_model import Team

from resolver.player_schema import PlayerType, PlayerInput
from resolver.team_schema import TeamType, TeamInput

from repository.team_repository import TeamRepository
from repository.player_repository import PlayerRepository

from events.publisher import publish_event, Publisher

from utils.logger import logger_config
from utils.converters import convert_player_to_playertype, convert_team_to_teamtype

log = logger_config(__name__)


class TeamService:
    @staticmethod
    async def create_team(team_data: TeamInput, publisher: Publisher) -> TeamType:
        log.info(f"Creating team: {team_data}")

        new_team = Team(
            team_name=team_data.teamName,
            team_password=team_data.teamPassword,
            created_at=datetime.now(timezone.utc),
        )

        team_created = await TeamRepository.create(new_team)

        log.info(f"Team created in service: {team_created.to_dict()}")

        await publish_event(publisher, "createTeam", team_created.to_dict())

        return convert_team_to_teamtype(team_created)

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
