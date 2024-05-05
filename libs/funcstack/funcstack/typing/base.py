from abc import ABC
from typing import Any, Optional

from pydantic import Field

from funcstack.typing import BaseDoc

class Artifact(BaseDoc, ABC):
    name: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True