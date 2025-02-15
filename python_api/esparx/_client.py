from urllib.parse import urljoin
from requests import Response, Session

from ._user_config import user_config

class ApiClient(Session):
    def __init__(self, base_url: str = "", headers: dict[str, str] = None) -> None:
        super().__init__()
        self.base_url = base_url
        self.headers = headers

    def request(self, method: str | bytes, url: str, json: dict | None = None, *args, **kwargs) -> Response:
        url = url.lstrip("/")
        joined_url = urljoin(self.base_url, url)

        # WARNING: Remove `verify=false` if official certificates are used
        return super().request(method, joined_url, json=json, verify=False, *args, **kwargs)

client = ApiClient(base_url=user_config.api_base)
"""Client for non identified API access"""

auth_client = ApiClient(base_url=user_config.api_base, headers={"X-user-id": user_config.user_id})
"""Client for API access with user identification"""
