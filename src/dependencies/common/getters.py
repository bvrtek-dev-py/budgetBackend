from fastapi import Request, HTTPException

from backend.src.dependencies.common.enums import IdentifierSource


def get_id_from_url_path(request: Request, name: str) -> int:
    value = request.path_params.get(name)

    if value is None:
        raise HTTPException(status_code=400, detail="Path argument not found")

    return int(value)


async def get_id_from_request(request: Request, name: str) -> int:
    json_data = await request.json()
    value = json_data[name]

    if value is None:
        raise HTTPException(status_code=400, detail="Request argument not found")

    return int(value)


async def get_object_id(scope: IdentifierSource, request: Request, name: str) -> int:
    if scope == IdentifierSource.PATH_PARAMETER:
        return get_id_from_url_path(request, name)

    return await get_id_from_request(request, name)
