import io
import logging
from typing import Any, Self

from pypdf import PdfReader

from funcstack.containers import Effect, Effects
from funcstack.mixins import PydanticMixin
from funcstack import Module
from funcstack import ArtifactSource, ByteStream, TextArtifact
from funcstack.utils.dicts import normalize_metadata
from funcstack.utils.func import zip2
from funcstack_pypdf import PyPDFConverter

logger = logging.getLogger(__name__)

class _DefaultConverter(PydanticMixin, PyPDFConverter):
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(**data)
    
    def to_dict(self) -> dict[str, Any]:
        return self.model_dump()
    
    def convert(self, reader: PdfReader) -> TextArtifact:
        return TextArtifact('\f'.join([page.extract_text() for page in reader.pages]))

class PyPDFToText(PydanticMixin, Module[list[ArtifactSource], list[TextArtifact]]):
    converter: PyPDFConverter
    
    def __init__(self, converter: PyPDFConverter | None = None):
        super().__init__(converter = converter or _DefaultConverter())
    
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
                    pdf_reader = PdfReader(io.BytesIO(bytes(bytestream)))
                    results.append(self.converter.convert(pdf_reader))
                except Exception as e:
                    logger.warning(f'Could not read {source} and convert it to TextArtifact. Skipping it. Error: {e}.')

            return results

        return Effects.Sync(_invoke)