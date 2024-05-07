from typing import Any, Type, cast, override

from jinja2 import Template, meta
from pydantic import Field

from funcstack.containers import Effect, Effects
from funcstack.mixins import PydanticMixin
from funcstack.modules import Module
from funcstack.typing._vars import Out

class JinjaConverter(PydanticMixin, Module[Any, Out]):
    template_str: str
    output_type: Type[Out] = Field(default=Any)

    @property
    @override
    def OutputType(self) -> Type[Out]:
        return self.output_type

    def __init__(
        self,
        template: str,
        output_type: Type[Out] = Any
    ):
        super().__init__(template_str=template, output_type=output_type)
        self.template = Template(template)
        ast = self.template.environment.parse(template)
        template_variables = meta.find_undeclared_variables(ast)
        self.context_variables = {v: (Any, None) for v in template_variables}

    def evaluate(self, context: Any, **kwargs) -> Effect[Out]:
        def _invoke() -> Out:
            return cast(Out, self.template.render(context))
        return Effects.Sync(_invoke)