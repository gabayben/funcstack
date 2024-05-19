from abc import ABC, abstractmethod
import asyncio
import inspect
from typing import Any, AsyncIterator, Callable, Coroutine, Generic, Iterator, Mapping, Sequence, Type, Union, cast, final, get_args

from pydantic import BaseModel

from funcstack.containers import Effect, Effects
from funcstack.typing import AfterRetryFailure, RetryStrategy, StopStrategy, WaitStrategy
from funcstack.typing._vars import Args, In, Other, Out
from funcstack.utils.typing import create_pydantic_model, is_return_type

class Module(Generic[In, Out], ABC):
    name: str | None = None

    @property
    def InputType(self) -> Type[In]:
        """
        The type of input this module accepts specified as a type annotation.
        """
        for cls in self.__class__.__orig_bases__: # type: ignore[attr-defined]
            type_args = get_args(cls)
            if type_args and len(type_args) == 2:
                return type_args[0]
        raise TypeError(
            f"Module {self.get_name()} doesn't have an inferrable InputType."
            'Override the InputType property to specify the input type.'
        )

    @property
    def OutputType(self) -> Type[Out]:
        """
        The type of output this module accepts specified as a type annotation.
        """
        for cls in self.__class__.__orig_bases__:  # type: ignore[attr-defined]
            type_args = get_args(cls)
            if type_args and len(type_args) == 2:
                return type_args[1]
        raise TypeError(
            f"Module {self.get_name()} doesn't have an inferrable OutputType."
            'Override the OutputType property to specify the output type.'
        )

    def __or__(
        self,
        other: Union['ModuleLike[Out, Other]', 'ModuleMapping[Out]']
    ) -> 'Module[In, Other]':
        from funcstack.modules.sequential import Sequential
        return Sequential(self, coerce_to_module(other))

    def __ror__(self, other: 'ModuleLike[Other, In]') -> 'Module[Other, Out]':
        from funcstack.modules.sequential import Sequential
        return Sequential(coerce_to_module(other), self)

    def bind(self, **kwargs) -> 'Module[In, Out]':
        from funcstack.modules.decorator import Decorator
        return Decorator(bound=self, kwargs=kwargs)

    def with_types(
        self,
        custom_input_type: Type[In] | BaseModel | None = None,
        custom_output_type: Type[Out] | BaseModel | None = None
    ) -> 'Module[In, Out]':
        from funcstack.modules.decorator import Decorator
        return Decorator(
            bound=self,
            custom_input_type=custom_input_type,
            custom_output_type=custom_output_type,
            kwargs={}
        )

    def with_retry(
        self,
        retry: RetryStrategy | None = None,
        stop: StopStrategy | None = None,
        wait: WaitStrategy | None = None,
        after: AfterRetryFailure | None = None
    ) -> 'Module[In, Out]':
        from funcstack.modules.fault_handling.retry import Retry
        return Retry(
            bound=self,
            retry=retry,
            stop=stop,
            wait=wait,
            after=after
        )

    def with_fallbacks(
        self,
        fallbacks: Sequence['Module[In, Out]'],
        exceptions_to_handle: tuple[BaseException, ...] | None = None
    ) -> 'Module[In, Out]':
        from funcstack.modules.fault_handling.fallbacks import Fallbacks
        return Fallbacks(
            bound=self,
            fallbacks=fallbacks,
            exceptions_to_handle=exceptions_to_handle
        )

    @abstractmethod
    def effect(self, data: In, **kwargs) -> Effect[Out]:
        pass

    @final
    def invoke(self, data: In, **kwargs) -> Out:
        return self(data, **kwargs).invoke()

    @final
    async def ainvoke(self, data: In, **kwargs) -> Out:
        return await self(data, **kwargs).ainvoke()

    @final
    def iter(self, data: In, **kwargs) -> Iterator[Out]:
        yield from self(data, **kwargs).iter()

    @final
    async def aiter(self, data: In, **kwargs) -> AsyncIterator[Out]:
        async for item in self(data, **kwargs).aiter(): #type: ignore
            yield item

    def get_name(
        self,
        name: str | None = None,
        suffix: str | None = None
    ) -> str:
        """
        Get the name of the module.
        """
        name = name or self.name or self.__class__.__name__
        if suffix:
            if name[0].isupper():
                return name + suffix.title()
            else:
                return name + '_' + suffix.lower()
        else:
            return name

    def input_schema(self) -> Type[BaseModel]:
        """
        Get a pydantic model that can be used to validate input to the module.

        Modules that leverage the configurable_fields and configurable_alternatives
        methods will have a dynamic input schema that depends on which
        configuration the module is invoked with.

        This method allows to get an input schema for a specific configuration.

        Returns:
            A pydantic model that can be used to validate input.
        """
        return create_pydantic_model(self.InputType, self.get_name(name='Input'), 'input')

    def output_schema(self) -> Type[BaseModel]:
        """
        Get a pydantic model that can be used to validate output to the module.

        Modules that leverage the configurable_fields and configurable_alternatives
        methods will have a dynamic output schema that depends on which
        configuration the module is invoked with.

        This method allows to get an output schema for a specific configuration.

        Returns:
            A pydantic model that can be used to validate output.
        """
        return create_pydantic_model(self.OutputType, self.get_name(name='Output'), 'output')

