import logging
from typing import Type, override

from pydantic import BaseModel

from funcstack.containers import Effect, Effects
from funcstack.mixins import PydanticMixin
from funcstack.modules import Module
from funcstack.modules.traits import HasSequentialSchema
from funcstack.typing import SupportsKeyIndex
from funcstack.typing._vars import Out

logger = logging.getLogger(__name__)

class Pick(PydanticMixin, Module[SupportsKeyIndex, Out], HasSequentialSchema):
    key: str

    def __init__(self, key: str, **kwargs):
        super().__init__(**kwargs, key=key)

    def evaluate(self, data: SupportsKeyIndex, **kwargs) -> Effect[Out]:
        def _pick() -> Out:
            try:
                picked = data[self.key]
                if not isinstance(picked, self.OutputType):
                    raise TypeError(f'Incompatible types. {self.key}: {type(picked)}, expected: {self.OutputType}.')
            except (AttributeError, KeyError) as e:
                raise KeyError(f'Key {self.key} not found in data.') from e
            else:
                return picked
        return Effects.Sync(_pick)

    @override
    def get_name(
        self,
        name: str | None = None,
        suffix: str | None = None
    ) -> str:
        name = (
            name
            or self.name
            or f'Pick<{self.OutputType}>({self.key})'
        )
        return super().get_name(name=name, suffix=suffix)

    def seq_input_schema(self, next_schema: Type[BaseModel]) -> Type[BaseModel]:
        return next_schema

    def seq_output_schema(self, prev_schema: Type[BaseModel]) -> Type[BaseModel]:
        return self.output_schema()