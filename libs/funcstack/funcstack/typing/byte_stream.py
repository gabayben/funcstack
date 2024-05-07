from typing import Self, override

from funcstack.typing import Artifact

class ByteStream(Artifact):
    bytes_: bytes
    content_type: str

    def __init__(self, bytes_: bytes, content_type: str, **kwargs):
        super().__init__(**kwargs, bytes_=bytes_, content_type=content_type)

    @classmethod
    def from_text(cls, text: str, content_type: str) -> Self:
        return cls(bytes(text, 'utf-8'), content_type)

    @override
    def to_bytes(self, **kwargs) -> bytes:
        return self.bytes_