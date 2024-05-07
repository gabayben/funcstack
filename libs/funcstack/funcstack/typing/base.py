from abc import ABC
from pathlib import Path
from typing import Any, Optional, Self

from pydantic import Field

from funcstack.typing import BaseDoc, BaseUrl, TextUrl

class Artifact(BaseDoc, ABC):
    name: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_source(cls, source: 'ArtifactSource') -> Self:
        if isinstance(source, Artifact):
            return cls.from_artifact(source)
        elif isinstance(source, BaseUrl):
            return cls.from_url(source)
        return cls.from_path(source)

    @classmethod
    def from_artifact(cls, other: 'Artifact') -> Self:
        artifact = cls.from_bytes(bytes(other))
        artifact.metadata.update(other.metadata)
        return artifact

    @classmethod
    def from_url(cls, url: BaseUrl) -> Self:
        artifact = cls.from_bytes(url.load_bytes())
        artifact.metadata['url'] = url
        return artifact

    @classmethod
    def from_path(cls, path: str | Path) -> Self:
        if isinstance(path, Path):
            valid_path = path.as_uri()
        else:
            valid_path = path
        return cls.from_url(TextUrl(valid_path)) #type: ignore[call-args]

    def to_utf8(self) -> str:
        return bytes(self).decode('utf-8')

    def is_empty(self) -> bool:
        return bytes(self) == b''

    class Config:
        extra = 'allow'
        arbitrary_types_allowed = True

ArtifactSource = str | Path | BaseUrl | Artifact