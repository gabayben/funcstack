from typing import Any, Type, override

from pydantic import BaseModel

from funcstack.containers import Effect
from funcstack.mixins import PydanticMixin
from funcstack.modules import Module
from funcstack.typing._vars import Out
from funcstack.utils.serialization import create_model

class JinjaConverter(PydanticMixin, Module[dict[str, Any], Out]):
    def __init__(
        self,
        template: str,
        **runtime_variables
    ):
        self.template = template
        self.runtime_variables = runtime_variables

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