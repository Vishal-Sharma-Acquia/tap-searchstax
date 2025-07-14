"""Stream type classes for tap-searchstax."""

from __future__ import annotations

import typing as t
from importlib import resources

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_searchstax.client import SearchStaxStream



class AccountsStream(SearchStaxStream):
    """Define custom stream."""

    name = "accounts"
    path = "/account"
    primary_keys: t.ClassVar[list[str]] = ["name"]
    replication_key = None
    next_page_token_jsonpath = "$.next"
    records_jsonpath = "$.results[*]"
    schema = th.PropertiesList(
        th.Property("name", th.StringType),
        th.Property("trial", th.BooleanType),
        th.Property("created_at", th.DateTimeType)
    ).to_dict()


class GroupsStream(SearchStaxStream):
    """Define custom stream."""

    name = "groups"
    path = "/groups"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = "modified"
    schema = th.PropertiesList(
        th.Property("name", th.StringType),
        th.Property("id", th.StringType),
        th.Property("modified", th.DateTimeType),
    ).to_dict()
