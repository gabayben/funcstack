from typing import Any, Type, override

from funcstack.utils.serialization import create_model
from jinja2 import Template, meta
from pydantic import BaseModel

from funcstack.containers import Effect, Effects
from funcstack.mixins import PydanticMixin
from funcstack.modules import Module

class PromptBuilder(PydanticMixin, Module[dict[str, Any], str]):
    template_str: str
    required_variables: list[str]

    def __init__(self, template: str, required_variables: list[str] | None = None):
        super().__init__(template_str=template, required_variables = required_variables or [])
        self.template = Template(template)
        ast = self.template.environment.parse(template)
        template_variables = meta.find_undeclared_variables(ast)
        self.context_variables = {v: (Any, None) for v in template_variables}

    def __call__(self, data: dict[str, Any], **kwargs) -> Effect[str]:
        def _invoke() -> str:
            missing_variables = [var for var in self.required_variables if var not in data]
            if missing_variables:
                raise ValueError(f'Missing required input variables in PromptBuilder: {', '.join(missing_variables)}.')
            return self.template.render(data)
        return Effects.Sync(_invoke)

    @override
    def input_schema(self) -> Type[BaseModel]:
        return create_model(self.get_name(name='Input'), **self.context_variables)