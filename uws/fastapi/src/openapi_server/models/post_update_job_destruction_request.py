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
from datetime import datetime
from typing import Any, ClassVar, Optional

from pydantic import BaseModel, Field


class PostUpdateJobDestructionRequest(BaseModel):
    """
    PostUpdateJobDestructionRequest
    """ # noqa: E501
    destruction: Optional[datetime] = Field(default=None, alias="DESTRUCTION")
    __properties: ClassVar[list[str]] = ["DESTRUCTION"]

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
    }


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> PostUpdateJobDestructionRequest:
        """Create an instance of PostUpdateJobDestructionRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        _dict = self.model_dump(
            by_alias=True,
            exclude={
            },
            exclude_none=True,
        )
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PostUpdateJobDestructionRequest:
        """Create an instance of PostUpdateJobDestructionRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "DESTRUCTION": obj.get("DESTRUCTION")
        })
        return _obj


