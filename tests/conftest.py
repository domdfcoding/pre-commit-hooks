# 3rd party
import pytest
from _pytest.fixtures import FixtureRequest
from shippinglabel.pypi import PYPI_API

# 3rd party
from betamax import Betamax  # type: ignore
from domdf_python_tools.paths import PathPlus

pytest_plugins = ("domdf_python_tools.testing", )

with Betamax.configure() as config:
	config.cassette_library_dir = PathPlus(__file__).parent / "cassettes"


@pytest.fixture()
def cassette(request: FixtureRequest):
	"""
	Provides a Betamax cassette scoped to the test function
	which record and plays back interactions with the PyPI API.
	"""  # noqa: D400

	with Betamax(PYPI_API._store["session"]) as vcr:
		vcr.use_cassette(request.node.name, record="none")

		yield PYPI_API
