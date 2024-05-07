from funcstack.containers import Effect, Effects
from funcstack.mixins import PydanticMixin
from funcstack.modules import Module
from funcstack.typing import ArtifactSource, TextArtifact

class PyPDFToText(PydanticMixin, Module[list[ArtifactSource], list[TextArtifact]]):
    def evaluate(self, data: list[ArtifactSource], **kwargs) -> Effect[list[TextArtifact]]:
        def _invoke() -> list[TextArtifact]:
            pass
        return Effects.Sync(_invoke)