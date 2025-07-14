"""SearchStax tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_searchstax import streams


class TapSearchStax(Tap):
    """SearchStax tap class."""

    name = "tap-searchstax"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "user_name",
            th.StringType(nullable=False),
            required=True,
            secret=True,  # Flag config as protected.
            title="User Name",
            description="The User Name to authenticate against the API service",
        ),
        th.Property(
            "password",
            th.StringType(nullable=False),
            required=True,
            secret=True,  # Flag config as protected.
            title="Password",
            description="The Password to authenticate against the API service",
        ),
        th.Property(
            "start_date",
            th.DateTimeType(nullable=True),
            description="The earliest record date to sync",
        ),
        th.Property(
            "user_agent",
            th.StringType(nullable=True),
            description=(
                "A custom User-Agent header to send with each request. Default is "
                "'<tap_name>/<tap_version>'"
            ),
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.SearchStaxStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.GroupsStream(self),
            streams.AccountsStream(self),
        ]


if __name__ == "__main__":
    TapSearchStax.cli()
