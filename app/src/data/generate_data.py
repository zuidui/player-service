import json
from datetime import datetime, timezone
from faker import Faker

faker = Faker()


def generate_team_player_data():
    now = datetime.now(timezone.utc)
    teams = []
    players = []
    player_id_counter = 1

    for team_num in range(1, 5):  # 4 teams
        team = {
            "team_name": f"Team{team_num}",
            "team_password": f"team{team_num}pass",
            "created_at": now.isoformat(),
        }
        teams.append(team)

        for _ in range(5):  # 5 players per team
            player = {
                "team_id": team_num,  # team_num matches the team_id to simulate relationships
                "player_name": faker.name(),
                "created_at": now.isoformat(),
            }
            players.append(player)
            player_id_counter += 1

    with open("teams.json", "w") as f:
        json.dump(teams, f, indent=4)

    with open("players.json", "w") as f:
        json.dump(players, f, indent=4)


if __name__ == "__main__":
    generate_team_player_data()
