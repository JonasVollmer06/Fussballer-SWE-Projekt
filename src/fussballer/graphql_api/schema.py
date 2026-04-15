"""Schema für die GraphQL-Schnittstelle mit Strawberry statt SDL."""
from typing import Final

import strawberry
from fastapi import Request
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info

from fussballer.config.graphql import graphql_ide
from fussballer.graphql_api.graphql_types import (
    CreatePayload,
    FussballerInput,
    LoginPayload,
    SuchparameterInput,
)
from fussballer.repository import FussballerRepository
from fussballer.repository.pageable import Pageable
from fussballer.router.fussballer_model import FussballerModel
from fussballer.security import UserService
from fussballer.security.dependencies import _token_service
from fussballer.service import (
    FussballerDTO,
    FussballerService,
    FussballerWriteService,
    NotFoundError,
)

__all__ = ["graphql_router"]

_repo: Final = FussballerRepository()
_fussballer_service: FussballerService = FussballerService(repo=_repo)
_user_service: UserService = UserService()
_write_service: FussballerWriteService = FussballerWriteService(repo=_repo,
user_service=_user_service)


@strawberry.type
class Query:
    """Klasse zum Lesen der Fußballerdaten über Strawberry."""

    @strawberry.field
    def fussballer(
        self,
        fussballer_id: strawberry.ID,
        info: Info) -> FussballerDTO | None:
        """Methode zum lesen von Fussballerdaten anhand einer gegebenen Id.

        :return: Gesuchte Fussballerdaten
        """
        request: Final[Request] = info.context.get("request")
        user: Final = _token_service.get_user_from_request(request=request)
        if user is None:
            return None

        try:
            int_fussballer_id: Final = int(fussballer_id)
            fussballer_dto: Final = _fussballer_service.find_by_id(
                fussballer_id=int_fussballer_id, user=user)

        except NotFoundError:
            return None

        return fussballer_dto

    @strawberry.field
    def fussballer_liste(
        self, suchparameter: SuchparameterInput
    ) -> list[FussballerDTO]:
        """Methode zum Lesen mehrerer Fussballer anhand von Suchparametern."""
        suchparameter_dict = {
            key: value
            for key, value in suchparameter.__dict__.items()
            if value is not None
        }
        try:
            fussballer_slice: Final = _fussballer_service.find(
                suchparameter=suchparameter_dict,
                pageable=Pageable.create(),
            )
        except NotFoundError:
            return []

        return list(fussballer_slice.content)


@strawberry.type
class Mutation:
    """Mutations-Klasse zum manipulieren der Daten(schreiben)."""

    @strawberry.mutation
    def login(self, username: str, password: str) -> LoginPayload:
        """GraphQL-Methode zum Erstellen eines Tokens."""
        token = _token_service.token(username=username, password=password)
        return LoginPayload(token=token["access_token"])

    @strawberry.mutation
    def create(self, fussballer_input: FussballerInput) -> CreatePayload:
        """GraphQL-Methode zum Erstellen eines Fussballer-Objekts.

        :return: Generierte ID des erstellten Objekts.
        """
        fussballer_dict = fussballer_input.__dict__
        fussballer_dict["adresse"] = fussballer_input.adresse.__dict__
        fussballer_dict["auszeichnungen"] = [auszeichnung.__dict__ for auszeichnung in
            fussballer_input.auszeichnungen]

        fussballer_model: Final = FussballerModel.model_validate(fussballer_dict)

        fussballer_dto: Final = _write_service.create(
            fussballer=fussballer_model.to_fussballer()
        )
        payload: Final = CreatePayload(id=fussballer_dto.id)

        return payload


schema: Final = strawberry.Schema(query=Query, mutation=Mutation)

Context = dict[str, Request]


def get_context(request: Request) -> Context:
    return {"request": request}


graphql_router: Final = GraphQLRouter[Context](
    schema, context_getter=get_context, graphql_ide=graphql_ide
)
