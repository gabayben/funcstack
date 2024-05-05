from funcstack.containers import Effect
from funcstack.modules import Module
from funcstack.typing import Document

class LostInTheMiddleRanker(Module[list[Document], list[Document]]):
    def evaluate(
        self,
        data: list[Document],
        top_k: int = 10
    ) -> Effect[list[Document]]:
        pass