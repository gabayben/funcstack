from typing import Any, Type, override

from pydantic import Field

from funcstack.containers import Effect
from funcstack.mixins import PydanticMixin
from funcstack.modules import Module
from funcstack.typing._vars import In

class PromptBuilder(PydanticMixin, Module[In, str]):
    template: str
    context_type: Type[In] = Field(default=Any)

    @property
    @override
    def InputType(self) -> Type[In]:
        return self.context_type

    def __init__(self, template: str, context_type: Type[In] = Any):
        super().__init__(template=template, context_type=context_type)

    def evaluate(self, data: In, **kwargs) -> Effect[str]:
        pass