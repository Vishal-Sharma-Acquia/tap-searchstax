from __future__ import annotations
import typing as t
import requests
from singer_sdk.authenticators import APIAuthenticatorBase

if t.TYPE_CHECKING:
    from singer_sdk.streams.rest import _HTTPStream

class SearchStaxAuthenticator(APIAuthenticatorBase):
    """Implements basic authentication for REST Streams.

    .. deprecated:: 0.36.0
       Use :class:`requests.auth.HTTPBasicAuth` instead.

    This Authenticator implements basic authentication by concatenating a
    username and password then base64 encoding the string. The resulting
    token will be merged with any HTTP headers specified on the stream.
    """

    def __init__(
            self,
            stream: _HTTPStream,
            username: str,
            password: str,
    ) -> None:
        """Create a new authenticator.

        Args:
            stream: The stream instance to use with this authenticator.
            username: API username.
            password: API password.
        """
        super().__init__(stream=stream)
        self.username = username
        self.password = password

        credentials_payload = {
            "username": self.username,
            "password": self.password
        }
        response = requests.post("https://app.searchstax.com/api/rest/v2/obtain-auth-token/", json=credentials_payload)
        token_data = response.json()
        self.auth_token = token_data.get('token')
        self.auth_credentials = {"Authorization": f"Token {self.auth_token}"}


    @classmethod
    def create_for_stream(
            cls: type[SearchStaxAuthenticator],
            stream: _HTTPStream,
            username: str,
            password: str,
    ) -> SearchStaxAuthenticator:
        """Create an Authenticator object specific to the Stream class.

        Args:
            stream: The stream instance to use with this authenticator.
            username: API username.
            password: API password.

        Returns:
            BasicAuthenticator: A new
                :class:`singer_sdk.authenticators.BasicAuthenticator` instance.
        """
        return cls(stream=stream, username=username, password=password)
