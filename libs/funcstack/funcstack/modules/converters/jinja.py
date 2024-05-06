from typing import Any, Type, override

from pydantic import BaseModel, Field

from funcstack.containers import Effect
from funcstack.mixins import PydanticMixin
from funcstack.modules import Module
from funcstack.typing._vars import Out
from funcstack.utils.serialization import create_model

class JinjaConverter(PydanticMixin, Module[dict[str, Any], Out]):
    template: str
    output_type: Type[Out] = Field(default=Any)
    runtime_variables: dict[str, Any]

    @property
    @override
    def OutputType(self) -> Type[Out]:
        return self.output_type

    def __init__(
        self,
        template: str,
        output_type: Type[Out],
        **runtime_variables
    ):
        super().__init__(template=template, runtime_variables=runtime_variables)
        self.output_type = output_type

    def evaluate(self, context: dict[str, Any], **kwargs) -> Effect[Out]:
        pass

    @override
    def input_schema(self) -> Type[BaseModel]:
        return create_model(
            self.get_name(suffix='Input'),
            **{
                k: (v, None)
                for k, v in self.runtime_variables.items()
            }
        )