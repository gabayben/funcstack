from abc import ABC
from typing import Any, Dict, Optional

from pydantic import Field

from funcstack.typing import BaseDoc, BaseUrl

class Artifact(BaseDoc, ABC):
    name: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @property
    def url(self) -> Optional[BaseUrl]:
        return None

    def _get_bytes(self) -> Optional[bytes]:
        return None

    class Config:
        arbitrary_types_allowed = True