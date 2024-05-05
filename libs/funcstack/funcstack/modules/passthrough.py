from typing import Type, override

from pydantic import Field

from funcstack.containers import Effect
from funcstack.mixins import PydanticMixin
from funcstack.modules import Module
from funcstack.typing._vars import In, Other, Out

class Passthrough(PydanticMixin, Module[Other, Other]):
    type_: Type[Other] = Field(exclude=True)

    @property
    @override
    def InputType(self) -> Type[In]:
        return self.type_

    @property
    @override
    def OutputType(self) -> Type[Out]:
        return self.type_

    def __init__(self, type_: Type[Other]):
        super().__init__()
        self.type_ = type_

    def evaluate(self, data: Other, **kwargs) -> Effect[Other]:
        pass