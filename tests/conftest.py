# stdlib
from typing import Iterator

# 3rd party
import pytest
import requests
from _pytest.fixtures import FixtureRequest
from betamax import Betamax  # type: ignore[import-untyped]
from domdf_python_tools.paths import PathPlus
from shippinglabel_pypi import _session

pytest_plugins = ("coincidence", )

with Betamax.configure() as config:
	config.cassette_library_dir = PathPlus(__file__).parent / "cassettes"


@pytest.fixture()
def cassette(request: FixtureRequest) -> Iterator[requests.Session]:
	"""
	Provides a Betamax cassette scoped to the test function
	which record and plays back interactions with the PyPI API.
	"""  # noqa: D400

	with Betamax(_session) as vcr:
		vcr.use_cassette(request.node.name, record="none")

		yield _session
