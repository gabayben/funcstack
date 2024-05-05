from funcstack.containers import Effect
from funcstack.mixins import PydanticMixin
from funcstack.modules import Module
from funcstack.typing._vars import In

class Passthrough(PydanticMixin, Module[In, In]):
    def evaluate(self, data: In, **kwargs) -> Effect[In]:
        pass