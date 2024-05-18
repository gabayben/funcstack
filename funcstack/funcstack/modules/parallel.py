import asyncio
from typing import Any, Mapping, Type, override

from pydantic import BaseModel

from funcstack.containers import Effect, Effects
from funcstack.mixins import PydanticMixin
from funcstack.modules import Module, coerce_to_module
from funcstack.modules.base import ModuleLike, ModuleMapping
from funcstack.typing._vars import In
from funcstack.utils.formatting import indent_lines_after_first

class Parallel(PydanticMixin, Module[In, dict[str, Any]]):
    steps: Mapping[str, Module[In, Any]]

    @property
    @override
    def InputType(self) -> Type[In]:
        for step in self.steps.values():
            if step.InputType:
                return step.InputType
        return Any

    def __init__(self, **steps: ModuleLike[In, Any] | ModuleMapping[In]):
        super().__init__(
            steps={k: coerce_to_module(m) for k, m in steps.items()}
        )

    def __repr__(self) -> str:
        map_for_repr = ',\n '.join(
            f"{name}: {indent_lines_after_first(repr(mod), f'  {name}: ')}"
            for name, mod in self.steps.items()
        )
        return '{\n  ' + map_for_repr + '\n}'

    def __call__(self, data: In, **kwargs) -> Effect[dict[str, Any]]:
        async def _ainvoke() -> dict[str, Any]:
            try:
                steps = dict(self.steps)
                generators = await asyncio.gather(
                    *(
                        mod.ainvoke(data, **kwargs)
                        for mod in steps.values()
                    )
                )
                return {
                    k: v
                    for k, v in zip(steps, generators)
                }
            except:
                raise
        return Effects.Async(_ainvoke)

    @override
    def get_name(
        self,
        name: str | None = None,
        suffix: str | None = None
    ) -> str:
        name = name or self.name or f"Parallel<{', '.join(self.steps.keys())}>"
        return super().get_name(name=name, suffix=suffix)

    @override
    def input_schema(self) -> Type[BaseModel]:
        if all(
            mod.input_schema().model_json_schema().get('type', 'object') == 'object'
            for mod in self.steps.values()
        ):
            return create_model( # type: ignore[call-overload]
                self.get_name(suffix='Input'),
                **{
                    k: (v.annotation, v.default)
                    for mod in self.steps.values()
                    for k, v in mod.input_schema().model_fields.items()
                    if k != '__root__'
                }
            )
        return super().input_schema()

    @override
    def output_schema(self) -> Type[BaseModel]:
        return create_model( # type: ignore[call-overload]
            self.get_name(suffix='Output'),
            **{
                k: (step.OutputType, None)
                for k, step in self.steps.items()
            }
        )