import inspect
from typing import Any, Callable, Type

from funcstack.utils.serialization import create_model
from overrides.typing_utils import get_type_hints, issubtype
from pydantic import BaseModel, TypeAdapter

def is_typed_dict(type_: Type) -> bool:
    return type_.__class__.__name__ == '_TypedDictMeta'

def from_typed_dict(type_: Type, name: str) -> Type[BaseModel]:
    fields: dict[str, Any] = {}
    for key, item in TypeAdapter(type_).core_schema['fields'].items():
        fields[key] = (item['schema']['type'], None)
    return create_model(name, **fields)

def create_pydantic_model(type_: Type, name: str, single_field_name: str):
    if inspect.isclass(type_) and issubclass(type_, BaseModel):
        return type_
    elif is_typed_dict(type_):
        return from_typed_dict(type_, name)
    return create_model(name, **{single_field_name: (type_, None)})

def get_return_type[R](func: Callable[..., R]) -> Type[R]:
    return get_type_hints(func)['return']

def is_return_type[R, T](func: Callable[..., R], type_: Type[T]) -> bool:
    return issubtype(get_return_type(func), type_)