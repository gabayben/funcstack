from funcstack.typing import Artifact

from funcstack.containers import Effect
from funcstack.modules import Module

class LostInTheMiddleRanker(Module[list[Artifact], list[Artifact]]):
    def evaluate(
        self,
        data: list[Artifact],
        top_k: int = 10
    ) -> Effect[list[Artifact]]:
        pass