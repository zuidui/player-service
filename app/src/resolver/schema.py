from strawberry import Schema


from resolver.team_query import TeamQuery
from resolver.player_query import PlayerQuery
from resolver.team_mutation import TeamMutation
from resolver.player_mutation import PlayerMutation


class Query(TeamQuery, PlayerQuery):
    pass


class Mutation(TeamMutation, PlayerMutation):
    pass


schema = Schema(query=TeamQuery, mutation=TeamMutation)
