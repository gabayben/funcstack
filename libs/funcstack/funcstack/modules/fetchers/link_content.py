import urllib3

from funcstack.containers import Effect
from funcstack.mixins import PydanticMixin
from funcstack.modules import Module
from funcstack.typing import ByteStream
from funcstack.version import __version__

DEFAULT_USER_AGENT = f'funcstack/LinkContentFetcher/{__version__}'
REQUEST_HEADERS = {
    'accept': '*/*',
    'User-Agent': DEFAULT_USER_AGENT,
    'Accept-Language': 'en-US,en;q=0.9,it;q=0.8,es;q=0.7',
    'referer': 'https://www.google.com/',
}

class LinkContentFetcher(PydanticMixin, Module[list[str], list[ByteStream]]):
    def __init__(
        self,
        user_agents: list[str] | None = None,
        raise_on_failure: bool = True
    ):
        super().__init__(
            user_agents = user_agents or [DEFAULT_USER_AGENT],
            raise_on_failure=raise_on_failure
        )

    def evaluate(self, urls: list[str], **kwargs) -> Effect[list[ByteStream]]:
        pass

    def get_response(self, url: str):
        data = urllib3.request(
            'GET',
            url,
            headers=REQUEST_HEADERS
        )