from funcstack.containers import Effect
from funcstack.typing import Artifact, Document

from funcstack.mixins import PydanticMixin
from funcstack.modules import Module

class HtmlToDocument(PydanticMixin, Module[list[Artifact], list[Document]]):
    def evaluate(self, html: list[Artifact], **kwargs) -> Effect[list[Document]]:
        pass