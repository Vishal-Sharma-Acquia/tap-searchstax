"""REST client handling, including SearchStaxStream base class."""

from __future__ import annotations
from tap_searchstax.auth import SearchStaxAuthenticator
from urllib.parse import parse_qsl
import decimal
import typing as t
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseHATEOASPaginator  # noqa: TC002
from singer_sdk.streams import RESTStream


if t.TYPE_CHECKING:
    import requests
    from singer_sdk.helpers.types import Context




class SearchStaxStream(RESTStream):
    """SearchStax stream class."""

    # Update this value if necessary or override `parse_response`.
    records_jsonpath = "$[*]"

    # Update this value if necessary or override `get_new_paginator`.
    next_page_token_jsonpath = "$.next_page"  # noqa: S105

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return "https://app.searchstax.com/api/rest/v2"

    @property
    def authenticator(self) -> SearchStaxAuthenticator:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return SearchStaxAuthenticator.create_for_stream(self,
                                                         self.config.get("user_name"),
                                                         self.config.get("password"))

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        # If not using an authenticator, you may also provide inline auth headers:
        # headers["Private-Token"] = self.config.get("auth_token")  # noqa: ERA001
        return self.authenticator.auth_credentials

    def get_new_paginator(self) -> SearchStaxHATEOASPaginator:
        """Create a new pagination helper instance.

        If the source API can make use of the `next_page_token_jsonpath`
        attribute, or it contains a `X-Next-Page` header in the response
        then you can remove this method.

        If you need custom pagination that uses page numbers, "next" links, or
        other approaches, please read the guide: https://sdk.meltano.com/en/v0.25.0/guides/pagination-classes.html.

        Returns:
            A pagination helper instance, or ``None`` to indicate pagination
            is not supported.
        """
        return super().get_new_paginator()

    def get_url_params(
        self,
        context: Context | None,  # noqa: ARG002
        next_page_token: t.Any | None,  # noqa: ANN401
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        if next_page_token:
            if hasattr(next_page_token, "query"):
                params.update(parse_qsl(next_page_token.query))
            elif isinstance(next_page_token, str):
                params.update(parse_qsl(next_page_token))
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key
        return params


    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        # TODO: Parse response body and return a set of records.
        yield from extract_jsonpath(
            self.records_jsonpath,
            input=response.json(parse_float=decimal.Decimal),
        )


class SearchStaxHATEOASPaginator(BaseHATEOASPaginator):
    def get_next_url(self, response):
        return response.json().get("next")
