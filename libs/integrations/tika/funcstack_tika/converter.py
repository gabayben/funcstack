from typing import Any

from funcstack.containers import Effect, Effects
from funcstack.mixins import PydanticMixin
from funcstack.modules import Module
from funcstack.typing import ArtifactSource, TextArtifact
from funcstack.utils.dicts import normalize_metadata
from funcstack.utils.func import zip2

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
                pass
        
        return Effects.Sync(_invoke)