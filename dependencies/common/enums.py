from enum import StrEnum


class IdentifierSource(StrEnum):
    REQUEST_BODY = "request_body"
    PATH_PARAMETER = "path_parameter"
