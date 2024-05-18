from typing import Iterator, Sequence, Type, override

from funcstack.containers import Effect, Effects
from funcstack.modules import DecoratorBase, Module
from funcstack.typing._vars import In, Out

class Fallbacks(DecoratorBase[In, Out]):
    fallbacks: Sequence[Module[In, Out]]
    exceptions_to_handle: tuple[Type[BaseException], ...]

    @property
    def _modules(self) -> Iterator[Module[In, Out]]:
        yield self.bound
        yield from self.fallbacks

    def __init__(
        self,
        bound: Module[In, Out],
        fallbacks: Sequence[Module[In, Out]],
        exceptions_to_handle: tuple[Type[BaseException], ...] | None = None
    ):
        super().__init__(
            bound=bound,
            fallbacks=fallbacks,
            exceptions_to_handle = exceptions_to_handle or (Exception,)
        )

    @override
    def __call__(self, data: In, **kwargs) -> Effect[Out]:
        async def _ainvoke() -> Out:
            first_error: BaseException | None = None
            last_error: BaseException | None = None

            for mod in self._modules:
                try:
                    output = await mod.ainvoke(
                        data,
                        first_error=first_error,
                        last_error=last_error,
                        **kwargs
                    )
                except self.exceptions_to_handle as e:
                    first_error = first_error or e
                    last_error = e
                except BaseException as e:
                    raise e
                else:
                    return output

            if first_error is None:
                raise ValueError('No error stored at end of fallbacks.')
            raise first_error

        return Effects.Async(_ainvoke)