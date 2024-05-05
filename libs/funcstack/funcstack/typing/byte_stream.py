from typing import override

from funcstack.typing import Artifact

class ByteStream(Artifact):
    bytes_: bytes
    content_type: str

    def __init__(self, bytes_: bytes, content_type: str, **kwargs):
        super().__init__(**kwargs, bytes_=bytes_, content_type=content_type)

    @override
    def to_bytes(self, **kwargs) -> bytes:
        return self.bytes_