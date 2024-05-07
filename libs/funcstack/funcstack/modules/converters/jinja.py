from typing import Any, Type, override

from pydantic import Field

from funcstack.containers import Effect
from funcstack.mixins import PydanticMixin
from funcstack.modules import Module
from funcstack.typing._vars import In, Out

class JinjaConverter(PydanticMixin, Module[In, Out]):
    template: str
    input_type: Type[In] = Field(default=Any)
    output_type: Type[Out] = Field(default=Any)

    @property
    @override
    def InputType(self) -> Type[In]:
        return self.input_type

    @property
    @override
    def OutputType(self) -> Type[Out]:
        return self.output_type

    def __init__(
        self,
        template: str,
        input_type: Type[In] = Any,
        output_type: Type[Out] = Any
    ):
        super().__init__(template=template, input_type=input_type, output_type=output_type)

    def evaluate(self, context: In, **kwargs) -> Effect[Out]:
        pass