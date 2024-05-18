from typing import Optional

from docarray.utils._internal.misc import ProtocolType

from funcstack.typing import Artifact

class TextArtifact(Artifact):
    content: str
    encoding: str = 'utf-8'

    def __init__(self, content: str, **kwargs):
        super().__init__(**kwargs, content=content)

    def __str__(self) -> str:
        return self.content

    def to_base64(
        self,
        protocol: ProtocolType = 'protobuf',
        compress: Optional[str] = None
    ) -> str:
        return str(self)

    def to_bytes(
        self,
        protocol: ProtocolType = 'protobuf',
        compress: Optional[str] = None
    ) -> bytes:
        return str(self).encode(encoding=self.encoding)