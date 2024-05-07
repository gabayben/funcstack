import logging
from typing import Any, ClassVar, Literal

from boilerpy3 import extractors
from boilerpy3.extractors import Extractor

from funcstack.containers import Effect, Effects
from funcstack.typing import ArtifactSource, ByteStream, TextArtifact
from funcstack.mixins import PydanticMixin
from funcstack.modules import Module
from funcstack.utils.dicts import normalize_metadata
from funcstack.utils.func import zip2

logger = logging.getLogger(__name__)

class HtmlToText(PydanticMixin, Module[list[ArtifactSource], list[TextArtifact]]):
    known_extractors: ClassVar[list[str]] = [
        'DefaultExtractor',
        'ArticleExtractor',
        'ArticleSentencesExtractor',
        'LargestContentExtractor',
        'CanolaExtractor',
        'KeepEverythingExtractor',
        'NumWordsRulesExtractor'
    ]

    def __init__(
        self,
        extractor_type: Literal[
            'DefaultExtractor',
            'ArticleExtractor',
            'ArticleSentencesExtractor',
            'LargestContentExtractor',
            'CanolaExtractor',
            'KeepEverythingExtractor',
            'NumWordsRulesExtractor',
        ] = 'DefaultExtractor',
        try_others: bool = True
    ):
        super().__init__()
        self.extractor_type = extractor_type
        self.try_others = try_others

    def evaluate(
        self,
        sources: list[ArtifactSource],
        metadata: dict[str, Any] | list[dict[str, Any]] | None = None
    ) -> Effect[list[TextArtifact]]:
        def _invoke() -> list[TextArtifact]:
            results: list[TextArtifact] = []
            metadata_list = normalize_metadata(metadata, len(sources))

            extractors_list = (
                list(dict.fromkeys([self.extractor_type, *self.known_extractors]))
                if self.try_others
                else [self.extractor_type]
            )

            for source, md in zip2(sources, metadata_list):
                try:
                    bytestream = ByteStream.from_source(source)
                except Exception as e:
                    logger.warning(f'Could not read {source}. Skipping it. Error: {e}.')
                    continue
                for extractor_name in extractors_list:
                    extractor_cls = getattr(extractors, extractor_name)
                    extractor: Extractor = extractor_cls(raise_on_failure=False)
                    try:
                        text = extractor.get_content(bytestream.to_utf8())
                        if text:
                            break
                    except Exception as e:
                        if self.try_others:
                            logger.warning(f'Failed to extract using {extractor_name} from {source}. Trying next extractor. Error: {e}.')
                if not text:
                    logger.warning(f'Failed to extract text using extractors {extractors_list}. Skipping it.')
                    continue
                results.append(TextArtifact(text, metadata={**bytestream.metadata, **md}))

            return results

        return Effects.Sync(_invoke)