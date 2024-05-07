from functools import lru_cache
from typing import Type

from pydantic import BaseModel, ConfigDict, create_model as create_model_base

class _SchemaConfig(ConfigDict):
    pass

@lru_cache(maxsize=256)
def _create_model_cached(
    __model_name: str,
    **field_definitions
) -> Type[BaseModel]:
    return create_model_base(
        __model_name,
        __config__=_SchemaConfig(extra='allow', arbitrary_types_allowed=True),
        **field_definitions
    )

def create_model(
    __model_name: str,
    **field_descriptions
) -> Type[BaseModel]:
    try:
        return _create_model_cached(__model_name, **field_descriptions)
    except TypeError:
        # something in field definitions is not hashable
        return create_model_base(
            __model_name,
            __config__=_SchemaConfig(extra='allow', arbitrary_types_allowed=True),
            **field_descriptions
        )