from abc import ABC
from typing import Optional

from docarray.utils._internal.misc import ProtocolType
from pydantic import Field

from funcstack.typing import Artifact, AudioBytes, AudioUrl, ImageBytes, ImageUrl, VideoBytes, VideoUrl

class BlobArtifact(Artifact, ABC):
    base64: Optional[str] = Field(default=None, kw_only=True)

    def to_base64(
        self,
        protocol: ProtocolType = 'protobuf',
        compress: Optional[str] = None
    ) -> str:
        return self.base64 or super().to_base64(protocol=protocol, compress=compress)

class MediaArtifact(BlobArtifact):
    pass

class ImageArtifact(MediaArtifact):
    image_url: Optional[ImageUrl] = Field(alias='url', default=None, kw_only=True)
    image_bytes: Optional[ImageBytes] = Field(default=None, exclude=True, init=False)

class VideoArtifact(MediaArtifact):
    video_url: Optional[VideoUrl] = Field(alias='url', default=None, kw_only=True)
    video_bytes: Optional[VideoBytes] = Field(default=None, exclude=True, init=False)

class AudioArtifact(MediaArtifact):
    audio_url: Optional[AudioUrl] = Field(alias='url', default=None, kw_only=True)
    audio_bytes: Optional[AudioBytes] = Field(default=None, exclude=True, init=False)