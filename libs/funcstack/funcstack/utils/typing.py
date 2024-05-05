from typing import Callable, Type

from overrides.typing_utils import get_type_hints, issubtype

def get_return_type[R](func: Callable[..., R]) -> Type[R]:
    return get_type_hints(func)['return']

def is_return_type[R, T](func: Callable[..., R], type_: Type[T]) -> bool:
    return issubtype(get_return_type(func), type_)