# coding: utf-8

"""
    Universal Worker Service (UWS)

    The Universal Worker Service (UWS) pattern defines how to manage asynchronous execution of jobs on a service.

    The version of the OpenAPI document: 1.2
    Contact: grid@ivoa.net
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations

import json
import pprint
import re  # noqa: F401
from typing import Any, ClassVar, Optional

from openapi_server.models.api_base_model import APIBaseModel
from pydantic import Field, StrictBool, StrictStr, field_validator


class ErrorSummary(APIBaseModel):
    """
    A short summary of an error - a fuller representation of the error may be retrieved from /{jobs}/{job_id}/error
    """  # noqa: E501

    message: Optional[StrictStr] = Field(default=None, description="A short message describing the error ")
    has_detail: StrictBool = Field(alias="hasDetail")
    type: StrictStr = Field(description="characterization of the type of the error ")
    __properties: ClassVar[list[str]] = ["message", "hasDetail", "type"]

    @field_validator("type")
    @classmethod
    def type_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ("transient", "fatal"):
            raise ValueError("must be one of enum values ('transient', 'fatal')")
        return value
