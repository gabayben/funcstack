from funcstack.containers import Effect
from funcstack.mixins import PydanticMixin
from funcstack.modules import Module
from funcstack.typing import Artifact

class LinkContentFetcher(PydanticMixin, Module[list[str], list[Artifact]]):
    def evaluate(self, urls: list[str], **kwargs) -> Effect[list[Artifact]]:
        pass