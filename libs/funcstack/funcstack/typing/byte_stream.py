from typing import Self, Type, override

from docarray.base_doc.mixins.io import T

from funcstack.typing import Artifact

class ByteStream(Artifact):
    bytes_: bytes
    content_type: str

    def __init__(self, bytes_: bytes, content_type: str = '', **kwargs):
        super().__init__(**kwargs, bytes_=bytes_, content_type=content_type)

    @classmethod
    def from_text(cls, text: str, content_type: str = '') -> Self:
        return cls(bytes(text, 'utf-8'), content_type=content_type)

    @classmethod
    def from_bytes(
        cls: Type[T],
        data: bytes,
        **kwargs
    ) -> 'ByteStream':
        return ByteStream(data)

    @override
    def to_bytes(self, **kwargs) -> bytes:
        return self.bytes_