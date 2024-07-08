from djnago.test import override_settings

import pytest


@pytest.fixture(autouse=True)
def test_settings(settings):
	with override_settings(SECRET_KEY='...',):
		yield
