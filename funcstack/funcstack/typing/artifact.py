from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional, Self

from pydantic import Field

from funcstack.typing import BaseDoc, BaseUrl, Embedding
from funcstack.utils.paths import get_mime_type

class Artifact(BaseDoc, ABC):
    name: Optional[str] = None
    mime_type: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    embedding: Optional[Embedding] = Field(default=None, exclude=True, kw_only=True)
    score: Optional[float] = Field(default=None, kw_only=True)

    @classmethod
    def from_source(cls, source: 'ArtifactSource', metadata: dict[str, Any] = {}) -> Self:
        if isinstance(source, Artifact):
            metadata['mime_type'] = metadata.get('mime_type', None) or source.mime_type
            return cls.from_artifact(source, metadata)
        elif isinstance(source, BaseUrl):
            return cls.from_url(source, metadata)
        return cls.from_path(source, metadata)

    @classmethod
    def from_artifact(cls, other: 'Artifact', metadata: dict[str, Any] = {}) -> Self:
        artifact = cls.from_bytes(bytes(other))
        artifact.mime_type = other.mime_type or other.metadata.get('mime_type', None) or metadata.get('mime_type', None)
        artifact.metadata.update({**other.metadata, **metadata})
        return artifact

    @classmethod
    def from_path(cls, path: str | Path, metadata: dict[str, Any] = {}) -> Self:
        if isinstance(path, Path):
            valid_path = path.as_uri()
        else:
            valid_path = path
        return cls.from_bytes(BaseUrl(valid_path).load_bytes())

    def is_empty(self) -> bool:
        return bytes(self) == b''

    @staticmethod
    def get_mime_type(source: 'ArtifactSource') -> str:
        path: Path
        if isinstance(source, str):
            path = Path(source)
        if isinstance(source, Path):
            mime_type = get_mime_type(source)
        elif isinstance(source, BaseUrl):
            mime_type = source.mime_type
        elif isinstance(source, Artifact):
            mime_type = source.mime_type
        else:
            raise ValueError(f'Unsupported data source type: {type(source).__name__}.')
        return mime_type

    class Config:
        extra = 'allow'
        arbitrary_types_allowed = True

class Utf8Artifact(Artifact, ABC):
    def to_bytes(self, **kwargs) -> bytes:
        return str(self).encode(encoding='utf-8')

    def __str__(self) -> str:
        return self.to_utf8()

    @abstractmethod
    def to_utf8(self) -> str:
        pass

StrictArtifactSource = Path | Artifact
ArtifactSource = str | StrictArtifactSource