from strawberry import Schema

from resolver.query import Query
from resolver.mutation import Mutation


schema = Schema(query=Query, mutation=Mutation)
