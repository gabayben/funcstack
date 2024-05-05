from typing import Optional

from docarray.utils._internal.misc import ProtocolType
from pydantic import Field

from funcstack.typing import Artifact, Embedding

class Document[T: Artifact](Artifact):
    data: T
    embedding: Optional[Embedding] = Field(default=None, exclude=True, kw_only=True)
    score: Optional[float] = Field(default=None, kw_only=True)

    def __init__(self, data: T, **kwargs):
        super().__init__(data=data, **kwargs)

    def __str__(self) -> str:
        return str(self.data)

    def to_base64(
        self,
        protocol: ProtocolType = 'protobuf',
        compress: Optional[str] = None
    ) -> str:
        return self.data.to_base64(protocol=protocol, compress=compress)

    def to_bytes(
        self,
        protocol: ProtocolType = 'protobuf',
        compress: Optional[str] = None
    ) -> bytes:
        return self.data.to_bytes(protocol=protocol, compress=compress)