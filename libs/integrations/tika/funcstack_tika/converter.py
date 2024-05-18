import io
import logging
from typing import Any

from tika import parser

from funcstack.containers import Effect, Effects
from funcstack.mixins import PydanticMixin
from funcstack import Module
from funcstack import ArtifactSource, ByteStream, TextArtifact
from funcstack.utils.dicts import normalize_metadata
from funcstack.utils.func import zip2

logger = logging.getLogger(__name__)

class TikaTextConverter(PydanticMixin, Module[list[ArtifactSource], list[TextArtifact]]):
    tika_url: str
    
    def __init__(self, tika_url: str = 'http://localhost:9998/tika'):
        super().__init__(tika_url=tika_url)

    def evaluate(
        self, 
        sources: list[ArtifactSource], 
        metadata: dict[str, Any] | list[dict[str, Any]] | None = None
    ) -> Effect[list[TextArtifact]]:
        def _invoke() -> list[TextArtifact]:
            results: list[TextArtifact] = []
            meta_list = normalize_metadata(metadata, len(sources))
            
            for source, md in zip2(sources, meta_list):
                try:
                    bytestream = ByteStream.from_source(source, md)
                except Exception as e:
                    logger.warning(f'Could not read {source}. Skipping it. Error: {e}.')
                    continue
                try:
                    text = parser.from_buffer(io.BytesIO(bytes(bytestream)), serverEndpoint=self.tika_url)['content']
                except:
                    logger.warning(f'Failed to extract text from {source}. Skipping it. Error: {e}.')
                    continue
                results.append(TextArtifact(text))

            return results
        
        return Effects.Sync(_invoke)