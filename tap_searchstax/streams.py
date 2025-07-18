"""Stream type classes for tap-searchstax."""

from __future__ import annotations
import typing as t
from singer_sdk.helpers import types
from singer_sdk.helpers.types import Context
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
        th.Property("created_at", th.DateTimeType),
        th.Property("search_studio_enabled", th.BooleanType),
        th.Property("cloud_manager_enabled", th.BooleanType),
        th.Property("analytics_enabled", th.BooleanType),
        th.Property("trial_days", th.IntegerType),
        th.Property("country", th.StringType),
        th.Property("parent_name", th.StringType)
    ).to_dict()

    def get_child_context(
            self,
            record: types.Record,
            context: types.Context | None,
    ) -> types.Context | None:
        """Return a context dictionary for child streams."""
        return {
            "account_name": record.get("name"),
            "year": self.config.get("year"),
            "month": self.config.get("month"),
        }

class UsageStream(SearchStaxStream):
    """Define custom stream."""

    name = "usage"
    path = "/account/{account_name}/usage-extended/{year}/{month}"
    primary_keys: t.ClassVar[list[str]] = ["account_name"]
    parent_stream_type = AccountsStream
    records_jsonpath = "$.[*]"
    ignore_parent_replication_keys = True
    schema = th.PropertiesList(
       th.Property("account_name", th.StringType),
        th.Property("startDate", th.DateTimeType),
        th.Property("endDate", th.DateTimeType),
        th.Property("contractEndDate", th.DateTimeType),
        th.Property("contractStatus", th.StringType),
        th.Property("SKU", th.StringType),
        th.Property("tagCollection", th.ArrayType(th.StringType)),
        th.Property("currency", th.StringType),
        th.Property("amount", th.NumberType),
        th.Property("maxAllowedRequests", th.IntegerType),
        th.Property("maxAllowedItems", th.IntegerType),
        th.Property("maxAppsAllowed", th.IntegerType),
        th.Property("displayMaxRequests", th.IntegerType),
        th.Property("displayMaxItems", th.IntegerType),
        th.Property("appsInfo", th.ArrayType(th.ObjectType(
                    th.Property("name", th.StringType),
                    th.Property("createdDate", th.DateTimeType),
                    th.Property("deletedDate", th.DateTimeType),
                    th.Property("status", th.StringType),
                    th.Property("totalRequests", th.IntegerType),
                    th.Property("totalItems", th.IntegerType)
                )))

    ).to_dict()

    def post_process(
            self,
            row: dict,
            context: Context | None = None,  # noqa: ARG002
    ) -> dict | None:
        """As needed, append or transform raw data to match expected structure.

        Note: As of SDK v0.47.0, this method is automatically executed for all stream types.
        You should not need to call this method directly in custom `get_records` implementations.

        Args:
            row: An individual record from the stream.
            context: The stream context.

        Returns:
            The updated record dictionary, or ``None`` to skip the record.
        """
        # Instead of direct access, use safe access
        if context is not None:
            row["account_name"] = context.get("account_name")
        return row

