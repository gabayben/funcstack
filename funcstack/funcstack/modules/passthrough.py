from typing import Type, override

from pydantic import Field

from funcstack.containers import Effect
from funcstack.mixins import PydanticMixin
from funcstack.modules import Module
from funcstack.typing._vars import In

class Passthrough(PydanticMixin, Module[In, In]):
    passthrough_type: Type[In] = Field(default=None)

    @property
    @override
    def InputType(self) -> Type[In]:
        return self.passthrough_type

    @property
    @override
    def OutputType(self) -> Type[In]:
        return self.passthrough_type

    def __init__(self, passthrough_type: Type[In]):
        super().__init__()
        self.passthrough_type = passthrough_type

    def forward(self, data: In, **kwargs) -> Effect[In]:
        pass