class Modules:
    @final
    class Effect(Module[In, Out]):
        def __init__(self, func: Callable[[In, Args.kwargs], Effect[Out]]):
            self.func = func

        def effect(self, data: In, **kwargs) -> Effect[Out]:
            return self.func(data, **kwargs)
    @final
    class Sync(Module[In, Out]):
        def __init__(self, func: Callable[[In, Args.kwargs], Out]):
            self.func = func

        def effect(self, data: In, **kwargs) -> Effect[Out]:
            def invoke() -> Out:
                return self.func(data, **kwargs)
            return Effects.Sync(invoke)

    @final
    class Async(Module[In, Out]):
        def __init__(self, func: Callable[[In, Args.kwargs], Coroutine[Any, Any, Out]]):
            self.func = func

        def effect(self, data: In, **kwargs) -> Effect[Out]:
            async def ainvoke() -> Coroutine[Any, Any, Out]:
                return await self.func(data, **kwargs)
            return Effects.Async(ainvoke)

    @final
    class Iterator(Module[In, Out]):
        def __init__(self, func: Callable[[In, Args.kwargs], Iterator[Out]]):
            self.func = func

        def effect(self, data: In, **kwargs) -> Effect[Out]:
            def _iter() -> Iterator[Out]:
                yield from self.func(data, **kwargs)
            return Effects.Iterator(_iter)

    @final
    class AsyncIterator(Module[In, Out]):
        def __init__(self, func: Callable[[In, Args.kwargs], AsyncIterator[Out]]):
            self.func = func

        def effect(self, data: In, **kwargs) -> Effect[Out]:
            async def _aiter() -> AsyncIterator[Out]:
                async for item in self.func(data, **kwargs):
                    yield item
            return Effects.AsyncIterator(_aiter)

ModuleFunction = Union[
    Callable[[In], Out],
    Callable[[In], Effect[Out]],
    Callable[[In], Coroutine[Any, Any, Out]],
    Callable[[In], Iterator[Out]],
    Callable[[In], AsyncIterator[Out]]
]
ModuleLike = Union[Module[In, Out], ModuleFunction[In, Out]]
ModuleMapping = Mapping[str, ModuleLike[In, Any]]

def coerce_to_module(thing: ModuleLike[In, Out] | ModuleMapping[In]) -> Module[In, Out]:
    if isinstance(thing, Module):
        return thing
    elif inspect.isasyncgenfunction(thing):
        return Modules.AsyncIterator(cast(Callable[[In, ...], AsyncIterator[Out]], thing))
    elif inspect.isgeneratorfunction(thing):
        return Modules.Iterator(cast(Callable[[In, ...], Iterator[Out]], thing))
    elif asyncio.iscoroutinefunction(thing):
        return Modules.Async(cast(Callable[[In, ...], Coroutine[Any, Any, Out]], thing))
    elif callable(thing):
        if is_return_type(thing, Effect):
            return Modules.Effect(thing)
        return Modules.Sync(thing)
    elif isinstance(thing, dict):
        from funcstack.modules.parallel import Parallel
        return cast(Module[In, Out], Parallel(**thing))
    else:
        raise TypeError(f'Expected a module, function, or dict. Got {type(thing)}.')

def module(func: ModuleFunction[In, Out]) -> Module[In, Out]:
    return coerce_to_module(func)