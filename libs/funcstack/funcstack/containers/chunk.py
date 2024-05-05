from abc import ABC, abstractmethod
from typing import Generic, Iterable

from funcstack.typing._vars import Out

class ISingleton(Generic[Out], ABC):
    @property
    @abstractmethod
    def value(self) -> Out:
        pass

class IList(Generic[Out], ABC):
    @property
    @abstractmethod
    def list(self) -> list[Out]:
        pass

class IConcat(Generic[Out], ABC):
    @property
    @abstractmethod
    def left(self) -> 'Chunk[Out]':
        pass

    @property
    @abstractmethod
    def right(self) -> 'Chunk[Out]':
        pass

class ISlice(Generic[Out], ABC):
    @property
    @abstractmethod
    def chunk(self) -> 'Chunk[Out]':
        pass

    @property
    @abstractmethod
    def length(self) -> int:
        pass

    @property
    @abstractmethod
    def offset(self) -> int:
        pass

Backing = ISingleton[Out] | IList[Out] | IConcat[Out] | ISlice[Out]

class Chunk(Iterable[Out], ABC):
    @property
    @abstractmethod
    def length(self) -> int:
        pass

    @property
    @abstractmethod
    def depth(self) -> int:
        pass

    @property
    @abstractmethod
    def left(self) -> 'Chunk[Out]':
        pass

    @property
    @abstractmethod
    def right(self) -> 'Chunk[Out]':
        pass

    @property
    @abstractmethod
    def backing(self) -> Backing[Out]:
        pass